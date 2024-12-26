# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simple_spectre_graf.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer

import matplotlib.pyplot as plt
from  matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from  matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from  matplotlib.gridspec import GridSpec
from  matplotlib.ticker import NullLocator, LinearLocator, MultipleLocator, IndexLocator, FixedLocator, MaxNLocator

from scipy.signal import savgol_filter
import numpy as np
import struct



class Ui_Form(object):

    # сигнал передачи данных в GUI (тип данных - словарь)   
    gui_info_signal = pyqtSignal(object)   

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1100, 800)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget_Plot = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_Plot.sizePolicy().hasHeightForWidth())
        self.widget_Plot.setSizePolicy(sizePolicy)
        self.widget_Plot.setObjectName("widget_Plot")
        self.horizontalLayout_2.addWidget(self.widget_Plot)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_channel = QtWidgets.QLabel(Form)

        self.label_channel.setAlignment(QtCore.Qt.AlignCenter)

        self.label_channel.setObjectName("label_channel")
        self.gridLayout_7.addWidget(self.label_channel, 1, 0, 1, 1)
        self.label_value = QtWidgets.QLabel(Form)

        self.label_value.setAlignment(QtCore.Qt.AlignCenter)

        self.label_value.setObjectName("label_value")
        self.gridLayout_7.addWidget(self.label_value, 1, 2, 1, 1)
        self.pushButton_right_channel = QtWidgets.QPushButton(Form)
        self.pushButton_right_channel.setObjectName("pushButton_right_channel")
        self.gridLayout_7.addWidget(self.pushButton_right_channel, 1, 4, 1, 1)
        self.label_energy = QtWidgets.QLabel(Form)

        self.label_energy.setAlignment(QtCore.Qt.AlignCenter)

        self.label_energy.setObjectName("label_energy")
        self.gridLayout_7.addWidget(self.label_energy, 1, 1, 1, 1)
        self.pushButton_left_channel = QtWidgets.QPushButton(Form)
        self.pushButton_left_channel.setObjectName("pushButton_left_channel")
        self.gridLayout_7.addWidget(self.pushButton_left_channel, 1, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(Form)

        self.label_4.setAlignment(QtCore.Qt.AlignCenter)

        self.label_4.setObjectName("label_4")
        self.gridLayout_7.addWidget(self.label_4, 0, 0, 1, 5)
        self.horizontalLayout_3.addLayout(self.gridLayout_7)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setContentsMargins(0, -1, -1, -1)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout_5.addWidget(self.label, 1, 0, 1, 1)        
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout_5.addWidget(self.label_2, 1, 2, 1, 1)
        self.checkBox_2 = QtWidgets.QCheckBox(Form)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout_5.addWidget(self.checkBox_2, 0, 2, 1, 2)
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_5.addWidget(self.checkBox, 0, 0, 1, 2)
        self.spinBox = QtWidgets.QSpinBox(Form)
        self.spinBox.setMaximum(28)
        self.spinBox.setSingleStep(2)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout_5.addWidget(self.spinBox, 1, 1, 1, 1)
        self.spinBox_2 = QtWidgets.QSpinBox(Form)
        self.spinBox_2.setMaximum(10)
        self.spinBox_2.setObjectName("spinBox_2")
        self.gridLayout_5.addWidget(self.spinBox_2, 1, 3, 1, 1)
        self.horizontalLayout_3.addLayout(self.gridLayout_5)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.current_x = 0
        self.current_y = 0

        self.pushButton_right_channel.clicked.connect(self.move_right)  # Кнопка вправо
        self.pushButton_left_channel.clicked.connect(self.move_left)    # Кнопка влево

        self.pushButton_right_channel.pressed.connect(self.on_right_button_pressed)  # Кнопка вправо, при нажатии
        self.pushButton_right_channel.released.connect(self.on_right_button_released)  # Кнопка вправо, при отпускании

        self.pushButton_left_channel.pressed.connect(self.on_left_button_pressed)  # Кнопка влево, при нажатии
        self.pushButton_left_channel.released.connect(self.on_left_button_released)  # Кнопка влево, при отпускании 

        self.move_timer = QTimer(Form)
        self.move_timer.setInterval(100)  # Интервал 100 мс      

        # Создаем Figure и FigureCanvas
        self.figure = plt.figure()          
        self.canvas = FigureCanvas(self.figure)

        # Встраиваем canvas в widget_Plot
        layout = QtWidgets.QVBoxLayout(self.widget_Plot)
        layout.addWidget(self.canvas)
        
        # Добавляем панель инструментов для навигации по графику
        self.navigation_toolbar = NavigationToolbar(self.canvas, Form) 

        self.navigation_toolbar.setStyleSheet("""
            QToolBar {
                spacing: 30px;  /* Интервал между кнопками и меню */
            }
        """)

            # Применяем подсказки к действиям
        for action in self.navigation_toolbar.actions():
            if action.text() == "Home":
                action.setToolTip("Перейти на початкову позицію")
            elif action.text() == "Back":
                action.setToolTip("Назад")
            elif action.text() == "Forward":
                action.setToolTip("Вперед")
            elif action.text() == "Pan":
                action.setToolTip("Переміщення графіка")
            elif action.text() == "Zoom":
                action.setToolTip("Масштабування графіка")
            elif action.text() == "Subplots":
                action.setToolTip("Керування  підграфіками")
            elif action.text() == "Customize":
                action.setToolTip("Налаштування панелі інструментів")
            elif action.text() == "Save":
                action.setToolTip("Зберегти графік")

        layout.addWidget(self.navigation_toolbar)

        self.ax = self.figure.add_subplot(111)

        # NUMPY  обычный массив спектра
        self.spectre_arr = np.zeros(1030)

        # NUMPY  логарифмический массив спектра
        self.spectre_log_arr = np.zeros(1030)


        self.start_spectre_time = None

        self.spinBox.setMinimum(3)
        self.spinBox.setMaximum(29)
        self.spinBox.setSingleStep(2)

        self.spinBox_2.setMinimum(2)
        self.spinBox_2.setMaximum(7)
        self.spinBox_2.setSingleStep(1)

        self.checkBox.stateChanged.connect(self.checkBox_Changed)
        self.checkBox_2.stateChanged.connect(self.checkBox_2_Changed)


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)




    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Параметри та графік стандартного спектру"))
        self.label_channel.setText(_translate("Form", "Канал"))
        self.label_value.setText(_translate("Form", "Значення"))
        self.pushButton_right_channel.setText(_translate("Form", ">>"))
        self.label_energy.setText(_translate("Form", "Енергія"))
        self.pushButton_left_channel.setText(_translate("Form", "<<"))
        self.label_4.setText(_translate("Form", "Енергетичні показники"))
        self.label.setText(_translate("Form", "Розмір вікна фільтра"))
        self.label_2.setText(_translate("Form", "Степінь полінома"))
        self.checkBox_2.setText(_translate("Form", "Усереднення"))
        self.checkBox.setText(_translate("Form", "   Логарифмічний масштаб"))




    def checkBox_Changed(self, state): 
            if self.checkBox.isChecked(): 
                self.checkBox_2.setChecked(False)	



    def checkBox_2_Changed(self, state): 
        if self.checkBox_2.isChecked(): 
            self.checkBox.setChecked(False)	


    def move_left(self):
        if self.current_x - 1 >= 0:
            self.current_x -= 1  # Перемещаем на 1 влево
            self.update_vertical_line(self.current_x, self.current_y)

    def move_right(self):
        # Проверяем, можем ли переместить линию вправо (не выходим за пределы графика)
        if self.current_x + 1 < len(self.spectre_arr):
            self.current_x += 1  # Перемещаем на 1 вправо
            self.update_vertical_line(self.current_x, self.current_y)  # Обновляем вертикальную линию

    def on_right_button_pressed(self):
        self.move_timer.timeout.connect(self.move_right)  # Привязываем обработчик
        self.move_timer.start()  # Запускаем таймер

    def on_right_button_released(self):
        self.move_timer.timeout.disconnect(self.move_right)
        self.move_timer.stop()  # Останавливаем таймер, когда кнопка отпущена


    def on_left_button_pressed(self):
        self.move_timer.timeout.connect(self.move_left)  # Привязываем обработчик
        self.move_timer.start()  # Запускаем таймер

    def on_left_button_released(self):
        self.move_timer.timeout.disconnect(self.move_left)
        self.move_timer.stop()  # Останавливаем таймер, когда кнопка отпущена     


    def update_vertical_line(self, _x, _y):
        # Удаляем только вертикальную линию, если она была
        for line in self.ax.lines:
            if line.get_label() == 'vertical_line':
                line.remove()

        # Отрисовываем новую вертикальную линию от точки (x, y) до оси X (x, 0)
        self.ax.plot([_x, _x], [0, _y], color = 'red', label = 'vertical_line') 

        # Обновляем canvas
        self.canvas.draw() 

        self.label_channel.setText(f"Канал<br><span style='color:red; font-weight:bold;'>{_x}</span>")

        if _x < len(self.spectre_arr):
            y = self.spectre_arr[_x]
            self.label_value.setText(f"Значення<br><span style='color:green; font-weight:bold;'>{y}</span>") 

    def on_pick(self, event) :
        if not self.navigation_toolbar.isEnabled():
            return None
        else: 
            if event.inaxes:
                x = event.xdata  # Координата x, на которой был клик
                y = event.ydata                
                x = int(x)
                y = int(y) 
                self.current_x = x
                self.current_y = y             

                self.update_vertical_line(x,y)

    @pyqtSlot()
    def clear_spectre(self):
        self.spectre_arr = np.zeros(1030)
        # Очищаем предыдущие графики (если есть)
        self.figure.clear()
        # Обновляем canvas
        self.canvas.draw()        


    @pyqtSlot(object)  
    def set_start_spectre_time(self, _time):
        self.start_spectre_time = _time

    @pyqtSlot(bool)
    def set_instrument_spectre(self, flag):    
        self.navigation_toolbar.setEnabled(flag)
        self.spinBox.setEnabled(flag)
        self.spinBox_2.setEnabled(flag)
        self.checkBox.setEnabled(flag)
        self.checkBox_2.setEnabled(flag) 
        self.pushButton_left_channel.setEnabled(flag)
        self.pushButton_right_channel.setEnabled(flag)

    @pyqtSlot(bytearray)
    def simple_spectre_slot(self, data:bytearray)-> None:        
        
        start_time = time.perf_counter()
        
       
        posit = 0        
        for i in range(6, 2059, 2):
            l_byte = data[i]  
            m_byte = data[i + 1] 
            value = l_byte  + (m_byte << 8)            
            self.spectre_arr[posit] += value
            if self.spectre_arr[posit] > 0:
                self.spectre_log_arr[posit] = np.log(self.spectre_arr[posit])
            else:
                 self.spectre_log_arr[posit] = 0                
            posit += 1

        # Очищаем предыдущие графики (если есть)
        self.figure.clear()

        # Получаем вспомогательный массив для выведения графика
        help_buff = self.spectre_arr[:1020]

        win_len = self.spinBox.value()
        pol_ord =  self.spinBox_2.value()       
        help_aver_buff = savgol_filter(help_buff, window_length = win_len, polyorder = pol_ord)

        help_log_buff = self.spectre_log_arr[:1020]

        MAX = np.max(help_buff)   
        x = np.arange(len(help_buff))   

        MAX_AVER = np.max(help_aver_buff)   
        MAX_LOG  = np.max(help_log_buff)    

        
        # Создаем локальный объект оси
        self.ax = self.figure.add_subplot(111)
        
        # self.ax.set_ylim(0, MAX * 1.25)  # Установка пределов оси Y

        # Устанавливаем метки по оси X с шагом 100 от 0 до 1100
        x_ticks = np.arange(0, 1200, 100)
        self.ax.set_xticks(x_ticks)

        # Устанавливаем метки по оси Y, чтобы их было 10
        y_ticks = np.linspace(0, 1.25 * MAX, 11)
        self.ax.set_yticks(y_ticks)

        self.ax.yaxis.set_major_locator(MaxNLocator(integer=True))


        if self.checkBox.isChecked():
            self.ax.set_ylim(0, MAX_LOG * 1.25)  # Установка пределов оси Y
            self.ax.plot(x, help_log_buff)  # Строим логарифмический график

        elif self.checkBox_2.isChecked():
            self.ax.set_ylim(0, MAX_AVER * 1.25)  # Установка пределов оси Y
            self.ax.plot(x, help_aver_buff)  # Строим усредненный график

        else:
            self.ax.set_ylim(0, MAX * 1.25)  # Установка пределов оси Y
            self.ax.plot(x, help_buff)  # Строим обычный график
       
        # Настройка осей
        self.ax.spines['left'].set_position('zero')  # Ось Y начинается с 0
        self.ax.spines['bottom'].set_position('zero')  # Ось X начинается с 0
        self.ax.spines['right'].set_color('none')  # Убираем правую ось
        self.ax.spines['top'].set_color('none')  # Убираем верхнюю ось

        # Добавляем сетку
        self.ax.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)

              
        # Сетка будет рисоваться ниже графика
        self.ax.set_axisbelow(True)

        # Добавляем отступы через фигуру
        self.figure.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.08)

        # Подключаем обработчик клика
        self.canvas.mpl_connect('button_press_event', self.on_pick)        
        
        # Обновляем canvas
        self.canvas.draw()        

        t_value = (data[2055]  << 8)  + (data[2054]) 
        
        num = struct.unpack('<I', data[2056:2060])[0]            
        ped = num * 0.01 
      
        value = (data[2065] << 8)   + data[2064] 
       
        byte_to_check = data[2061]

        high_sens_detect  = "OK"
        low_sens_detector = "OK"            
        
        if byte_to_check & 0b00000001:   # D0 = 1 - отказ высокочувствительного детектора
            high_sens_detect  = "ERROR" 

        if byte_to_check & 0b00000010:   # D1 = 1 - отказ низкочувствительного детектора
            low_sens_detector = "ERROR"      


        formatted_text = f"""
        <h3><b><i>Накопичення стандартного спектру</i></b></h3>
        <p><b><i>Час початку накопичення:</i></b> <span style="color: blue;">&nbsp;{self.start_spectre_time }</span></p>
        <p><b><i>Тривалість накопичення, с:</i></b> <span style="color: green;">&nbsp;{t_value}</span></p>
        <p><b><i>Потужність дози, мкЗв/год:</i></b> <span style="color: red;">&nbsp;{str(ped)}</span></p>
        <p><b><i>Завантаження, імп/сек:</i></b> <span style="color: purple;">&nbsp;{str(value)}</span></p>
        <p><b>Самоконтроль ЛГМ:</b> <span style="color: black;">&nbsp;{low_sens_detector}</span></p>
        <p><b>Самоконтроль високочутливого детект.:</b> <span style="color: black;">&nbsp;{high_sens_detect}</span></p>
        """
        end_time = time.perf_counter()
        elapsed_time_ms = (end_time - start_time) * 1000  # Преобразование в миллисекунды  
        _str = "Прийнято " + str(len(data)) + " байт спектру\n"
        _str += f"Час виконання методу: {elapsed_time_ms:.3f} мілісекунд\n"  
        info_dict = {"left": _str, "right": formatted_text}                           
        if self.gui_info_signal: 
            self.gui_info_signal.emit(info_dict)

       




     



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()


    sys.exit(app.exec_())
