from typing import Dict, Tuple, Union
import time
from PyQt5.QtCore import  QObject, QTimer, pyqtSignal, pyqtSlot, QMutex, QMutexLocker, QWaitCondition
import struct
import serial  
import serial.tools.list_ports
import threading  
import queue 
import COMMANDS as COMM       



class SerialPortHandler(QObject):

    """
        Класс для асинхронной обработки данных из последовательного порта.
        Реализует событийную модель обработки данных    
        Использует два потока:
        1. Поток чтения - постоянно проверяет порт на наличие новых данных
        2. Поток обработки - забирает данные из очереди и передает их в обработчики
    """

    ############################# Сигналы для вызова обработчика принятого пакета   
    
    paed_signal = pyqtSignal(bytearray)                  # сигнал вызова обработчика для получения ПАЕД 
    ser_num_signal = pyqtSignal(bytearray)               # сигнал вызова обработчика для получения серийного номера
    rad_intens_signal = pyqtSignal(bytearray)            # сигнал вызова обработчика для получения интенсивности радиации  
    temp_signal = pyqtSignal(bytearray)                  # сигнал вызова обработчика для получения температуры  
    simple_spectre_signal = pyqtSignal(bytearray)        # сигнал вызова обработчика простого спектра
    time_spectre_signal = pyqtSignal(bytearray)          # сигнал вызова обработчика часового спектра



    one_dim_spectre_start_signal = pyqtSignal(bytearray)   # сигнал вызова обработчика для старта набора одномерного спектра 
    one_dim_spectre_clear_signal = pyqtSignal(bytearray)   # сигнал вызова обработчика для очистки одномерного спектра 
    one_dim_spectre_get_signal   = pyqtSignal(bytearray)   # сигнал вызова обработчика для выдачи одномерного спектра 


    two_dim_spectre_start_signal = pyqtSignal(bytearray)   # сигнал вызова обработчика для старта набора одномерного спектра 
    two_dim_spectre_clear_signal = pyqtSignal(bytearray)   # сигнал вызова обработчика для очистки одномерного спектра 
    two_dim_spectre_get_signal   = pyqtSignal(bytearray)   # сигнал вызова обработчика для выдачи одномерного спектра 

    # сигнал передачи данных в GUI (тип данных - словарь)   
    gui_info_signal = pyqtSignal(object)   

    def __init__(self):    
        """
            Инициализация обработчика последовательного порта.        
            Args:
                port (str): Имя порта (например, 'COM1' для Windows или '/dev/ttyUSB0' для Unix)
                baudrate (int): Скорость передачи данных в бодах (по умолчанию 9600)        
            Note:
                timeout = 1 устанавливает таймаут на 1 секунду для операций чтения
        """
        super(SerialPortHandler, self).__init__()  # Вызов конструктора QObject
        self.serial_port = None          # Создаем только атрибут порта без открытия  СОМ-порта
        self.port_name = None            # Создаем только атрибут имени порта без присвоения значения
        self.running = False               # Флаг работы потоков
        self.error_read_count = 0             # Счетчик ошибок ответов девайса 
        self.error_write_count = 0             # Счетчик ошибок ответов девайса
        self.command = None                    # Копия команды для записи в девайс
        self.wait_condition = QWaitCondition()   # Для координации потоков чтения и записи
        self.mutex = QMutex()              # Создаем объект QMutex  для методов записи-чтения
        self.mode_mutex = QMutex()              # Создаем объект QMutex для изменения данных режима 
        self.reader_thread = None             # Атрибут потока чтения данных
        self.write_thread  = None             # Атрибут потока записи данных
        self.error_timer = QTimer(self)        # Таймер повторения запроса
        self.error_timer.timeout.connect(self.proc_error_timer) 
  
        self.previous_simple_spectre_time = None
        
        self.mode_tuple = ("", 0)  #  Атрибут режима работы и длины пакета (кортеж)
        
        # Коннект сигналов с обработчиками принятых данных
        self.paed_signal.connect(self._paed_data)        
        self.ser_num_signal.connect(self._ser_num_data)    
        self.rad_intens_signal.connect(self._rad_intens_data) 
        self.temp_signal.connect(self._temp_data)  
       
       

    def open_serial_port(self, serial_port, port_name: str = None, baud_rate: int = 115200, time_out: int = 1)-> None:
        """
            Функция создания и открытия Serial Port
            Note: В любои случае закрывается старый объект порта,
            создается и открывается новый порт
        """ 
        if serial_port and serial_port.is_open:
            serial_port.close()

        if port_name == None:
            port_name = self.port_name

        ser = serial.Serial(
            port = port_name,
            baudrate = baud_rate,
            bytesize = serial.EIGHTBITS,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            timeout = time_out
        )
        if ser.is_open:
            return ser
        else:
            return None  

    @pyqtSlot()
    def find_device_port(self) -> None:
        """
        Определяет имя COM-порта, к которому подключен прибор.
        Возвращает имя порта (например, 'COM3') или None, если прибор не найден.
        """
        ports = list(serial.tools.list_ports.comports())
        
        search_flag = False

        try:
        
            for port in ports:
                
                    # Не "USB" порты пропускаем
                    if not "USB" in port.description:  continue 
                    
                    # Создаем и открываем очередной порт
                    if self.serial_port != None:
                        if self.serial_port.isOpen():
                            self.serial_port.close()
                        self.serial_port = None
                   
                    ser = serial.Serial(port.device, baudrate = 115200, timeout = 1)  
                        
                    
                    # Формируем и отправляем запрос серийного номера + CRC 
                    command = bytearray([0x55, 0xAA, 0x70, 0x01, 0x05])          
                    crc = self.calc_crc(command)              
                    command.append(crc)  
                    ser.write(command)             
                    ser.flush()                
                    
                    time.sleep(0.2) # Ожидаем ответа
                    
                    if ser.in_waiting:
                        response = ser.read_all()
                        if self.verify_crc(response):  # Принят "нужный" пакет - значит, нашли СОМ-порт
                            ser.close()
                            self.port_name = port.device
                            self.serial_port = self.open_serial_port(None, port.device) # Здесь открываем нужный нам порт для работы
                            info_dict = {"type": "search_port", "inner_type": "dev_search", "port": port.device} 
                            search_flag = True                            
                            if self.gui_info_signal: 
                                self.gui_info_signal.emit(info_dict)
                            self.start_reader_thread()
                            return None
                    ser.close()

            if not search_flag:
                info_dict = {"type": "search_port", "inner_type": "dev_no_search", "message": "Немає підключених приладів"}                 
                if self.gui_info_signal: 
                    self.gui_info_signal.emit(info_dict)
                return None



        except serial.SerialException as e:
            info_dict = {"type": "search_port", "inner_type": "search_dev_serial_port_error", "message": str(e)}
            if self.gui_info_signal:
                self.gui_info_signal.emit(info_dict) 
                return None
                
        except Exception as e:
            info_dict = {"type": "search_port", "inner_type": "search_dev_unknown_error", "message": str(e)}
            if self.gui_info_signal:
                self.gui_info_signal.emit(info_dict) 
                return None
        return None
    
   

    def clear_mode(self)-> None:
        """
        Сбрасываем кортеж режима в None
        """
        with QMutexLocker(self.mode_mutex):  
            self.mode_tuple = None

    def set_mode(self, comm_name: str, comm_len: int) -> None:
        """
        Устанавливает режим с использованием мьютекса для защиты.
        """
        with QMutexLocker(self.mode_mutex):  
            self.mode_tuple = (comm_name, comm_len)
  
    def get_mode(self) -> None:
        """
        Функция возвращает кортеж режима:
            название режима (str)
            длину ожидаемого пакета (int)
        """       
        with QMutexLocker(self.mode_mutex):  
            if self.mode_tuple:
                return self.mode_tuple[0], self.mode_tuple[1]
            return None

    def calc_crc(self, buff: bytearray) -> int:
        """
            Функция расчета CRC для массива bytearray
        """        
        crc = 0
        for i in range(len(buff)):
            crc += buff[i]
            if (crc & 0x0100) == 0x0100:
                crc = (crc & 0xFF) + 1   
        return crc    

    def verify_crc(self, buff: bytearray)-> bool:
        """
            Функция контроля CRC для массив
            Возвращает True(совпало) или False(не совпало)
        """        
        if len(buff) < 2: 
            return False  
        expected_crc = buff[-1]      
        calculated_crc =  self.calc_crc(buff[:-1])          
        return calculated_crc == expected_crc 

    # Создаем и запускаем поток чтения данных
    def start_reader_thread(self) -> None:
        """
        Запуск потока для функции чтения 
        """
        self.running = True
        self.reader_thread = threading.Thread( target = self._read_data_spectre, daemon = True )
        self.reader_thread.start()

    # Останавливаем поток чтения данных и закрываем порт
    def stop_reader_thread(self) -> None:
        """
        Корректная остановка потока для функции чтения, закрытие порта
        """
        self.running = False

        # Ждем завершения потока чтения, если он был создан
        if hasattr(self, 'reader_thread') and self.reader_thread is not None:
            self.reader_thread.join()   

        # Ждем завершения потока чтения, если он был создан
        if hasattr(self, 'write_thread') and self.write_thread is not None:
            self.write_thread.join()   

        # Закрываем последовательный порт
        if self.serial_port:
            self.serial_port.close() 
            return (not self.serial_port.isOpen()) and (not self.reader_thread.is_alive()) 
        
        return True 
      

    @pyqtSlot()
    def proc_error_timer(self):
        self.error_timer.stop()
        if self.command:            
            command = self.command
            self.handle_write_signal(command) 
            info_dict = {"type": "global_write_error", "message": "Відбувся повторний запит у прилад"}

        else:
            info_dict = {"type": "global_write_error", "message": "Проблема з перезапуском таймеру помилок"}

        if self.gui_info_signal: 
            self.gui_info_signal.emit(info_dict) 


    @pyqtSlot(object)
    def handle_write_signal(self, command):
        try:           
            self.write_thread = threading.Thread(target = self.write_data, args=(command,))
            self.write_thread.start()

        except Exception as e:
            info_dict = {"type": "global_write_error", "message": "Виник exception у потоку запису даних"}
            if self.gui_info_signal: 
                self.gui_info_signal.emit(info_dict) 



    @pyqtSlot(object)
    def write_data(self, command):
        """
        Метод записи данных в serial port.
        Ожидает завершения метода чтения, если он выполняется.
        """
        try:            
            self.mutex.lock()

            # Если в порту есть данные - ожидаем, пока метод _read_data_spectre завершит работу с портом
            while self.serial_port and self.serial_port.in_waiting > 0:
                self.wait_condition.wait(self.mutex)

            time.sleep(0.005)

            # Приступаем к записи данных
            
            comm_name = command.name
            comm_data = command.data
            comm_len = command.length

            crc = self.calc_crc(comm_data)
            buff = bytearray(comm_data)
            buff.append(crc)

            self.clear_mode()  # Сбрасываем режим до успешной записи

            if self.serial_port:
                num_bytes = self.serial_port.write(buff)
                self.serial_port.flush()           
                
                if num_bytes != len(buff):                    # Некорректная запись в порт
                    self.error_write_count += 1
                    if self.error_write_count < COMM.Const.MAX_ERROR:
                        # Число ошибок не превысило максимум, "перезагружаем" наш порт 
                        # повторяем попытку записи                    
                        self.command = command            # Сохраняем копию команды и данные режима 
                        _port = self.port_name
                        local_port = self.serial_port
                        self.serial_port = self.open_serial_port(local_port, _port)    
                        self.error_timer.start(COMM.Const.WAIT_TIME)                        
                    else:
                    # Число ошибок превысило максимум,                         
                        info_dict = {"type": "global_write_error", "message": "Дані не записуються у порт"}
                        if self.gui_info_signal:
                            self.gui_info_signal.emit(info_dict)                  

                else:         # Корректная запись в порт, сбрасываем счетчик ошибок записи                
                    self.set_mode(comm_name, comm_len)     # Записали данные запроса в кортеж режима                      
                    self.error_write_count = 0          
    
            else:
                info_dict = {"type": "global_write_error", "message": "Порт не подключен"}
                self.gui_info_signal.emit(info_dict)
        except serial.SerialException as e:
            info_dict = {"type": "global_write_error", "message": f"Ошибка записи в порт: {str(e)}"}
            self.gui_info_signal.emit(info_dict)
        except Exception as e:
            info_dict = {"type": "global_write_error", "message": f"Неизвестная ошибка записи: {str(e)}"}
            self.gui_info_signal.emit(info_dict)
        finally:
            self.mutex.unlock()




    def _read_data_spectre(self):
        """
        Метод постоянного чтения данных из serial port.
        Работает в отдельном потоке и блокирует мьютекс только на время чтения.
        """
        try:
            while self.running:
                if self.serial_port and self.serial_port.in_waiting > 0:   # В порту есть байты                   
                    
                    # Получаем текущий режим и длину пакета после записи в девайс
                    mode, pack_size = self.get_mode()

                    try:

                        # Приступаем к вычитыванию данных, блокируем мьютекс
                        self.mutex.lock()

                        data = bytearray()

                        # Пока есть данные в порту, вычитываем
                        while self.serial_port.in_waiting > 0:
                            data += self.serial_port.read_all()
                            time.sleep(0.01) 

                        _size =   len(data)                     
                            
                        if _size >= pack_size: 
                            buff = bytearray(data[:pack_size])
                            
                            #Проверяем CRC
                            if self.verify_crc(buff):
                                self.error_read_count = 0 
                                
                                match mode:
                                    case "RAD_DOSE":                    
                                        self.paed_signal.emit(buff.copy()) # ПАЕД                                  

                                    case "SER_NUM" :                                                
                                        self.ser_num_signal.emit(buff.copy()) # серийный номер                                                            
                    
                                    case "RAD_INTENS" :                                               
                                        self.rad_intens_signal.emit(buff.copy()) # интенсивность 100 мсек                                    
                                                        
                                    case "TEMP" :
                                        self.temp_signal.emit(buff.copy())   # Обрабатываем температуру                                    

                                    case "TOGGLE_SIMPLE_SPECTRE" :
                                        self.simple_spectre_signal.emit(buff.copy())   # Отправляем данные простого спектра

                                    case "TOGGLE_TIME_SPECTRE" :
                                        self.time_spectre_signal.emit(buff.copy())     # Отправляем данные часового спектра
                            
                                
                            else:  #  Ошибка CRC    
                                self.error_read_count += 1                                
                                info_dict = {"type": "global_read_error", "inner_type": str(self.error_read_count), "message": "Прилад не відповідає коректно, помилка CRC"}                                
                                if self.gui_info_signal:
                                    self.gui_info_signal.emit(info_dict)                                  
                                    
                        else:   #  Ошибка - неполный пакет                      
                            self.error_read_count += 1                                
                            info_dict = {"type": "global_read_error", "inner_type": str(self.error_read_count), "message": "Прилад не відповідає коректно, прийнято неповний пакет даних"}                                
                            if self.gui_info_signal:
                                self.gui_info_signal.emit(info_dict)                   

                    finally:
                        self.mutex.unlock()
                        self.wait_condition.wakeAll()  # Уведомляем поток записи, что чтение завершено                
                        
                        
                else:     # В порту нет байтов , пауза и проверяем дальше
                    time.sleep(0.05)
                    
        except serial.SerialException as e:
            info_dict = {"type": "read_data_serial_port_error", "message": f"Exception - Ошибка чтения из порта: {str(e)}"}
            self.gui_info_signal.emit(info_dict)

        except Exception as e:
            info_dict = {"type": "read_data_unknown_error", "message": f"Exception - Неизвестная ошибка: {str(e)}"}
            self.gui_info_signal.emit(info_dict) 
                   
        finally:
            self.mutex.unlock()
            self.wait_condition.wakeAll()  # Уведомляем поток записи, что чтение завершено     





   








  
    @pyqtSlot(bytearray)  
    def _paed_data(self, data:bytearray)-> None:
       
        num = struct.unpack('<I', data[5:9])[0]   
        ped = 0
        
        byte_to_check = data[10]
        
        high_sens_detect_failure  = True
        low_sens_detector_failure = True
        result_valid              = True        
        
        if byte_to_check & 0b00000001:   # D0 = 1 - отказ высокочувствительного детектора
            high_sens_detect_failure  = False     

        if byte_to_check & 0b00000010:   # D1 = 1 - отказ низкочувствительного детектора
            low_sens_detector_failure = False  

        if byte_to_check & 0b00000100:   # D2 = 1 - результат невалидный
            result_valid = False 
            
        if byte_to_check & 0b10000000:   # Перерасчет ПЕД 
           ped = num * 0.1        
        else:
           ped = num * 0.01 

        ped = str(ped) + " мкЗв/год" 
 
        info_dict = {
            "type" : "ped", 
            "high_sens_detect_failure": high_sens_detect_failure,
            "low_sens_detector_failure": low_sens_detector_failure,
            "result_valid": result_valid,
            "ped" : ped
        }
        
        self.gui_info_signal.emit(info_dict) #Отправляем сигнал в GUI  

    @pyqtSlot(bytearray)  
    def _ser_num_data(self, data:bytearray)-> None:
       
        high_self = data[8] & 0x0F
        _str = chr(high_self + ord('0'))

        for i in range(7, 4, -1):
            high_self = (data[i] >> 4) & 0x0F       
            low_self = data[i] & 0x0F
            _str += chr(high_self + ord('0')) + chr(low_self + ord('0'))
        
        info_dict = {
            "type" : "ser_num", 
            "serial_number": _str          
        }
        
        self.gui_info_signal.emit(info_dict) #Отправляем сигнал в GUI  

    @pyqtSlot(bytearray)  
    def _rad_intens_data(self, data:bytearray)-> None:
        """
            Функция получает интенсивность излучения (CPS) за 100 мсек        
        """
        
        byte5 = data[5]
        byte6 = data[6]        
        
        Intense = struct.unpack('<H', bytes([byte5, byte6]))[0]        
        
        info_dict = {
            "type" : "intense", 
            "Intense": str(Intense)          
        }
        
        self.gui_info_signal.emit(info_dict) #Отправляем сигнал в GUI  

    @pyqtSlot(bytearray)  
    def _temp_data(self, data:bytearray)-> None:
        temperature = 0.0
        
        l_byte = data[5]  
        m_byte = data[6]  

        sensor_valid = True
        if m_byte & 0b10000000:   
           sensor_valid = False 

        res = l_byte + (m_byte << 8)
        temperature = (res * 2500.0/2048.0-1858.3)/-11.67   

        temperature = round(temperature, 2)             
            
        info_dict = {
            "type" : "temp", 
            "sensor_valid" : sensor_valid,
            "temperature": str(temperature)           
        }
        
        self.gui_info_signal.emit(info_dict) 

    # @pyqtSlot(bytearray) 
    # def _simple_spectre_data(self, data:bytearray)-> None:
    #     current_time = time.time()
    #     if self.previous_simple_spectre_time is not None:
    #         elapsed_time = current_time - self.previous_simple_spectre_time
    #         res = f"Час між прийомами даних : {elapsed_time:.2f} сек"            
    #     else:
    #         res = "Перший виклик, немає даних"
	
    #     self.previous_simple_spectre_time = current_time

    #     size = len(data)
    #     info_dict = {
    #         "type" : "simple_spectre", 
    #         "size" : str(size),
    #         "interval" :  res                   
    #     }
        
    #     self.gui_info_signal.emit(info_dict) 