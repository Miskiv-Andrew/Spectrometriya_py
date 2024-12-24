import time
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot, QTimer
# from PyQt5.QtGui import QFont



from PyQt5.QtWidgets import QFileDialog, QMessageBox

import matplotlib.pyplot as plt
from  matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from  matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from  matplotlib.gridspec import GridSpec
from  matplotlib.ticker   import NullLocator, LinearLocator, MultipleLocator, IndexLocator, FixedLocator, MaxNLocator
from  matplotlib.ticker   import ScalarFormatter

import numpy as np

import COMMANDS as COMM 

import h5py
import os


class Ui_Form(object):

    # сигнал передачи данных в GUI (тип данных - словарь)   
    gui_info_signal = pyqtSignal(object) 

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

        self.file_path = None




    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Параметри та графіки часового спектру"))
        self.checkBox.setText(_translate("Form", "     Завантажувати дані у файл"))
        self.comboBox.setItemText(0, _translate("Form", "Режим таймера"))
        self.comboBox.setItemText(1, _translate("Form", "Покроковий режим"))
        self.comboBox.setItemText(2, _translate("Form", "Повне завантаження"))
        self.pushButton.setText(_translate("Form", "Виконати  крок завантаження"))
        self.pushButton_3.setText(_translate("Form", "Резерв"))
        self.pushButton_4.setText(_translate("Form", "Резерв"))



    
    @pyqtSlot(object)  
    def set_start_spectre_time(self, _time):
        self.start_spectre_time = _time

    @pyqtSlot(bool)
    def set_instrument_spectre(self, flag):    
        pass


    def on_checkBox_file_search(self, state):
        
        try:
            if state == QtCore.Qt.Unchecked:
                self.file_path = ""
                return None

            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly

            file_name, _ = QFileDialog.getSaveFileName(self, "Create TSP File", "", "TSP Files (*.tsp);;All Files (*)", options = options)
            
            if file_name:
                self.file_path = file_name

                # Открытие или создание файла HDF5
                with h5py.File(self.file_path, 'a') as file:
                    # Отображение информационного сообщения
                    QMessageBox.information(self, "Файл створено", f"Файл створено, запис даних буде відбуватись в нього:\n {self.file_path}")
                    # Здесь можно добавить любые начальные данные, если нужно
            else:
                self.file_path = ""
                return None

        except Exception as e:
            print(f"Error: {e}")
            self.file_path = ""

        



    @pyqtSlot()
    def clear_spectre(self):
        # Очищаем глобальный массив часового спектра
        self.global_buff = np.zeros(COMM.Const.GLOB_BUFF_SIZE,  dtype = np.int16)                
        
        # Очищаем предыдущие графики (если есть)
        self.ax_1.clear()
        self.canvas_1.draw()   


    def get_nonzero_values(self):

        # Получаем индексы ненулевых значений
        nonzero_indices = np.nonzero(self.global_buff)[0]        
        # Получаем сами ненулевые значения
        nonzero_values = self.global_buff[nonzero_indices]
        
        return nonzero_indices, nonzero_values

    @pyqtSlot(bytearray)
    def time_spectre_slot(self, data:bytearray)-> None:  

        try: 

            start_time = time.perf_counter() 

            if(data[5] == 0x09):
                return None
               

        ###### ОЧИСТКА ###############
        # После превышения кол-ва итераций начинаем заново "наполнять" секунду
            # self.iteration += 1
            # if self.iteration > COMM.Const.NUM_ITERATION:
            #     self.iteration = 0                             
            #     self.textEdit_spectre.append("\n\nNEW ITERATION")
            #     self.global_buff = np.zeros(COMM.Const.GLOB_BUFF_SIZE,  dtype = np.int16)                
            #     self.ax_1.clear()
           
        ###### ПЕРВИННА ОБРОБКА ###############

            # Обнуляем суммарную часовую метку
            self.time_parameter = 0 

            buff_list = []      
            l_byte_ch = None
            m_byte_ch = None
            l0_byte_tm = None
            l1_byte_tm = None
            l2_byte_tm = None
            l3_byte_tm = None  

            for i in range(6, 8994, 6):
                l_byte_ch = data[i]  
                m_byte_ch = data[i + 1] 
                channel = l_byte_ch + (m_byte_ch << 8)

                if channel == 0:
                    continue

                l0_byte_tm = data[i + 2]
                l1_byte_tm = data[i + 3]                
                tmp_val_l = l0_byte_tm  + (l1_byte_tm << 8)

                l2_byte_tm = data[i + 4]
                l3_byte_tm = data[i + 5]  
                tmp_val_m = l2_byte_tm  + (l3_byte_tm << 8)       

                new_time = tmp_val_l + (tmp_val_m << 16)            

                self.time_parameter += new_time   
                if  self.time_parameter >  1000000:
                    break   

                buff_list.append((channel,  self.time_parameter))        

            for pair in buff_list:
                value = pair[0]
                index = pair[1]
                if value == 0 or index == 0:
                    continue
                if index < len(self.global_buff):  
                    self.global_buff[index] = value

           
            ## Получаем numpy массивы для отрисовки
            nonzero_indices, nonzero_values = self.get_nonzero_values()            
            self.ax_1.scatter(nonzero_indices, nonzero_values,  s = 3, color='blue', label = "Small Points" )    

            x_ticks = np.arange(0, 1100000, 100000)
            self.ax_1.set_xticks(x_ticks)           
            
            # Установите ScalarFormatter для оси X
            formatter = ScalarFormatter(useOffset=False)
            formatter.set_scientific(False)  # Отключить научную запись
            self.ax_1.xaxis.set_major_formatter(formatter)
           
            
            y_ticks = np.arange(0, 1024, 100)
            self.ax_1.set_yticks(y_ticks)


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

            self.canvas_1.draw()     

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
