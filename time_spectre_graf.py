import time
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot, QThread, QTimer
# from PyQt5.QtGui import QFont


from PyQt5.QtWidgets import QFileDialog, QMessageBox

import matplotlib.pyplot as plt
from  matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from  matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# from  matplotlib.gridspec import GridSpec
# from  matplotlib.ticker   import NullLocator, LinearLocator, MultipleLocator, IndexLocator, FixedLocator, MaxNLocator
from  matplotlib.ticker   import ScalarFormatter

from matplotlib.lines import Line2D

import numpy as np

import COMMANDS as COMM 

import h5py
import os

import struct

import threading  

import COMMANDS as COMM 


class Ui_Form(object):

    # сигнал передачи данных в GUI (тип данных - словарь)   
    gui_info_signal = pyqtSignal(object) 

    # Создаем сигнал для записи данных спектра в файл в отдельном потоке
    write_file_signal = pyqtSignal(object)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(896, 829)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.gridLayout_4 = QtWidgets.QGridLayout()

        self.gridLayout_4.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)

        self.gridLayout_4.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_4.setSpacing(5)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.widget_Diff_Spectre = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_Diff_Spectre.sizePolicy().hasHeightForWidth())
        self.widget_Diff_Spectre.setSizePolicy(sizePolicy)
        self.widget_Diff_Spectre.setObjectName("widget_Diff_Spectre")
        self.gridLayout_4.addWidget(self.widget_Diff_Spectre, 0, 1, 1, 1)
        self.widget_Spectre = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_Spectre.sizePolicy().hasHeightForWidth())
        self.widget_Spectre.setSizePolicy(sizePolicy)
        self.widget_Spectre.setObjectName("widget_Spectre")
        self.gridLayout_4.addWidget(self.widget_Spectre, 0, 0, 1, 1)
        self.horizontalLayout_3.addLayout(self.gridLayout_4)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem, 0, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_5)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()

        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)

        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()

        self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)

        self.gridLayout_3.setObjectName("gridLayout_3")
        self.textEdit_spectre = QtWidgets.QTextEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_spectre.sizePolicy().hasHeightForWidth())
        self.textEdit_spectre.setSizePolicy(sizePolicy)
        self.textEdit_spectre.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.textEdit_spectre.setObjectName("textEdit_spectre")
        self.gridLayout_3.addWidget(self.textEdit_spectre, 0, 0, 2, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setObjectName("checkBox")        
        self.verticalLayout.addWidget(self.checkBox)
        self.comboBox = QtWidgets.QComboBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout.addWidget(self.comboBox)
        self.pushButton = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 1, 2, 1)
        self.horizontalLayout_4.addLayout(self.gridLayout_3)
        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
         

        # Массив numpy размером 12,000,000 из расчета 1 мин на экране
        self.global_buff = np.zeros(COMM.Const.GLOB_BUFF_SIZE,  dtype = np.int16) 

        # Временной параметр для добавления относительного времени
        self.time_parameter = 0     

        # Числовой параметр для очищения
        self.iteration = -1

        
        # Создаем Figure и FigureCanvas
        self.figure_1 = plt.figure()          
        self.canvas_1 = FigureCanvas(self.figure_1)
        # Встраиваем canvas в widget_Plot
        layout_1 = QtWidgets.QVBoxLayout(self.widget_Spectre)   #widget_Diff_Spectre
        layout_1.addWidget(self.canvas_1)
        # Добавляем панель инструментов для навигации по графику
        self.navigation_toolbar_1 = NavigationToolbar(self.canvas_1, Form) 
        layout_1.addWidget(self.navigation_toolbar_1)

        self.ax_1 = self.figure_1.add_subplot(111)
        x_ticks = np.arange(0, 1100000, 100000)
        self.ax_1.set_xticks(x_ticks)    
        # Установите ScalarFormatter для оси X
        formatter = ScalarFormatter(useOffset=False)
        formatter.set_scientific(False)  # Отключить научную запись
        self.ax_1.xaxis.set_major_formatter(formatter)


        # y_ticks = np.arange(0, 1100, 100)
        # self.ax_1.set_yticks(y_ticks)
        # self.ax_1.set_ylim(0, 1100)

        y_ticks = np.arange(0, 1200, 100)
        self.ax_1.set_yticks(y_ticks)
        self.ax_1.set_ylim(0, 1200)

        # Настройка осей
        self.ax_1.spines['left'].set_position('zero')  # Ось Y начинается с 0
        self.ax_1.spines['bottom'].set_position('zero')  # Ось X начинается с 0
        self.ax_1.spines['right'].set_color('none')  # Убираем правую ось
        self.ax_1.spines['top'].set_color('none')  # Убираем верхнюю ось
        # Установка подписей для осей
        self.ax_1.set_xlabel("Час  (мксек)", fontsize = 8)
        self.ax_1.set_ylabel("Канал імпульса", fontsize = 8)
        # Дополнительно можно настроить стиль текста
        self.ax_1.xaxis.label.set_style("italic")  # Курсив для подписи оси X
        self.ax_1.yaxis.label.set_style("italic")  # Курсив для подписи оси Y
        # Добавляем сетку
        self.ax_1.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)
        # Сетка будет рисоваться ниже графика
        self.ax_1.set_axisbelow(True)
        # Добавляем отступы через фигуру
        self.figure_1.subplots_adjust(left = 0.08, right = 0.95, top = 0.95, bottom = 0.2)

        # Создание пустого Line2D 
        self.line = Line2D([], [], linestyle='None', marker='o', color='blue', markersize = COMM.Const.DOT_SIZE) 
        self.ax_1.add_line(self.line)

        # Создаем Figure и FigureCanvas
        self.figure_2 = plt.figure()          
        self.canvas_2 = FigureCanvas(self.figure_2)        
        # # Встраиваем canvas в widget_Plot
        layout_2 = QtWidgets.QVBoxLayout(self.widget_Diff_Spectre)   #widget_Diff_Spectre
        layout_2.addWidget(self.canvas_2)
        #  # Добавляем панель инструментов для навигации по графику
        self.navigation_toolbar_2 = NavigationToolbar(self.canvas_2, Form) 
        layout_2.addWidget(self.navigation_toolbar_2)   

        self.start_spectre_time = None
        self.checkBox.stateChanged.connect(self.on_checkBox_file_search)   

        # Полный путь к файлу загрузки данных
        self.file_path = None

        # Счетчик групп записей в файл
        self.group_file_index = 0

        # Атрибут потока записи данных
        self.write_file_thread  = None     


        # Соединяем сигнал с методом запуска потока записи в файл
        self.write_file_signal.connect(self.write_file_thread_start)       


        # Атрибут данных полученных из файла спектра
        self.all_file_data = [] 

        # Атрибут-счетчик загруженных групп из файла
        self.count_load_groups = 0

        # Атрибут количества загруженных групп из файла
        self.max_load_groups = 0

        self.data_file_timer = QTimer() 
        
        self.data_file_timer.timeout.connect(self.proc_data_file_timer)


        self.comboBox.activated.connect(self.handle_combobox_activated)

        self.pushButton.clicked.connect(self.handle_button_start_timer)  

        self.pushButton_3.clicked.connect(self.handle_button_one_group)  

        self.pushButton_4.clicked.connect(self.handle_button_all_groups)  

        self.pushButton.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)



    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Параметри та графіки часового спектру"))
        self.checkBox.setText(_translate("Form", "     Завантажувати дані у файл"))
        self.comboBox.setItemText(0, _translate("Form", "Режим таймера"))
        self.comboBox.setItemText(1, _translate("Form", "Покроковий режим"))
        self.comboBox.setItemText(2, _translate("Form", "Повне завантаження"))  
        self.comboBox.addItem("Очистити завантаження")

        self.pushButton.setText(_translate("Form", "Включити таймер"))
        self.pushButton_3.setText(_translate("Form", "Зробити крок завантаження"))
        self.pushButton_4.setText(_translate("Form", "Зробити повне завантаження"))


    def handle_button_start_timer(self):
        if self.pushButton.text() == "Включити таймер": 
            self.pushButton.setText("Зупинити таймер")
            self.data_file_timer.start(COMM.Const.LOAD_SPECTRE_TIMER_INTERVAL)
            return None

        self.pushButton.setText("Включити таймер")
        self.data_file_timer.stop()


    def handle_button_one_group(self):
        self.work_file_spectrum_data(False)


    def handle_button_all_groups(self):
        self.work_file_spectrum_data(True)
        
    

    def handle_combobox_activated(self, index): 
        self.pushButton.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        match index:
            case 0:  # Таймер
                self.pushButton.setEnabled(True)
            case 1:  # Ручной режим
                self.pushButton_3.setEnabled(True)
            case 2:  # Полная загрузка
                self.pushButton_4.setEnabled(True)
            case 3:  # Очистка после загрузки
                # Проводим предварительную очистку 
                self.clear_spectre()
                self.count_load_groups = 0                
            case _:
                return None
            
        


    def process_render_func(self, result: np.ndarray):
        """
        Параметры:
        - result (np.ndarray): numpy массив с данными, имеет вид: 
        result = np.zeros(num_entries, dtype=[('channel', np.uint16), ('time', np.uint32)]).    
        Метод предназначен для обработки данных часовго cпектра, полученного из 
        файла и их визуализации
        """ 
        try:
            # Фильтруем массив
            mask = (result['channel'] != 0) & (result['time'] < len(self.global_buff))
            filtered = result[mask]

            # Массовая запись в глобальный буфер
            self.global_buff[filtered['time']] = filtered['channel'].astype(np.int16)

            # Получаем numpy массивы для отрисовки             
            indices = result['channel'] 
            values  = result['time']       
        
            # Добавляем новые точки на график 
            self.line.set_xdata(np.append(self.line.get_xdata(), values)) 
            self.line.set_ydata(np.append(self.line.get_ydata(), indices)) 
            self.ax_1.relim() 
            self.ax_1.autoscale_view()
            
            self.canvas_1.draw()
            
            # Здесь будет дальнейшая обработка

        except Exception as e:
            self.textEdit_spectre.append(f"Виник exception при відмальовці даних, {str(e)}" + "\n")


    def fill_numpy_array_from_group_data(self, param = False):
        """
        Метод обрабатывает данные из файла часового спектра,
        возвращает numpy массив np.zeros(all_entries, dtype=[('channel', np.uint16), ('time', np.uint32)]) для сохранения в self.global_buff  и отрисовки
        При param == False метод отдает очередной кадр
        При param == True метод отдает все полученные данные
        
        """ 
        if param:   # Отдаем сразу все данные           
            all_entries = sum(len(group_data) for group_data in self.all_file_data)
            result = np.zeros(all_entries, dtype=[('channel', np.uint16), ('time', np.uint32)])

            index = 0
            for group_data in self.all_file_data:
                for channel, time in group_data:
                    result[index]['channel'] = channel
                    result[index]['time'] = time
                    index += 1

            
            self.count_load_groups = self.max_load_groups
            self.textEdit_spectre.append(f"Дані завантажені повністю, {str(len(self.all_file_data))} кадрів")
            self.pushButton.setEnabled(False)
            self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            return result
        
        else: # Отдаем очередной кадр
            if self.count_load_groups >= self.max_load_groups:
                return np.zeros(7, dtype=[('channel', np.uint16), ('time', np.uint32)])

            group_data = self.all_file_data[self.count_load_groups]
            num_entries = len(group_data)
            result = np.zeros(num_entries, dtype=[('channel', np.uint16), ('time', np.uint32)])

            for i, (channel, time) in enumerate(group_data):
                result[i]['channel'] = channel
                result[i]['time'] = time

            self.textEdit_spectre.setText(f"Завантажено {str(self.count_load_groups + 1)} кадр")

            self.count_load_groups += 1
            return result

    def work_file_spectrum_data(self, param : bool):    
        arr = self.fill_numpy_array_from_group_data(param)
        nonzero_count = np.count_nonzero(arr['channel'])
        if not nonzero_count:     
            self.textEdit_spectre.append("Дані завантажені повністю")
            self.pushButton.setEnabled(False)
            self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            return None
            
        self.process_render_func(arr)

    @pyqtSlot()
    def proc_data_file_timer(self):
        if self.count_load_groups >= self.max_load_groups:
            self.data_file_timer.stop()
            self.textEdit_spectre.append("Дані завантажені повністю")
            self.pushButton.setEnabled(False)
            self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            return None
            
        self.work_file_spectrum_data(False)


    


    @pyqtSlot(object)
    def write_file_thread_start(self, buffer):
        try:           
            self.write_file_thread = threading.Thread(target = self.load_data_to_file, args = (buffer, ))
            self.write_file_thread.start()

        except Exception as e:
            self.write_file_thread = None
            info_dict = {"type": "global_write_file_error", "message": f"Виник exception у потоку запису даних спектру у файл , {str(e)}"}
            if self.gui_info_signal: 
                self.gui_info_signal.emit(info_dict) 
    
    @pyqtSlot(object)  
    def set_start_spectre_time(self, _time):
        self.start_spectre_time = _time

    @pyqtSlot(bool)
    def set_instrument_spectre(self, flag):    
        self.checkBox.setEnabled(flag)
        
    @pyqtSlot(bool)
    def set_instrument_load_file_spectre(self, flag): 
        self.comboBox.setEnabled(flag)
        self.pushButton.setEnabled(flag)
        self.pushButton_3.setEnabled(flag)
        self.pushButton_4.setEnabled(flag) 


    def on_checkBox_file_search(self, state):    
        try:
            if state == QtCore.Qt.Unchecked:                
                self.file_path = None
                return None

            _options = QFileDialog.Options()
            _options |= QFileDialog.ReadOnly

            file_name, _ = QFileDialog.getSaveFileName(self, "Create .tsp file", "", "TSP Files (*.tsp);;All Files (*)", options = _options)

            if file_name:
                self.file_path = file_name

                if os.path.exists(self.file_path):
                    reply = QMessageBox.question(
                        self, 'Файл вже існує',
                        "Файл вже існує. Замінити файл? Усі дані буде втрачено.",
                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                    )

                    if reply == QMessageBox.No:
                        self.file_path = None
                        return None

                # Открытие или создание файла HDF5
                with h5py.File(self.file_path, 'w') as file:
                    # Отображение информационного сообщения
                    QMessageBox.information(self, "Файл створено", f"Файл створено, запис даних буде відбуватись в нього:\n {self.file_path}")
                    # Здесь можно добавить любые начальные данные, если нужно

                    # Очищаем все данные перед началом записи
                    self.clear_spectre()

                    # Сбрасываем счетчик групп записей в файл
                    self.group_file_index = 0



            else:
                self.file_path = None
                return None

        except Exception as e:
            print(f"Error: {e}")
            self.file_path = None


    @pyqtSlot(object)   
    def load_data_from_file(self, data_list):
        # Записываем данные файла в атрибут класса all_file_data
        self.all_file_data = data_list        
        
        # Проводим предварительную очистку 
        self.clear_spectre()
        self.count_load_groups = 0

        # Записываем макс. число кадров из файла 
        self.max_load_groups = len(self.all_file_data)

        # Проверяем на наличие информации в файле
        if not self.max_load_groups:
            self.textEdit_spectre.append(" У файлі відсутні дані\n")
            return None

        self.textEdit_spectre.append("Прийнято " + str(self.max_load_groups) + " кадрів даних\nВиберіть режим роботи з даними файлу")
        self.pushButton.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)


    @pyqtSlot()
    def clear_spectre(self):

        self.textEdit_spectre.clear()

        # Очищаем глобальный массив часового спектра
        self.global_buff = np.zeros(COMM.Const.GLOB_BUFF_SIZE,  dtype = np.int16)                
        
        # Очищаем предыдущие графики (если есть)
        self.ax_1.clear()
        self.canvas_1.draw()   


        # self.ax_1 = self.figure_1.add_subplot(111)
        x_ticks = np.arange(0, 1100000, 100000)
        self.ax_1.set_xticks(x_ticks)    
        # # Установите ScalarFormatter для оси X
        formatter = ScalarFormatter(useOffset=False)
        formatter.set_scientific(False)  # Отключить научную запись
        self.ax_1.xaxis.set_major_formatter(formatter)
        y_ticks = np.arange(0, 1200, 100)
        self.ax_1.set_yticks(y_ticks)
        self.ax_1.set_ylim(0, 1200)
        # # Настройка осей
        self.ax_1.spines['left'].set_position('zero')  # Ось Y начинается с 0
        self.ax_1.spines['bottom'].set_position('zero')  # Ось X начинается с 0
        self.ax_1.spines['right'].set_color('none')  # Убираем правую ось
        self.ax_1.spines['top'].set_color('none')  # Убираем верхнюю ось
        # Установка подписей для осей
        self.ax_1.set_xlabel("Час  (мксек)", fontsize = 8)
        self.ax_1.set_ylabel("Канал імпульса", fontsize = 8)
        # # Дополнительно можно настроить стиль текста
        self.ax_1.xaxis.label.set_style("italic")  # Курсив для подписи оси X
        self.ax_1.yaxis.label.set_style("italic")  # Курсив для подписи оси Y
        # Добавляем сетку
        self.ax_1.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)
        # Сетка будет рисоваться ниже графика
        self.ax_1.set_axisbelow(True)
        # # Добавляем отступы через фигуру
        # self.figure_1.subplots_adjust(left = 0.08, right = 0.95, top = 0.95, bottom = 0.2)

        # Создание пустого Line2D 
        self.line = Line2D([], [], linestyle='None', marker='o', color='blue', markersize = COMM.Const.DOT_SIZE) 
        self.ax_1.add_line(self.line)


    def load_data_to_file(self, data_array):
        """
            Во время получения данных из прибора каждый полученный кадр
            записываем в файл, выбранный пользователем
        """
        try:
            if self.file_path:        
                with h5py.File(self.file_path, 'a') as file:  # Открытие файла на дозапись
                    group_name = f'list_{self.group_file_index}'  # Уникальное имя для каждой группы данных
                    group = file.create_group(group_name)
                    for j in range(len(data_array)):
                        group.create_dataset(f'pair_{j}', data = np.array([data_array[j]['channel'], data_array[j]['time']]))
                    self.group_file_index += 1  # Увеличение порядкового номера для следующего списка данных
        except Exception as e:
            self.textEdit_spectre.append("Виник exception під час запису даних у файл")


    @pyqtSlot(bytearray)
    def time_spectre_slot(self, data:bytearray)-> None:  

        try: 

            start_time = time.perf_counter() 

            if(data[5] == 0x09):
                return None          

            # Исходный размер numpy массива
            num_entries = 1550                 # (len(data) - 6) // 6  # Каждая запись занимает 6 байт    for i in range(6, 8994, 6):

            # Создаем пустой массив NumPy с нужным количеством записей
            result = np.zeros(num_entries, dtype=[('channel', np.uint16), ('time', np.uint32)])

            time_parameter = 0  # Локальная переменная для накопления времени
            count = 0  # Счетчик валидных записей

            for i in range(6, 8994, 6):
                # Распаковка сразу всех необходимых байт
                l_byte_ch, m_byte_ch, l0_byte_tm, l1_byte_tm, l2_byte_tm, l3_byte_tm = struct.unpack_from("6B", data, i)
                
                # Вычисление канала
                channel = l_byte_ch + (m_byte_ch << 8)
                if channel == 0:
                    continue

                # Вычисление временного значения
                tmp_val_l = l0_byte_tm + (l1_byte_tm << 8)
                tmp_val_m = l2_byte_tm + (l3_byte_tm << 8)
                new_time = tmp_val_l + (tmp_val_m << 16)
                if new_time == 0:
                    continue

                # Обновление time_parameter
                time_parameter += new_time
                if time_parameter > 1000000:
                    break

                # Добавляем данные в NumPy массив
                result[count] = (channel, time_parameter)
                count += 1

            # Отсекаем пустые записи
            result = result[:count]

            if self.checkBox.isChecked():
                self.write_file_signal.emit(result)  

            #################### ВСТАВИТЬ МЕТОД НАЧАЛО ###############################

            # Фильтруем массив
            mask = (result['channel'] != 0) & (result['time'] < len(self.global_buff))
            filtered = result[mask]

            # Массовая запись в глобальный буфер
            self.global_buff[filtered['time']] = filtered['channel'].astype(np.int16)

            # Получаем numpy массивы для отрисовки             
            indices = result['channel'] 
            values  = result['time']       
           
            # Добавляем новые точки на график 
            self.line.set_xdata(np.append(self.line.get_xdata(), values)) 
            self.line.set_ydata(np.append(self.line.get_ydata(), indices)) 
            self.ax_1.relim() 
            self.ax_1.autoscale_view()
               
            self.canvas_1.draw()  

            #################### ВСТАВИТЬ МЕТОД ОКОНЧАНИЕ ############################

            # Время набора спектра
            t_value = data[9006]    + (data[9007] << 8) 

            # ПЕД
            l_byte_ped = data[9008] + (data[9009] << 8)
            m_byte_ped = data[9010] + (data[9011] << 8) 
            num = l_byte_ped + (m_byte_ped << 8)       
            ped = num * 0.01 

            # CPS
            value = data[9016]   + (data[9017] << 8) 
            
            # Тестовый байт
            byte_to_check = data[9013]
            high_sens_detect  = "OK"
            low_sens_detector = "OK"           
            if byte_to_check & 0b00000001:   # D0 = 1 - отказ высокочувствительного детектора
                high_sens_detect  = "ERROR" 

            if byte_to_check & 0b00000010:   # D1 = 1 - отказ низкочувствительного детектора
                low_sens_detector = "ERROR" 
           
            
            formatted_text = f"""
                <h3><b><i>Накопичення часового спектру</i></b></h3>
                <p><b><i>Час початку накопичення:</i></b> <span style="color: blue;">&nbsp;{self.start_spectre_time }</span></p>
                <p><b><i>Тривалість накопичення, с:</i></b> <span style="color: green;">&nbsp;{t_value}</span></p>
                <p><b><i>Потужність дози, мкЗв/год:</i></b> <span style="color: red;">&nbsp;{str(ped)}</span></p>
                <p><b><i>Завантаження, імп/сек:</i></b> <span style="color: purple;">&nbsp;{str(value)}</span></p>
                <p><b>Самоконтроль ЛГМ:</b> <span style="color: black;">&nbsp;{low_sens_detector}</span></p>
                <p><b>Самоконтроль високочутливого детект.:</b> <span style="color: black;">&nbsp;{high_sens_detect}</span></p>
                """     

            end_time = time.perf_counter()
            elapsed_time_ms = (end_time - start_time) * 1000  # Преобразование в миллисекунды
            size = str(len(data))   
            _str  = "Прийнято " + size + " байт спектру\n"
            _str += f"Час виконання методу: {elapsed_time_ms:.3f} мілісекунд\n" 
            nonzero_count = np.count_nonzero(self.global_buff) 
            _str += f"Кількість eлементів у контейнері: {nonzero_count}\n"       
            
            info_dict = {"type": "time_spectre_params", "param_edit": _str, "data_edit": formatted_text}
            if self.gui_info_signal: 
                self.gui_info_signal.emit(info_dict)

        except Exception as e:
            info_dict = {"type": "time_spectre_global_write_error", "message": f"Виник exception у потоку запису даних, {str(e)}"}
            if self.gui_info_signal: 
                self.gui_info_signal.emit(info_dict)
            self.textEdit_spectre.append(str(e) + "\n")


    
    



    


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
