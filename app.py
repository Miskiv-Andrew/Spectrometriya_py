import sys
from PyQt5 import QtCore, QtGui,QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot, QEvent
from PyQt5.QtWidgets import  QMessageBox, QFileDialog, QApplication
# from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QFont

import SERIAL 
import COMMANDS as COMM 
import simple_spectre_graf as simple_graf 
import time_spectre_graf as time_graf 

from datetime import datetime

import h5py
import numpy as np

import os

COMM.Const.MAX_ERROR

class SimpleGraf(QtWidgets.QWidget, simple_graf.Ui_Form):  # Используем QWidget для немодального окна

    def __init__(self):
        super(SimpleGraf, self).__init__()
        self.setupUi(self)


class TimeGraf(QtWidgets.QWidget, time_graf.Ui_Form):  # Используем QWidget для немодального окна

    def __init__(self):
        super(TimeGraf, self).__init__()
        self.setupUi(self)

class MainApp(QtWidgets.QMainWindow):

    # Создаем сигнал с параметром COMM.Command из DeviceCommands для записи данных в девайс
    send_ser_handler_signal = pyqtSignal(COMM.Command) 

    # Создаем сигнал для передачи времени начала набора простого спектра 
    send_simple_graf_time_signal = pyqtSignal(object) 

    # Создаем сигнал для разрешения-запрещения инструментов простого графика спектра
    send_simple_graf_instrument_signal = pyqtSignal(bool)

    # Создаем сигнал для передачи времени начала набора часового спектра 
    send_time_graf_time_signal = pyqtSignal(object) 

    # Создаем сигнал для разрешения-запрещения инструментов часового графика спектра
    send_time_graf_instrument_signal = pyqtSignal(bool)

    # Создаем сигнал для разрешения-запрещения инструментов загрузки из файла часового графика спектра
    send_time_graf_load_file_signal = pyqtSignal(bool)

    # Создаем сигнал для передачи данных из файла часового графика спектра в  class TimeGraf
    send_time_graf_data_file_signal = pyqtSignal(object)

    # Создаем сигнал без параметров для старта поиска порта девайса
    send_search_dev_signal = pyqtSignal()

    # Создаем сигнал без параметров для старта потоков методов записи и чтения девайса
    send_start_dev_threads = pyqtSignal()   

    # Создаем сигнал без параметров для очистки данных обычного спектра
    send_clear_1_spectre = pyqtSignal()   

    # Создаем сигнал без параметров для очистки данных часового спектра
    send_clear_2_spectre = pyqtSignal()  

    def __init__(self):        
        super(MainApp, self).__init__()

        # Загружаем интерфейс из файла .ui
        uic.loadUi('main_window.ui', self)      

        # Создаем экземпляр SerialPortHandler
        self.serial_handler = SERIAL.SerialPortHandler()    

        # Создаем атрибут начала времени набора спектра
        self.start_spectre_time = None  

        # Подключаем сигнал gui_info_signal класса SerialPortHandler к методу port_info_process 
        self.serial_handler.gui_info_signal.connect(self.port_info_process)

        # Подключаем сигнал старта поиска порта девайса к слоту find_device_port SerialPortHandler
        self.send_search_dev_signal.connect(self.serial_handler.find_device_port) 



        # Подключаем кнопку поиска порта девайса
        self.pushButton_search_dev.clicked.connect(self.handle_button_search_dev) 

        # # Подключаем сигнал записи данных в девайс к слоту write_data SerialPortHandler  
        # self.send_ser_handler_signal.connect(self.serial_handler.write_data)    
        # Подключаем сигнал записи данных в девайс к слоту запуска потока handle_write_signal SerialPortHandler 
        self.send_ser_handler_signal.connect(self.serial_handler.handle_write_signal) 

        # Подключаем кнопку получения серийного номера девайса
        self.pushButton_ser_num_dev.clicked.connect(self.handle_button_ser_num_dev)   
        # Подключаем кнопку получения температуры девайса  
        self.pushButton_temp_dev.clicked.connect(self.handle_button_temp_dev)  
        # Подключаем кнопку получения интенсивности за 100 мсек
        self.pushButton_intence.clicked.connect(self.handle_button_intence_dev) 
        # Подключаем кнопку получения ПАЕД
        self.pushButton_paed.clicked.connect(self.handle_button_paed_dev) 
        # Подключаем кнопку старта-остановки простого спектра
        self.pushButton_start_1_spectre.clicked.connect(self.handle_button_start_1_spectre)  

        # Подключаем кнопку очистки простого спектра
        self.pushButton_clear_1_spectre.clicked.connect(self.handle_button_clear_1_spectre)  
      
        # Подключаем кнопку старта-остановки часового спектра
        self.pushButton_9.clicked.connect(self.handle_button_search_file_2_spectre) 

        # Подключаем кнопку старта-остановки часового спектра
        self.pushButton_start_2_spectre.clicked.connect(self.handle_button_start_2_spectre) 

         # Подключаем кнопку очистки простого спектра
        self.pushButton_clear_2_spectre.clicked.connect(self.handle_button_clear_2_spectre)          


        self.action_1.triggered.connect(self.test_action)

        # Атрибут окна простого спектра
        self.s_graf =  SimpleGraf()  

        # Передача времени начала набора спектра
        self.send_simple_graf_time_signal.connect(self.s_graf.set_start_spectre_time)

        # Создаем сигнал для разрешения-запрещения инструментов простого графика спектра
        self.send_simple_graf_instrument_signal.connect(self.s_graf.set_instrument_spectre)

        # Подключаем сигнал очистки простого спектра к слоту 
        self.send_clear_1_spectre.connect(self.s_graf.clear_spectre) 

        self.s_graf.gui_info_signal.connect(self.s_graf_info_process)


        # # Атрибут окна часового спектра 
        self.t_graf =  TimeGraf()         

        # Подключаем сигнал gui_info_signal класса SerialPortHandler к методу port_info_process 
        self.t_graf.gui_info_signal.connect(self.port_info_process)   

        # Передача времени начала набора часового спектра
        self.send_time_graf_time_signal.connect(self.t_graf.set_start_spectre_time)

        # Подключаем сигнал для разрешения-запрещения инструментов часового графика спектра
        self.send_time_graf_instrument_signal.connect(self.t_graf.set_instrument_spectre)

        # Подключаем сигнал для разрешения-запрещения инструментов загруз-ки из файла часового графика спектра
        self.send_time_graf_load_file_signal.connect(self.t_graf.set_instrument_load_file_spectre)

        # Подключаем сигнал очистки часового спектра к слоту 
        self.send_clear_2_spectre.connect(self.t_graf.clear_spectre) 

        # Подключаем сигнал очистки часового спектра к слоту 
        self.send_time_graf_data_file_signal.connect(self.t_graf.load_data_from_file) 
        
        # Получаем объект экрана
        screen = QApplication.primaryScreen()

         # Получаем геометрию экрана (размер экрана и его расположение)
        screen_geometry = screen.geometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()       
        self.screen_dpi = screen.logicalDotsPerInch()   # Получаем DPI экрана (плотность пикселей)
       

        _width = self.screen_width - 10
        _top = int(self.screen_height/3.3)       

        # Задание размеров окна (ширина, высота) 
        self.resize(_width , _top)
        # # Задание положения окна на экране (X, Y) 
        self.move(5, 5)       

        # Соединяем передачу данных простого спектра из класса SERIAL в класс simple_spectre_graf
        self.serial_handler.simple_spectre_signal.connect(self.s_graf.simple_spectre_slot)  

        # Соединяем передачу данных простого спектра из класса SERIAL в класс simple_spectre_graf
        self.serial_handler.time_spectre_signal.connect(self.t_graf.time_spectre_slot) 

        # Атрибут данных полученных из файла спектра
        self.all_file_data = [] 


        self.buttons_enable(False)   


        font = QFont()
        font.setFamily('Arial')         # Устанавливаем семейство шрифта
        font.setPointSize(10)           # Устанавливаем размер шрифта
        font.setBold(True)              # Устанавливаем полужирный шрифт
        font.setItalic(False)           # Отключаем курсив
        font.setUnderline(False)        # Отключаем подчеркивание       
        self.textEdit.setFont(font)
 
        font.setFamily('Arial')          # Устанавливаем семейство шрифта
        font.setPointSize(10)            # Устанавливаем размер шрифта
        font.setBold(False)              # Устанавливаем полужирный шрифт
        font.setItalic(True)             # Отключаем курсив
        font.setUnderline(False)         # Отключаем подчеркивание       
        self.textEdit_2.setFont(font)
       

        self.send_time_graf_instrument_signal.emit(False)

        

    def test_action(self):      
        self.lineEdit_ser_num.clear()
        self.lineEdit_temp.clear()
        self.lineEdit_intence.clear()
        self.lineEdit_paed.clear()

    def buttons_enable(self, flag: bool)-> None:
        self.pushButton_ser_num_dev.setEnabled(flag)
        self.pushButton_temp_dev.setEnabled(flag)  
        self.pushButton_intence.setEnabled(flag)   
        self.pushButton_paed.setEnabled(flag)   
        self.pushButton_start_1_spectre.setEnabled(flag)   
        self.pushButton_clear_1_spectre.setEnabled(flag)   
        self.pushButton_start_2_spectre.setEnabled(flag)  
        self.pushButton_clear_2_spectre.setEnabled(flag)
        

                
    
    def open_simple_graf(self): 
        _width = self.screen_width - 10
        _top = int(self.screen_height/3.7)
        _under = self.screen_height - _top       
        self.s_graf.setGeometry(5, int(_top * 1.4), _width, int(_under * 0.78))
        self.s_graf.show()  # Открыть окно простого графика спектра


       

    def open_time_graf(self): 
        _width = self.screen_width - 10
        _top = int(self.screen_height/3.7)
        _under = self.screen_height - _top       
        self.t_graf.setGeometry(5, int(_top * 1.4), _width, int(_under * 0.78))
        self.t_graf.show()  # Открыть окно простого графика спектра


    def event(self, event):
        # Перехватываем событие закрытия
        if event.type() == QEvent.Close:
            return self.handle_close_event(event)
        return super().event(event)   
    

    def handle_close_event(self, event):
        # Диалог подтверждения
        reply = QMessageBox.question(
            self,
            "Підтвердження виходу",
            "Ви впевнені, що хочете завершити роботу?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No  # Кнопка по умолчанию
        )

        if reply == QMessageBox.Yes:
            # Обрабатываем ситуацию 
            flag = self.serial_handler.stop_reader_thread()
            if flag:
                event.accept()  # Порт закрыт, поток чтения остановлен, завершаем работу
                self.s_graf.close()
                self.t_graf.close()
                return True
            else:
                event.ignore()  # Что-то пошло не так, не завершаем работу
                return True 

        else: # Не выходим, возвращаемся в приложение            
            event.ignore()  
            return True       
    
    @pyqtSlot()
    def handle_button_search_dev(self):
        self.lineEdit_search.clear()
        self.send_search_dev_signal.emit()


    @pyqtSlot()
    def handle_button_ser_num_dev(self):
        try: 
            command = COMM.DeviceCommands.COMMAND_SER_NUM 
            self.send_ser_handler_signal.emit(command) 
        
        except Exception as e: 
            self.textEdit.clear()
            self.textEdit.setText(f"Ошибка при отправке запроса серийного номера : {e}")

    @pyqtSlot()
    def handle_button_temp_dev(self):
        try: 
            command = COMM.DeviceCommands.COMMAND_TEMP 
            self.send_ser_handler_signal.emit(command) 
        
        except Exception as e: 
            self.textEdit.clear()
            self.textEdit.setText(f"Ошибка при отправке запроса температуры девайса : {e}")

    @pyqtSlot()
    def handle_button_intence_dev(self):
        try: 
            command = COMM.DeviceCommands.COMMAND_RAD_INTENS 
            self.send_ser_handler_signal.emit(command) 
        
        except Exception as e:
            self.textEdit.clear() 
            self.textEdit.setText(f"Ошибка при отправке запроса интенсивности: {e}")   

    @pyqtSlot()
    def handle_button_paed_dev(self):
        try: 
            command = COMM.DeviceCommands.COMMAND_RAD_DOSE 
            self.send_ser_handler_signal.emit(command) 
        
        except Exception as e:   
            self.textEdit.clear()          
            self.textEdit.setText(f"Ошибка при отправке запроса ПАЕД: {e}")  


    @pyqtSlot()
    def handle_button_clear_1_spectre(self):
        self.send_clear_1_spectre.emit()
        self.textEdit.clear()
        self.textEdit_2.clear()
        self.start_spectre_time = None


    @pyqtSlot()
    def handle_button_clear_2_spectre(self):
        self.send_clear_2_spectre.emit()
        self.textEdit.clear()
        self.textEdit_2.clear()
        self.start_spectre_time = None


    @pyqtSlot()
    def handle_button_search_file_2_spectre(self):
        try:    
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly

            # Установка фильтра файлов       
            filter = "TSP Files (*.tsp);;All Files (*)"
            file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", filter, options=options)

            if not file_name: # Проверка, был ли выбран файл 
                return None
            
            # Получаем размер файла в байтах
            file_size_bytes = os.path.getsize(file_name)
            # Преобразуем размер файла в мегабайты (1 МБ = 1 048 576 байт)
            file_size_mb = file_size_bytes / (1024 * 1024)
            file_size_mb = round(file_size_mb, 2)
            self.textEdit_3.append(f"Розмір вибраного файлу: {str(file_size_mb)} мБайт")            
            
            self.all_file_data = [] 

            with h5py.File(file_name, 'r') as file:  # Открытие файла для чтения   
                for group_name in file.keys():  # Итерация по всем группам в файле
                    group = file[group_name]
                    group_data = []
                    for dataset_name in group.keys():  # Итерация по всем датасетам в группе
                        dataset = group[dataset_name]
                        data = np.array(dataset)
                        group_data.append((data[0], data[1]))  # Сохранение данных в виде кортежей
                    self.all_file_data.append(group_data)     # Сохранение данных группы


            if not self.all_file_data:
                self.textEdit_3.setText("У вибраному файлі немає даних")
                return None
            
            self.textEdit_3.append(f"Кількість груп у файлі: {str(len(self.all_file_data))}") 

                       
            self.open_time_graf()
            
            self.send_time_graf_data_file_signal.emit(self.all_file_data)
            



        
        except Exception as e:            
            self.textEdit_3.setText(f"Ошибка при чтении данных из файла: {str(e)}")
            return None
       

    @pyqtSlot()
    def handle_button_start_1_spectre(self):        
        command = None       
        enable = True    

        if self.start_spectre_time == None:
            current_time = datetime.now()                                # Получаем  время начала набора спектра
            self.start_spectre_time = current_time.strftime("%H:%M:%S") + "\n"

        
        if self.pushButton_start_1_spectre.text() == "Стандартний спектр - почати набір": 
            self.pushButton_start_1_spectre.setText("Стандартний спектр - зупинити набір")
            command = COMM.DeviceCommands.COMMAND_TOGGLE_SIMPLE_SPECTRE           
            enable = False
            self.open_simple_graf()    
            self.t_graf.close()    
            self.pushButton_clear_1_spectre.setEnabled(False)   
            self.pushButton_start_2_spectre.setEnabled(False)  
            self.pushButton_clear_2_spectre.setEnabled(False)         
            self.pushButton_search_dev.setEnabled(False)
            self.pushButton_ser_num_dev.setEnabled(False)
            self.pushButton_temp_dev.setEnabled(False)
            self.pushButton_intence.setEnabled(False)
            self.pushButton_paed.setEnabled(False)
            self.textEdit.clear()
            self.textEdit_2.clear()
            
        else: 
            self.pushButton_start_1_spectre.setText("Стандартний спектр - почати набір")
            command = COMM.DeviceCommands.COMMAND_RAD_DOSE            
            self.pushButton_clear_1_spectre.setEnabled(True)   
            self.pushButton_start_2_spectre.setEnabled(True)  
            self.pushButton_clear_2_spectre.setEnabled(True)             
            self.pushButton_search_dev.setEnabled(True)
            self.pushButton_ser_num_dev.setEnabled(True)
            self.pushButton_temp_dev.setEnabled(True)
            self.pushButton_intence.setEnabled(True)
            self.pushButton_paed.setEnabled(True)          
        
        try:   
            # Отправляем сигнал записи данных в порт           
            self.send_ser_handler_signal.emit(command) 

            # Отправляем сигналы времени и интерфейса            
            self.send_simple_graf_time_signal.emit(self.start_spectre_time)
            self.send_simple_graf_instrument_signal.emit(enable)

        except Exception as e:   
            self.textEdit.clear()          
            self.textEdit.setText(f"Ошибка при отправке запроса старта спектра: {e}")  


    @pyqtSlot()
    def handle_button_start_2_spectre(self):                              
        command = None  
        enable = True    

        if self.start_spectre_time == None:
            current_time = datetime.now()                                # Получаем  время начала набора спектра
            self.start_spectre_time = current_time.strftime("%H:%M:%S") + "\n"

        
        if self.pushButton_start_2_spectre.text() == "Часовий спектр - почати набір": 
            self.pushButton_start_2_spectre.setText("Часовий спектр - зупинити набір")
            command = COMM.DeviceCommands.COMMAND_TOGGLE_TIME_SPECTRE           
            enable = False 
            self.open_time_graf()  
            self.s_graf.close() 

            self.pushButton_clear_1_spectre.setEnabled(False)   
            self.pushButton_start_1_spectre.setEnabled(False)  
            self.pushButton_clear_2_spectre.setEnabled(False)           
            self.pushButton_search_dev.setEnabled(False)
            self.pushButton_ser_num_dev.setEnabled(False)
            self.pushButton_temp_dev.setEnabled(False)
            self.pushButton_intence.setEnabled(False)
            self.pushButton_paed.setEnabled(False)
            self.textEdit.clear()
            self.textEdit_2.clear()
            
        else: 
            self.pushButton_start_2_spectre.setText("Часовий спектр - почати набір")
            command = COMM.DeviceCommands.COMMAND_RAD_DOSE 

            self.pushButton_clear_1_spectre.setEnabled(True)   
            self.pushButton_start_1_spectre.setEnabled(True)  
            self.pushButton_clear_2_spectre.setEnabled(True)
            self.pushButton_search_dev.setEnabled(True)
            self.pushButton_ser_num_dev.setEnabled(True)
            self.pushButton_temp_dev.setEnabled(True)
            self.pushButton_intence.setEnabled(True)
            self.pushButton_paed.setEnabled(True)
        
        try:              
            # Отправляем сигнал записи данных в порт
            self.send_ser_handler_signal.emit(command) 

            # Отправляем сигналы времени и интерфейса  
            self.send_time_graf_time_signal.emit(self.start_spectre_time)
            self.send_time_graf_instrument_signal.emit(enable)

        except Exception as e:   
            self.textEdit.clear()          
            self.textEdit.setText(f"Ошибка при отправке запроса старта спектра: {e}")  


    @pyqtSlot(object)
    def s_graf_info_process(self, _dict):       
        self.textEdit_2.clear()
        self.textEdit_2.setText(_dict.get("right"))

        text = self.textEdit.toPlainText()
        text = text.split('\n')  
        if len(text) > 10:
            self.textEdit.clear()

        self.textEdit.append(_dict.get("left"))



    @pyqtSlot(object)
    def port_info_process(self, _dict):       
        
        if not "type" in _dict:
            self.textEdit.clear()
            self.textEdit.setText("Ошибка ключа 'type' словаря")
            return None
        
        value = _dict.get("type")       

        match value:          
            case "search_port":  
                inner_value = _dict.get("inner_type")       
                if  inner_value ==  "dev_no_search": 
                    self.textEdit.clear() 
                    self.textEdit.append(_dict.get("message")) 
                    self.pushButton_9.setEnabled(True)    
                    self.send_time_graf_load_file_signal.emit(True)  
                    return None          

                elif inner_value ==  "dev_search":  
                    _str = _dict.get("port")
                    self.lineEdit_search.setText(_str)
                    self.send_start_dev_threads.emit()
                    self.buttons_enable(True)   
                    self.pushButton_9.setEnabled(False) 
                    self.send_time_graf_load_file_signal.emit(False)  
                    return None      
           
            case "ped":
                _str = ""
                high  = _dict.get("high_sens_detect_failure")
                low   = _dict.get("low_sens_detector_failure")
                valid = _dict.get("result_valid")
                ped   = _dict.get("ped")

                _str += "Високочутливий детектор справний\n" if high else "Високочутливий детектор несправний\n"
                _str += "Низькочутливий детектор справний\n" if low else "Низькочутливий детектор несправний\n"
                _str += "Результат ПАЕД валідний\n" if valid else "Результат ПАЕД невалідний\n"
                self.textEdit_3.clear()
                self.textEdit_3.append(_str)              
                self.lineEdit_paed.setText(ped)                

            case "ser_num":               
                self.lineEdit_ser_num.setText(_dict.get("serial_number"))    

            case "intense":
                self.lineEdit_intence.setText(_dict.get("Intense") )
            
            case "temp":
                _str = "Сенсор температури справний\n" if _dict.get("sensor_valid") else "Сенсор температури несправний\n"
                self.textEdit_3.clear()
                self.textEdit_3.append(_str)
                _str = _dict.get("temperature") + "°C"
                self.lineEdit_temp.setText(_str) 

            case "simple_spectre":
                _str = "Прийнято простий спектр\n"
                _str += "Розмір пакету " + _dict.get("size") + "\n"
                _str += "Час між пакетами " + _dict.get("interval") + "\n----------------------\n"
                self.textEdit.clear()
                self.textEdit.append(_str) 

            case "simple_spectre_not_full_data":
                _str =   "Неповний простий спектр\n"
                _str +=  "Розмір пакету " + _dict.get("received_data") + "\n"  
                self.textEdit.clear()
                self.textEdit.append(_str) 

            case "global_write_error":
                _str =  _dict.get("message") + "\n"
                self.textEdit.clear()
                self.textEdit.append(_str)         


            case "read_data_serial_port_error":  
                _str =  _dict.get("message") + "\n"
                self.textEdit.clear()
                self.textEdit.append(_str)  

            case "read_data_unknown_error": 
                _str =  _dict.get("message") + "\n"
                self.textEdit.clear()
                self.textEdit.append(_str) 
              
            case "global_read_error": 
                _str =  _dict.get("message") + "\n"
                _str += "Кількість помилок читання " + _dict.get("inner_type") + "\n"
                self.textEdit.clear()
                self.textEdit.append(_str) 
               
            case "time_spectre_global_write_error": 
                _str =  _dict.get("message") + "\n"
                self.textEdit.clear()
                self.textEdit.append(_str) 

            case "time_spectre_params": 

                text = self.textEdit.toPlainText()
                text = text.split('\n')  
                if len(text) > 10:
                    self.textEdit.clear()
                self.textEdit.append(_dict.get("param_edit"))

                self.textEdit_2.setText(_dict.get("data_edit"))   

            case "global_write_file_error":
                _str =  _dict.get("message") + "\n"
                self.textEdit.clear()
                self.textEdit.append(_str)  

            




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)    
    window = MainApp()
    window.show()
    # window.showFullScreen() 
    # window.showMaximized()  

    sys.exit(app.exec_()) 