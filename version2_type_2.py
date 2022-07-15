import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QLabel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPalette, QBrush, QPixmap


import matplotlib.pyplot as plt
import yfinance as yf
from scipy import stats
import mplfinance as mpf
import numpy as np
import pandas as pd
import statsmodels.regression.linear_model as lm
import statsmodels.api as sm
import datetime
from datetime import datetime as Dt

page_horizonal = 50
page_vertical = 50
page_width = 1600
page_height = 800

RA_default = 'AAPL' # the apple stock
MB_default = '^GSPC' # use S&P 500 index to represent the market
SD_default = '2021-1-1'
# ED_default = '2021-3-1'
ED_default = datetime.date.today()
global RISKY_ASSET
global MARKET_BENCHMARK
global START_DATE
global END_DATE
RISKY_ASSET = RA_default
MARKET_BENCHMARK = MB_default
START_DATE = SD_default
END_DATE = ED_default

class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):


        # self.centralwidget = QtWidgets.QWidget(MainWindow)
        # self.centralwidget.setStyleSheet("")
        # self.centralwidget.setObjectName("centralwidget")

        #set page window
        self.setGeometry(page_vertical, page_horizonal, page_width-460, page_height)
        self.setWindowTitle('Main Page')

        #set lineEdit
        font_lineEdit = QtGui.QFont()
        font_lineEdit.setFamily("Bradley Hand ITC")
        font_lineEdit.setPointSize(14)
        self.lineEdit_1 = QtWidgets.QLineEdit(self)
        self.lineEdit_1.setGeometry(QtCore.QRect(20, 130, 101, 51))
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        self.lineEdit_2.setGeometry(QtCore.QRect(200, 130, 111, 51))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self)
        self.lineEdit_3.setGeometry(QtCore.QRect(380, 130, 113, 51))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self)
        self.lineEdit_4.setGeometry(QtCore.QRect(560, 130, 113, 51))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.input_button1 = QtWidgets.QPushButton("Load Input", self)
        self.input_button1.setGeometry(QtCore.QRect(740, 130, 113, 51))
        self.input_button1.setFont(font_lineEdit)
        self.input_button1.clicked.connect(self.inputButton1Clicked)
        self.input_button2 = QtWidgets.QPushButton("Reset", self)
        self.input_button2.setGeometry(QtCore.QRect(920, 130, 113, 51))
        self.input_button2.setFont(font_lineEdit)
        self.input_button2.clicked.connect(self.inputButton2Clicked)
        self.label_1 = QtWidgets.QLabel("Risky Asset", self)
        self.label_1.setGeometry(QtCore.QRect(20, 100, 121, 30))
        self.label_1.setObjectName("label_1")
        self.label_1.setFont(font_lineEdit)
        self.label_2 = QtWidgets.QLabel("Market Benchmark", self)
        self.label_2.setGeometry(QtCore.QRect(170, 100, 200, 20))
        self.label_2.setObjectName("label_2")
        self.label_2.setFont(font_lineEdit)
        self.label_3 = QtWidgets.QLabel("Start Date", self)
        self.label_3.setGeometry(QtCore.QRect(380, 100, 100, 20))
        self.label_3.setObjectName("label_3")
        self.label_3.setFont(font_lineEdit)
        self.label_4 = QtWidgets.QLabel("End Date", self)
        self.label_4.setGeometry(QtCore.QRect(560, 100, 100, 20))
        self.label_4.setObjectName("label_4")
        self.label_4.setFont(font_lineEdit)

        #set 4 menu button
        font1 = QtGui.QFont()
        font1.setFamily("Bradley Hand ITC")
        font1.setPointSize(18)
        self.Btn_menu_1 = QtWidgets.QPushButton("Financial Data Dashboard", self)
        self.Btn_menu_1.setGeometry(QtCore.QRect(370, 210, 401, 101))
        self.Btn_menu_1.setFont(font1)
        self.Btn_menu_2 = QtWidgets.QPushButton("Show Designated Stock Data", self)
        self.Btn_menu_2.setGeometry(QtCore.QRect(370, 340, 401, 91))
        self.Btn_menu_2.setFont(font1)
        self.Btn_menu_3 = QtWidgets.QPushButton("Capm Model On Designated Stock", self)
        self.Btn_menu_3.setGeometry(QtCore.QRect(330, 470, 471, 91))
        self.Btn_menu_3.setFont(font1)
        self.Btn_menu_4 = QtWidgets.QPushButton("Fama French Model on Designated Stock", self)
        self.Btn_menu_4.setGeometry(QtCore.QRect(280, 590, 561, 101))
        self.Btn_menu_4.setFont(font1)

        #set label1
        font2 = QtGui.QFont()
        font2.setFamily("Bradley Hand ITC")
        font2.setPointSize(20)
        self.label1 = QtWidgets.QLabel(self)
        self.label1.setGeometry(QtCore.QRect(250, 10, 661, 45))
        self.label1.setFont(font2)
        self.label1.setObjectName("label_1")
        self.label1.setText("Welcome to use stock analytics assisstant tool")

        # set label2
        font3 = QtGui.QFont()
        font3.setFamily("Bradley Hand ITC")
        font3.setPointSize(16)
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(350, 740, 431, 51))
        self.label_2.setFont(font3)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Developed by Zhanfei Shi S2212045")

        self.show()

        self.Btn_menu_1.clicked.connect(self.close)  # add this line to implement page jump
        self.Btn_menu_2.clicked.connect(self.close)
        self.Btn_menu_3.clicked.connect(self.close)
        self.Btn_menu_4.clicked.connect(self.close)
    #load lineEdit data into the public string
    def inputButton1Clicked(self):
        global RISKY_ASSET
        global MARKET_BENCHMARK
        global START_DATE
        global END_DATE
        s1 = self.lineEdit_1.text()
        s2 = self.lineEdit_2.text()
        s3 = self.lineEdit_3.text()
        s4 = self.lineEdit_4.text()
        if s1 != '': #有输入就输入，没输入就默认值
            RISKY_ASSET = s1  # the amazon stock
        else:
            RISKY_ASSET = RA_default
        if s2 != '':
            MARKET_BENCHMARK = s2
        else:
            MARKET_BENCHMARK = MB_default
        if s3 != '':
            START_DATE = s3
        else:
            START_DATE = SD_default
        if s4 != '':
            END_DATE = s4
        else:
            END_DATE = ED_default
        # MARKET_BENCHMARK = s2  # use S&P 500 index to represent the market
        # START_DATE = s3
        # END_DATE = s4
        self.input_button1.setText('Data Loaded')
        self.input_button1.adjustSize()
    #reset lineEdit Data
    def inputButton2Clicked(self):
        global RISKY_ASSET
        global MARKET_BENCHMARK
        global START_DATE
        global END_DATE
        self.lineEdit_1.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        RISKY_ASSET = RA_default
        MARKET_BENCHMARK = MB_default
        START_DATE = SD_default
        END_DATE = ED_default
        self.input_button1.setText('Load Input')
        self.input_button1.setGeometry(QtCore.QRect(740, 130, 113, 51))

class page1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(page_vertical, page_horizonal, page_width, page_height)
        self.setWindowTitle('Page1')

        #set button1
        self.pushButton1 = QtWidgets.QPushButton(self)
        self.pushButton1.setGeometry(QtCore.QRect(10, 10, 230, 131))
        font1 = QtGui.QFont()
        font1.setFamily("Bradley Hand ITC")
        font1.setPointSize(18)
        self.pushButton1.setFont(font1)
        self.pushButton1.setText("Click to Visualize\nFinancial Data")
        self.pushButton1.clicked.connect(self.pushButton1Clicked)


        #set button2
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 160, 230, 61))
        font2 = QtGui.QFont()
        font2.setFamily("Bradley Hand ITC")
        font2.setPointSize(18)
        self.pushButton_2.setFont(font2)
        self.pushButton_2.setText("Click to return")
        self.pushButton_2.clicked.connect(self.close)
        self.pushButton_2.clicked.connect(self.pushButton2Clicked)

        #set figure label
        self.fig_label1 = QLabel(self)
        self.fig_label1.setGeometry(250, 100, 440, 225)
        self.fig_label1.setScaledContents(True)  # set this True to let figure fit label size

        self.fig_label2 = QLabel(self)
        self.fig_label2.setGeometry(700, 100, 440, 220)
        self.fig_label2.setScaledContents(True)  # set this True to let figure fit label size

        self.fig_label3 = QLabel(self)
        self.fig_label3.setGeometry(1150, 100, 440, 220)
        self.fig_label3.setScaledContents(True)  # set this True to let figure fit label size

        self.fig_label4 = QLabel(self)
        self.fig_label4.setGeometry(250, 335, 440, 220)
        self.fig_label4.setScaledContents(True)  # set this True to let figure fit label size

        self.fig_label5 = QLabel(self)
        self.fig_label5.setGeometry(700, 335, 440, 220)
        self.fig_label5.setScaledContents(True)  # set this True to let figure fit label size

        self.fig_label6 = QLabel(self)
        self.fig_label6.setGeometry(1150, 335, 440, 220)
        self.fig_label6.setScaledContents(True)  # set this True to let figure fit label size

        self.fig_label7 = QLabel(self)
        self.fig_label7.setGeometry(250, 570, 440, 220)
        self.fig_label7.setScaledContents(True)  # set this True to let figure fit label size

        self.fig_label8 = QLabel(self)
        self.fig_label8.setGeometry(700, 570, 440, 220)
        self.fig_label8.setScaledContents(True)  # set this True to let figure fit label size

        self.fig_label9 = QLabel(self)
        self.fig_label9.setGeometry(1150, 570, 440, 220)
        self.fig_label9.setScaledContents(True)  # set this True to let figure fit label size

    def pushButton1Clicked(self):
        # self.pushButton1.setText('Please wait a second:)')
        # self.pushButton1.adjustSize()
        #show gdp data
        world_gdp_data = pd.read_csv('API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4251000.csv')
        # world_gdp_data = world_gdp_data.reset_index(drop=True)
        world_gdp = world_gdp_data.iloc[259][4:66]
        China_gdp = world_gdp_data.iloc[40][4:66]
        USA_gdp = world_gdp_data.iloc[251][4:66]
        UK_gdp = world_gdp_data.iloc[81][4:66]
        # print(Russian_gdp)
        x = np.arange(1960, 2022, 1)
        plt.figure()
        plt.plot(x, world_gdp, label='World GDP data')
        plt.plot(x, China_gdp, label='China GDP data')
        plt.plot(x, USA_gdp, label='USA GDP data')
        plt.plot(x, UK_gdp, label='UK GDP data')
        plt.xlabel('Year')
        plt.ylabel('GDP/million dollars')
        plt.title('GDP data of world main economy')
        plt.legend()
        plt.savefig('World_GDP_visualization.jpg')

        #show gdp per capital data
        world_gdp_perCapital_data = pd.read_csv('API_NY.GDP.PCAP.CD_DS2_en_csv_v2_4251004.csv')
        world_gdp_perCapital = world_gdp_perCapital_data.iloc[259][4:66]
        China_gdp_perCapital = world_gdp_perCapital_data.iloc[40][4:66]
        USA_gdp_perCapital = world_gdp_perCapital_data.iloc[251][4:66]
        UK_gdp_perCapital = world_gdp_perCapital_data.iloc[81][4:66]
        # print(world_gdp_perCapital)
        x2 = np.arange(1960, 2022, 1)
        plt.figure()
        plt.plot(x2, world_gdp_perCapital, label='World GDP per capital data')
        plt.plot(x2, China_gdp_perCapital, label='China GDP per capital data')
        plt.plot(x2, USA_gdp_perCapital, label='USA GDP per capital data')
        plt.plot(x2, UK_gdp_perCapital, label='UK GDP per capital data')
        plt.xlabel('Year')
        plt.ylabel('GDP per capital/dollars')
        plt.title('GDP per capital data of world main economy')
        plt.legend()
        plt.savefig('World_GDP_perCapital_visualization.jpg')

        #show gdp growth rate data
        world_gdp_growth_data = pd.read_csv('API_NY.GDP.PCAP.KD.ZG_DS2_en_csv_v2_4250851.csv')
        world_gdp_growth = world_gdp_growth_data.iloc[259][4:66]
        China_gdp_growth = world_gdp_growth_data.iloc[40][4:66]
        USA_gdp_growth = world_gdp_growth_data.iloc[251][4:66]
        UK_gdp_growth = world_gdp_growth_data.iloc[81][4:66]
        # print(world_gdp_growth)
        x3 = np.arange(1960, 2022, 1)
        plt.figure()
        plt.plot(x3, world_gdp_growth, label='World GDP growth rate')
        plt.plot(x3, China_gdp_growth, label='China GDP growth rate')
        plt.plot(x3, USA_gdp_growth, label='USA GDP per growth rate')
        plt.plot(x3, UK_gdp_growth, label='UK GDP per growth rate')
        plt.xlabel('Year')
        plt.ylabel('GDP growth rate/percent')
        plt.title('GDP growth rate of world main economy')
        plt.legend()
        plt.savefig('World_GDP_growthRate_visualization.jpg')

        # show world electricity consumption data
        world_electricity_data = pd.read_csv('API_EG.USE.ELEC.KH.PC_DS2_en_csv_v2_4251643.csv')
        world_electricity = world_electricity_data.iloc[259][4:66]
        China_electricity = world_electricity_data.iloc[40][4:66]
        USA_electricity = world_electricity_data.iloc[251][4:66]
        UK_electricity = world_electricity_data.iloc[81][4:66]
        # print(world_electricity)
        x4 = np.arange(1960, 2022, 1)
        plt.figure()
        plt.plot(x4, world_electricity, label='World electricity consumption')
        plt.plot(x4, China_electricity, label='China electricity consumption')
        plt.plot(x4, USA_electricity, label='USA electricity consumption')
        plt.plot(x4, UK_electricity, label='UK electricity consumption')
        plt.xlabel('Year')
        plt.ylabel('Electricity consumption / kW·h per capital')
        plt.title('Electricity Consumption of world main economy')
        plt.legend()
        plt.savefig('World_electricity_visualization.jpg')

        # show world population rate data
        world_population_data = pd.read_csv('API_SP.POP.GROW_DS2_en_csv_v2_4251293.csv')
        world_population = world_population_data.iloc[259][4:66]
        China_population = world_population_data.iloc[40][4:66]
        USA_population = world_population_data.iloc[251][4:66]
        UK_population = world_population_data.iloc[81][4:66]
        # print(world_population)
        x5 = np.arange(1960, 2022, 1)
        plt.figure()
        plt.plot(x5, world_population, label='World population growth rate')
        plt.plot(x5, China_population, label='China population growth rate')
        plt.plot(x5, USA_population, label='USA population growth rate')
        plt.plot(x5, UK_population, label='UK population growth rate')
        plt.xlabel('Year')
        plt.ylabel('Population growth rate / percent')
        plt.title('Population growth rate of world main economy')
        plt.legend()
        plt.savefig('World_population_visualization.jpg')

        # show world inflation data(GDP deflator)
        world_inflation_data = pd.read_csv('API_NY.GDP.DEFL.KD.ZG_DS2_en_csv_v2_4250766.csv')
        world_inflation = world_inflation_data.iloc[259][4:66]
        China_inflation = world_inflation_data.iloc[40][4:66]
        USA_inflation = world_inflation_data.iloc[251][4:66]
        UK_inflation = world_inflation_data.iloc[81][4:66]
        # print(world_inflation)
        x6 = np.arange(1960, 2022, 1)
        plt.figure()
        plt.plot(x6, world_inflation, label='World inflation rate')
        plt.plot(x6, China_inflation, label='China inflation rate')
        plt.plot(x6, USA_inflation, label='USA inflation rate')
        plt.plot(x6, UK_inflation, label='UK inflation rate')
        plt.xlabel('Year')
        plt.ylabel('Inflation rate / percent')
        plt.title('Inflation rate of world main economy')
        plt.legend()
        plt.savefig('World_inflation_visualization.jpg')

        #show gold data
        start_date = '2021-1-5'
        today = datetime.date.today()
        latest_day = today + datetime.timedelta(days=-1)
        # end_date = '2022-7-22'
        Gold_data = yf.download('GLD', start=start_date, end=latest_day, group_by="ticker", proxy="127.0.0.1:33210",
                                index_col=0, auto_adjust=True)
        # print(Gold_data)
        plt.figure()
        plt.plot(Gold_data['Close'])
        plt.xlabel('Year')
        plt.ylabel('Gold Price/dollar')
        plt.title(f'Gold Price from{start_date} until {today}')
        plt.savefig(f'Gold_price_until_{today}.jpg')

        #show oil data
        start_date = '2021-1-1'
        today = datetime.date.today()
        # end_date = '2022-7-22'
        Oil_data = yf.download('USO', start=start_date, end=today, group_by="ticker", proxy="127.0.0.1:33210",
                               index_col=0, auto_adjust=True)
        plt.figure()
        plt.plot(Oil_data['Close'])
        plt.xlabel('Year')
        plt.ylabel('Oil Price/dollar')
        plt.title(f'Oil Price from{start_date} until {today}')
        plt.savefig(f'Oil_price_until_{today}.jpg')

        # show gas data
        start_date = '2021-1-1'
        today = datetime.date.today()
        # end_date = '2022-7-22'
        Gas_data = yf.download('UNG', start=start_date, end=today, group_by="ticker", proxy="127.0.0.1:33210",
                               index_col=0, auto_adjust=True)
        plt.figure()
        plt.plot(Gas_data['Close'])
        plt.xlabel('Year')
        plt.ylabel('Gas Price/dollar')
        plt.title(f'Gas Price from{start_date} until {today}')
        plt.savefig(f'Gas_price_until_{today}.jpg')

        self.fig_label1.setStyleSheet("border: 1px solid red")  # define fig_label1 in the init_Ui, click button to show
        self.fig1 = QPixmap('World_GDP_visualization.jpg')
        self.fig_label1.setPixmap(self.fig1)

        self.fig_label2.setStyleSheet("border: 1px solid red")  # define fig_label1 in the init_Ui, click button to show
        self.fig2 = QPixmap('World_GDP_perCapital_visualization.jpg')
        self.fig_label2.setPixmap(self.fig2)

        self.fig_label3.setStyleSheet("border: 1px solid red")  # define fig_label1 in the init_Ui, click button to show
        self.fig3 = QPixmap('World_GDP_growthRate_visualization.jpg')
        self.fig_label3.setPixmap(self.fig3)

        self.fig_label4.setStyleSheet("border: 1px solid red")  # define fig_label1 in the init_Ui, click button to show
        self.fig4 = QPixmap('World_electricity_visualization.jpg')
        self.fig_label4.setPixmap(self.fig4)

        self.fig_label5.setStyleSheet("border: 1px solid red")  # define fig_label1 in the init_Ui, click button to show
        self.fig5 = QPixmap('World_population_visualization.jpg')
        self.fig_label5.setPixmap(self.fig5)

        self.fig_label6.setStyleSheet("border: 1px solid red")  # define fig_label1 in the init_Ui, click button to show
        self.fig6 = QPixmap('World_inflation_visualization.jpg')
        self.fig_label6.setPixmap(self.fig6)

        self.fig_label7.setStyleSheet("border: 1px solid red")  # define fig_label1 in the init_Ui, click button to show
        self.fig7 = QPixmap(f'Gold_price_until_{today}.jpg')
        self.fig_label7.setPixmap(self.fig7)

        self.fig_label8.setStyleSheet("border: 1px solid red")  # define fig_label1 in the init_Ui, click button to show
        self.fig8 = QPixmap(f'Oil_price_until_{today}.jpg')
        self.fig_label8.setPixmap(self.fig8)

        self.fig_label9.setStyleSheet("border: 1px solid red")  # define fig_label1 in the init_Ui, click button to show
        self.fig9 = QPixmap(f'Gas_price_until_{today}.jpg')
        self.fig_label9.setPixmap(self.fig9)

        self.pushButton1.setText('Financial data visualized\nand saved in same directory')
        self.pushButton1.adjustSize()
        
    def pushButton2Clicked(self):
        self.pushButton1.setGeometry(QtCore.QRect(10, 10, 230, 131))
        self.pushButton1.setText("Click to Visualize\nFinancial Data")
        self.fig_label1.setStyleSheet("")
        self.fig1 = QPixmap('')
        self.fig_label1.setPixmap(self.fig1)
        self.fig_label2.setStyleSheet("")
        self.fig2 = QPixmap('')
        self.fig_label2.setPixmap(self.fig2)
        self.fig_label3.setStyleSheet("")
        self.fig3 = QPixmap('')
        self.fig_label3.setPixmap(self.fig3)
        self.fig_label4.setStyleSheet("")
        self.fig4 = QPixmap('')
        self.fig_label4.setPixmap(self.fig4)
        self.fig_label5.setStyleSheet("")
        self.fig5 = QPixmap('')
        self.fig_label5.setPixmap(self.fig5)
        self.fig_label6.setStyleSheet("")
        self.fig6 = QPixmap('')
        self.fig_label6.setPixmap(self.fig6)
        self.fig_label7.setStyleSheet("")
        self.fig7 = QPixmap('')
        self.fig_label7.setPixmap(self.fig7)
        self.fig_label8.setStyleSheet("")
        self.fig8 = QPixmap('')
        self.fig_label8.setPixmap(self.fig8)
        self.fig_label9.setStyleSheet("")
        self.fig9 = QPixmap('')
        self.fig_label9.setPixmap(self.fig9)

class page2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(page_vertical, page_horizonal, page_width, page_height)
        self.setWindowTitle('Page2')

        # set button1
        self.pushButton1 = QtWidgets.QPushButton(self)
        self.pushButton1.setGeometry(QtCore.QRect(10, 10, 280, 131))
        font1 = QtGui.QFont()
        font1.setFamily("Bradley Hand ITC")
        font1.setPointSize(18)
        self.pushButton1.setFont(font1)
        self.pushButton1.setText("Click to Visualize\nDesinated Stock Data")
        self.pushButton1.clicked.connect(self.pushButton1Clicked)

        # set button2
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 160, 280, 61))
        font2 = QtGui.QFont()
        font2.setFamily("Bradley Hand ITC")
        font2.setPointSize(18)

        #set figure label
        self.fig_label1 = QLabel(self)
        self.fig_label1.setGeometry(300, 100, 600, 600)
        self.fig_label1.setScaledContents(True) # set this True to let figure fit label size

        self.fig_label2 = QLabel(self)
        self.fig_label2.setGeometry(950, 100, 600, 600)
        self.fig_label2.setScaledContents(True)  # set this True to let figure fit label size

        self.pushButton_2.setFont(font2)
        self.pushButton_2.setText("Click to return")
        self.pushButton_2.clicked.connect(self.pushButton2Clicked)
        self.pushButton_2.clicked.connect(self.close)

    def pushButton1Clicked(self):
        global RISKY_ASSET
        global MARKET_BENCHMARK
        global START_DATE
        global END_DATE
        stockObject = yf.download(RISKY_ASSET, start=START_DATE, end=END_DATE, group_by="ticker",
                                  proxy="127.0.0.1:33210")  # acquire data
        marketBenchmark = yf.download(MARKET_BENCHMARK, start=START_DATE, end=END_DATE, group_by="ticker",
                                      proxy="127.0.0.1:33210")
        stockObject = stockObject.drop(columns=['Adj Close'])
        mpf.plot(stockObject, type='candle', title=f'Price change of {RISKY_ASSET}', volume=True,
                 savefig=f'stock_data_{RISKY_ASSET}.jpg')  # can add savefig='mpf1.jpg' to save the fig
        marketBenchmark = marketBenchmark.drop(columns=['Adj Close'])
        mpf.plot(marketBenchmark, type='candle', title=f'Price change of {MARKET_BENCHMARK}', volume=True,
                 savefig=f'stock_data_{MARKET_BENCHMARK}.jpg')
        self.pushButton1.setText('Data has been visualized\nand saved in same directory')
        self.pushButton1.adjustSize()
        # print('Data has been downloaded')

        self.fig_label1.setStyleSheet("border: 2px solid red")# define fig_label1 in the init_Ui, click button to show
        self.fig1 = QPixmap(f'stock_data_{RISKY_ASSET}.jpg')
        self.fig_label1.setPixmap(self.fig1)

        self.fig_label2.setStyleSheet("border: 2px solid red")  # define fig_label1 in the init_Ui, click button to show
        self.fig2 = QPixmap(f'stock_data_{MARKET_BENCHMARK}.jpg')
        self.fig_label2.setPixmap(self.fig2)
    
    def pushButton2Clicked(self):
        self.pushButton1.setGeometry(QtCore.QRect(10, 10, 280, 131))
        self.pushButton1.setText("Click to Visualize\nDesinated Stock Data")
        self.fig_label1.setStyleSheet("")
        self.fig1 = QPixmap('')
        self.fig_label1.setPixmap(self.fig1)
        self.fig_label2.setStyleSheet("")
        self.fig2 = QPixmap('')
        self.fig_label2.setPixmap(self.fig2)

class page3(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(page_vertical, page_horizonal, page_width, page_height)
        self.setWindowTitle('Page3')

        # set button1
        self.pushButton1 = QtWidgets.QPushButton(self)
        self.pushButton1.setGeometry(QtCore.QRect(10, 10, 260, 131))
        font1 = QtGui.QFont()
        font1.setFamily("Bradley Hand ITC")
        font1.setPointSize(18)
        self.pushButton1.setFont(font1)
        self.pushButton1.setText("Click to Run\nCAPM Model\non Desinated Stock")
        self.pushButton1.clicked.connect(self.pushButton1Clicked)

        # set button2
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 180, 260, 61))
        font2 = QtGui.QFont()
        font2.setFamily("Bradley Hand ITC")
        font2.setPointSize(18)
        self.pushButton_2.setFont(font2)
        self.pushButton_2.setText("Click to return")

        # set figure label
        self.fig_label1 = QLabel(self)
        self.fig_label1.setGeometry(50, 300, 650, 400)
        self.fig_label1.setScaledContents(True)  # set this True to let figure fit label size

        self.fig_label2 = QLabel(self)
        self.fig_label2.setGeometry(720, 300, 400, 400)
        self.fig_label2.setScaledContents(True)  # set this True to let figure fit label size

        self.fig_label3 = QLabel(self)
        self.fig_label3.setGeometry(1140, 300, 400, 400)
        self.fig_label3.setScaledContents(True)  # set this True to let figure fit label size

        self.pushButton_2.clicked.connect(self.pushButton2Clicked)
        self.pushButton_2.clicked.connect(self.close)

    def pushButton1Clicked(self):
        global RISKY_ASSET
        global MARKET_BENCHMARK
        global START_DATE
        global END_DATE
        stockObject = yf.download(RISKY_ASSET, start=START_DATE, end=END_DATE, group_by="ticker",
                                  proxy="127.0.0.1:33210")  # acquire data
        marketBenchmark = yf.download(MARKET_BENCHMARK, start=START_DATE, end=END_DATE, group_by="ticker",
                                      proxy="127.0.0.1:33210")

        stockObject['Close'] = stockObject['Close'] / stockObject['Close'].iloc[0]
        marketBenchmark['Close'] = marketBenchmark['Close'] / marketBenchmark['Close'].iloc[0]
        stockObject['daily_ret'] = stockObject['Close'].pct_change(1)
        marketBenchmark['daily_ret'] = marketBenchmark['Close'].pct_change(1)
        lr = stats.linregress(stockObject['daily_ret'].iloc[1:], marketBenchmark['daily_ret'].iloc[1:])

        beta, alpha, r_value, p_value, std_err = lr
        rf = 1.2855 / 100  # UK 1-Year Treasury Bond on 30/03/2022
        Ef = (marketBenchmark['Close'].iloc[marketBenchmark['Close'].shape[0] - 1] - marketBenchmark['Close'].iloc[0]) / \
             marketBenchmark['Close'].iloc[0]
        CAPM_expectReturnRate = rf + beta * (Ef - rf)
        self.pushButton1.setText(
            f'The CAPM Return Rate of {RISKY_ASSET}\n based on{MARKET_BENCHMARK}\nfrom {START_DATE} to {END_DATE} \nis {round(CAPM_expectReturnRate, 5)}')
        self.pushButton1.adjustSize()
        plt.figure()
        plt.bar(['risk-free rate', 'market rate', f'CAPM model rate of {RISKY_ASSET}'], [rf, Ef, CAPM_expectReturnRate])
        plt.xlabel('investing rate comparison')
        plt.ylabel('investing return rate')
        plt.title(f'Investing Return Rate of Risk-free Rate, Market Rate and CAPM model Rate of {RISKY_ASSET}')
        plt.savefig('CAPM model bar chart.jpg')

        RiskFreeRate = 1.2855 / 100  # UK 1-Year Treasury Bond on 30/03/2022
        sharpe_stock = (stockObject['Close'] - RiskFreeRate).mean() / (stockObject['Close'] - RiskFreeRate).std()
        sharpe_market = (marketBenchmark['Close'] - RiskFreeRate).mean() / (
                marketBenchmark['Close'] - RiskFreeRate).std()
        print(sharpe_market)
        plt.figure()
        plt.bar([f'Sharpe Ratio of {RISKY_ASSET}', f'Sharpe Ratio of {MARKET_BENCHMARK}'],
                [sharpe_stock, sharpe_market])
        plt.xlabel('Sharpe Ratio Comparison')
        plt.ylabel('Sharpe Ratio')
        plt.title(f'Sharpe Ratio of {RISKY_ASSET} and Market Benchmark')
        plt.savefig('sharpe ratio visualization.jpg')

        def normfun(x, mu, sigma):
            pdf = np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) / (sigma * np.sqrt(2 * np.pi))
            return pdf

        mean_stock = (stockObject['Close'] - RiskFreeRate).mean()
        std_stock = (stockObject['Close'] - RiskFreeRate).std()
        x_stock = np.linspace(mean_stock - 5 * std_stock, mean_stock + 5 * std_stock, 100)
        y_stock = normfun(x_stock, mean_stock, std_stock)

        mean_market = (marketBenchmark['Close'] - RiskFreeRate).mean()
        std_market = (marketBenchmark['Close'] - RiskFreeRate).std()
        x_market = np.linspace(mean_market - 5 * std_market, mean_market + 5 * std_market, 100)
        y_market = normfun(x_market, mean_market, std_market)

        plt.figure()
        plt.plot(x_stock, y_stock, label=f'{RISKY_ASSET} Volatility')
        plt.plot(x_market, y_market, label=f'{MARKET_BENCHMARK} Volatility')
        plt.xlabel('Volatility Comparison')
        plt.ylabel('Volatility')
        plt.legend()
        plt.title(f'Comparison of Volatility between {RISKY_ASSET} and {MARKET_BENCHMARK}')
        plt.savefig('Volatility Visualization.jpg')

        self.fig_label1.setStyleSheet("border: 1px solid red")  # define fig_label1 in the init_Ui, click button to show
        self.fig1 = QPixmap('CAPM model bar chart.jpg')
        self.fig_label1.setPixmap(self.fig1)
        self.fig_label2.setStyleSheet("border: 1px solid red")  # define fig_label1 in the init_Ui, click button to show
        self.fig2 = QPixmap('sharpe ratio visualization.jpg')
        self.fig_label2.setPixmap(self.fig2)
        self.fig_label3.setStyleSheet("border: 1px solid red")  # define fig_label1 in the init_Ui, click button to show
        self.fig3 = QPixmap('Volatility Visualization.jpg')
        self.fig_label3.setPixmap(self.fig3)

    def pushButton2Clicked(self):
        self.pushButton1.setGeometry(QtCore.QRect(10, 10, 260, 131))
        self.pushButton1.setText("Click to Run\nCAPM Model\non Desinated Stock")
        #hide figure
        self.fig_label1.setStyleSheet("")
        self.fig1 = QPixmap('')
        self.fig_label1.setPixmap(self.fig1)
        self.fig_label2.setStyleSheet("")
        self.fig2 = QPixmap('')
        self.fig_label2.setPixmap(self.fig2)
        self.fig_label3.setStyleSheet("")
        self.fig3 = QPixmap('')
        self.fig_label3.setPixmap(self.fig3)

class page4(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(page_vertical, page_horizonal, page_width, page_height)
        self.setWindowTitle('Page4')

        # set button1
        self.pushButton1 = QtWidgets.QPushButton(self)
        self.pushButton1.setGeometry(QtCore.QRect(10, 10, 270, 121))
        font1 = QtGui.QFont()
        font1.setFamily("Bradley Hand ITC")
        font1.setPointSize(16)
        self.pushButton1.setFont(font1)
        self.pushButton1.setText("Click to Run\nFama French Model\non Desinated Stock")
        self.pushButton1.clicked.connect(self.pushButton1Clicked)
        # set button2
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 260, 250, 61))
        font2 = QtGui.QFont()
        font2.setFamily("Bradley Hand ITC")
        font2.setPointSize(18)
        self.pushButton_2.setFont(font2)
        self.pushButton_2.setText("Click to return")

        # set figure label
        self.fig_label1 = QLabel(self)
        self.fig_label1.setGeometry(50, 330, 650, 450)
        self.fig_label1.setScaledContents(True)  # set this True to let figure fit label size

        self.fig_label2 = QLabel(self)
        self.fig_label2.setGeometry(720, 330, 400, 450)
        self.fig_label2.setScaledContents(True)  # set this True to let figure fit label size

        self.fig_label3 = QLabel(self)
        self.fig_label3.setGeometry(1140, 330, 400, 450)
        self.fig_label3.setScaledContents(True)  # set this True to let figure fit label size

        self.fig_label4 = QLabel(self)
        self.fig_label4.setGeometry(900, 10, 600, 300)
        self.fig_label4.setScaledContents(True)  # set this True to let figure fit label size

        self.pushButton_2.clicked.connect(self.pushButton2Clicked)
        self.pushButton_2.clicked.connect(self.close)

    def pushButton1Clicked(self):
        global RISKY_ASSET
        global MARKET_BENCHMARK
        global START_DATE
        global END_DATE
        stockObject = yf.download(RISKY_ASSET, start=START_DATE, end=END_DATE, group_by="ticker",
                                  proxy="127.0.0.1:33210", index_col=0)
        # stockObject_qFactor = yf.download(RISKY_ASSET, start=START_DATE, end=END_DATE, group_by="ticker",
        #                           proxy="127.0.0.1:33210", index_col=0)
        stockObject_qFactor = stockObject.copy(deep=True)# 复制一份给qfactor用
        returns_3 = pd.read_csv('F-F_Research_Data_Factors_daily.csv', index_col=0)
        returns_5 = pd.read_csv('F-F_Research_Data_5_Factors_2x3_daily.csv', index_col=0)
        returns_3['Date'] = returns_3.index
        returns_5['Date'] = returns_5.index
        stockObject['daily_ret'] = stockObject['Close'].pct_change(1)

        # 观察发现3因子和5因子数据集的SMB不一样，Mkt-RF和HML是一样的
        stockObject['Date'] = stockObject.index
        stockObject.insert(stockObject.shape[1], 'Mkt-RF', 0)
        stockObject.insert(stockObject.shape[1], 'SMB_3', 0)
        stockObject.insert(stockObject.shape[1], 'SMB_5', 0)
        stockObject.insert(stockObject.shape[1], 'HML', 0)
        stockObject.insert(stockObject.shape[1], 'RMW', 0)
        stockObject.insert(stockObject.shape[1], 'CMA', 0)
        stockObject.insert(stockObject.shape[1], 'RF', 0)

        # 合并fama french五因子数据到yf 股票data里 yf下载的数据可能比上面得到的end_iloc要提前（yf似乎下载指定结束日期之前交易日的数据）
        for i in range(returns_3.shape[0]):
            if Dt.strptime(returns_3['Date'][i], '%Y/%m/%d') == Dt.strptime(
                    str(stockObject['Date'].iloc[0]).split(' ')[0], '%Y-%m-%d'):
                iloc_offset_3 = i
                print('OFFSET iteration is', iloc_offset_3)
        for i in range(returns_5.shape[0]):
            if Dt.strptime(returns_5['Date'][i], '%Y/%m/%d') == Dt.strptime(
                    str(stockObject['Date'].iloc[0]).split(' ')[0], '%Y-%m-%d'):
                iloc_offset_5 = i
                print('OFFSET iteration is', iloc_offset_5)
        # 然后，把stockObject那段长度之前的fama-french数据放进stockObject

        for i in range(stockObject.shape[0]):
            stockObject['Mkt-RF'].iloc[i] = returns_3['Mkt-RF'].iloc[i + iloc_offset_3]
            stockObject['SMB_3'].iloc[i] = returns_3['SMB'].iloc[i + iloc_offset_3]
            stockObject['SMB_5'].iloc[i] = returns_5['SMB'].iloc[i + iloc_offset_5]
            stockObject['HML'].iloc[i] = returns_3['HML'].iloc[i + iloc_offset_3]
            stockObject['RMW'].iloc[i] = returns_5['RMW'].iloc[i + iloc_offset_5]
            stockObject['CMA'].iloc[i] = returns_5['CMA'].iloc[i + iloc_offset_5]
            stockObject['RF'].iloc[i] = returns_3['RF'].iloc[i + iloc_offset_3]
            stockObject['daily_ret'].iloc[i] -= returns_3['RF'].iloc[i + iloc_offset_3]

        # stockObject.loc[1:,'CT'] = ct.add_constant(stockObject) #ct是多元线性拟合的截距项
        x_ff3 = stockObject[['Mkt-RF', 'SMB_3', 'HML']].iloc[1:]
        y_ff3 = stockObject['daily_ret'].iloc[1:]
        x_ff3 = sm.add_constant(x_ff3)
        ff3fm = lm.OLS(y_ff3, x_ff3).fit()
        x_ff5 = stockObject[['Mkt-RF', 'SMB_5', 'HML', 'RMW', 'CMA']].iloc[1:]
        y_ff5 = stockObject['daily_ret'].iloc[1:]
        x_ff5 = sm.add_constant(x_ff5)
        ff5fm = lm.OLS(y_ff5, x_ff5).fit()
        # ff3fm = lm.OLS(stockObject['daily_ret'].iloc[1:], stockObject[['Mkt-RF', 'SMB_3', 'HML']].iloc[1:],
        #                hasconst=bool).fit()
        # ff5fm = lm.OLS(stockObject['daily_ret'].iloc[1:],
        #                stockObject[['Mkt-RF', 'SMB_5', 'HML', 'RMW', 'CMA']].iloc[1:], hasconst=bool).fit()
        print('Fama French 3 factors summary')
        print(ff3fm.summary())
        print('Fama French 5 factors summary')
        print(ff5fm.summary())

        # 绘制ff5fm模型预测收益率，和实际进行可视化对比
        intercept3, beta_Mkt_RF_3, beta_SMB_3, beta_HML_3 = ff3fm.params
        intercept5, beta_Mkt_RF_5, beta_SMB_5, beta_HML_5, beta_RMW, beta_CMA = ff5fm.params
        # beta_Mkt_RF = ff5fm.params[0]
        # beta_SMB_3 = ff5fm.params[1]
        # beta_SMB_5 = ff3fm.params[1]
        # beta_HML = ff5fm.params[2]
        # beta_RMW = ff5fm.params[3]
        # beta_CMA = ff5fm.params[4]
        stockObject.insert(stockObject.shape[1], 'ff3fm_return', 0)
        stockObject.insert(stockObject.shape[1], 'ff5fm_return', 0)
        stockObject['ff3fm_return'] = stockObject['RF'] + beta_Mkt_RF_3 * stockObject['Mkt-RF'] + beta_SMB_3 * \
                                      stockObject['SMB_3'] + beta_HML_3 * stockObject['HML']
        stockObject['ff5fm_return'] = stockObject['RF'] + beta_Mkt_RF_5 * stockObject['Mkt-RF'] + beta_SMB_5 * \
                                      stockObject['SMB_5'] + beta_HML_5 * stockObject['HML'] + beta_RMW * stockObject[
                                          'RMW'] + beta_CMA * stockObject['CMA']

        #跑一下q5模型
        q_returns = pd.read_csv('q5_factors_daily_2021_2.csv', index_col=0)
        q_returns.columns.tolist
        # returns.rename_axis('Date',axis='columns')
        q_returns['Date'] = q_returns.index
        # print(q_returns)
        stockObject_qFactor['daily_ret'] = stockObject_qFactor['Close'].pct_change(1)

        stockObject_qFactor['Date'] = stockObject_qFactor.index
        stockObject_qFactor.insert(stockObject_qFactor.shape[1], 'Mkt-RF', 0)
        stockObject_qFactor.insert(stockObject_qFactor.shape[1], 'ME', 0)
        stockObject_qFactor.insert(stockObject_qFactor.shape[1], 'IA', 0)
        stockObject_qFactor.insert(stockObject_qFactor.shape[1], 'ROE', 0)
        stockObject_qFactor.insert(stockObject_qFactor.shape[1], 'EG', 0)
        stockObject_qFactor.insert(stockObject_qFactor.shape[1], 'RF', 0)

        for i in range(q_returns.shape[0]):
            if Dt.strptime(q_returns['Date'][i], '%Y/%m/%d') == Dt.strptime(
                    str(stockObject_qFactor['Date'].iloc[0]).split(' ')[0], '%Y-%m-%d'):
                iloc_offset_qFactor = i
        print('qFactor OFFSET iteration is', iloc_offset_qFactor)
        for i in range(stockObject_qFactor.shape[0]):
            stockObject_qFactor['Mkt-RF'].iloc[i] = q_returns['R_MKT'].iloc[i + iloc_offset_qFactor] - q_returns['R_F'].iloc[
                i + iloc_offset_qFactor]
            stockObject_qFactor['ME'].iloc[i] = q_returns['R_ME'].iloc[i + iloc_offset_qFactor]
            stockObject_qFactor['IA'].iloc[i] = q_returns['R_IA'].iloc[i + iloc_offset_qFactor]
            stockObject_qFactor['ROE'].iloc[i] = q_returns['R_ROE'].iloc[i + iloc_offset_qFactor]
            stockObject_qFactor['EG'].iloc[i] = q_returns['R_EG'].iloc[i + iloc_offset_qFactor]
            stockObject_qFactor['RF'].iloc[i] = q_returns['R_F'].iloc[i + iloc_offset_qFactor]
            stockObject_qFactor['daily_ret'].iloc[i] -= q_returns['R_F'].iloc[i + iloc_offset_qFactor]
        # stockObject_qFactor.to_csv('stockObject.csv')
        x_qf = stockObject_qFactor[['Mkt-RF', 'ME', 'IA', 'ROE', 'EG']].iloc[1:]
        y_qf = stockObject_qFactor['daily_ret'].iloc[1:]
        x_qf = sm.add_constant(x_qf)
        Qf = lm.OLS(y_qf, x_qf).fit()
        print('q5 factors summary')
        print(Qf.summary())
        intercept_q5, beta_Mkt_RF_q5, beta_ME, beta_IA, beta_ROE, beta_EG = Qf.params
        stockObject_qFactor.insert(stockObject_qFactor.shape[1], 'qf_return', 0)
        stockObject_qFactor['qf_return'] = intercept_q5 + stockObject_qFactor['RF'] + beta_Mkt_RF_q5 * stockObject_qFactor['Mkt-RF'] + beta_ME * \
                                   stockObject_qFactor['ME'] + beta_IA * stockObject_qFactor['IA'] + beta_ROE * stockObject_qFactor[
                                       'ROE'] + beta_EG * stockObject_qFactor['EG']

        #显示ff3、5和q5 收益率与真实收益率
        plt.figure()
        plt.plot(stockObject['daily_ret'], label='Actual daily return')
        plt.plot(stockObject['ff3fm_return'], label='Fama French 3 factor model daily return')
        plt.plot(stockObject['ff5fm_return'], label='Fama French 5 factor model daily return')
        plt.plot(stockObject_qFactor['qf_return'], label='q5 factor model daily return')
        plt.xlabel('Date')
        plt.ylabel('Return Rate')
        plt.title(f'Comparison of Actual daily return, Fama French and q5 factor return of {RISKY_ASSET}')
        plt.legend()
        plt.savefig('FF35&q5fm_return.jpg')

        # 可视化对比一下ff各个beta系数
        plt.figure()
        # plt.bar(['beta_Mkt-RF','beta_SMB','beta_HML'],[beta_Mkt_RF,beta_SMB,beta_HML])
        plt.bar(['beta_Mkt-RF', 'beta_SMB', 'beta_HML', 'alpha'],
                [beta_Mkt_RF_3, beta_SMB_3, beta_HML_3, intercept3])
        plt.xlabel('Coefficient value of Fama French Factors')
        plt.ylabel('Coefficient value')
        plt.title(f'Beta value of coefficient of Fama French 3 factor of {RISKY_ASSET}')
        plt.savefig('FF3fm_coefficient_value.jpg')

        plt.figure()
        plt.bar(['beta_Mkt-RF', 'beta_SMB', 'beta_HML', 'beta_RMW', 'beta_CMA', 'alpha'],
                [beta_Mkt_RF_5, beta_SMB_5, beta_HML_5, beta_RMW, beta_CMA, intercept5])
        plt.xlabel('Coefficient value of Fama French Factors')
        plt.ylabel('Coefficient value')
        plt.title(f'Beta value of coefficient of Fama French 5 factor of {RISKY_ASSET}')
        plt.savefig('FF5fm_coefficient_value.jpg')

        # 可视化对比一下q5各个beta系数
        plt.figure()
        plt.bar(['beta_Mkt-RF', 'beta_ME', 'beta_IA', 'beta_ROE', 'beta_EG', 'alpha'],
                [beta_Mkt_RF_q5, beta_ME, beta_IA, beta_ROE, beta_EG, intercept_q5])
        plt.xlabel('Coefficient value of q5 Factors')
        plt.ylabel('Coefficient value')
        plt.title(f'Beta value of coefficient of q5 factor of {RISKY_ASSET}')
        plt.savefig('q5_coefficient_value.jpg')

        self.fig_label1.setStyleSheet("border: 1px solid red")  # define fig_label1 in the init_Ui, click button to show
        self.fig1 = QPixmap('FF35&q5fm_return.jpg')
        self.fig_label1.setPixmap(self.fig1)
        self.fig_label2.setStyleSheet("border: 1px solid red")  # define fig_label1 in the init_Ui, click button to show
        self.fig2 = QPixmap('FF3fm_coefficient_value.jpg')
        self.fig_label2.setPixmap(self.fig2)
        self.fig_label3.setStyleSheet("border: 1px solid red")  # define fig_label1 in the init_Ui, click button to show
        self.fig3 = QPixmap('FF5fm_coefficient_value.jpg')
        self.fig_label3.setPixmap(self.fig3)
        self.fig_label4.setStyleSheet("border: 1px solid red")  # define fig_label1 in the init_Ui, click button to show
        self.fig4 = QPixmap('q5_coefficient_value.jpg')
        self.fig_label4.setPixmap(self.fig4)

        self.pushButton1.setText(
            f'Fama French 3 factor coefficients are:\nMkt-RF {round(beta_Mkt_RF_3, 5)},SMB {round(beta_SMB_3, 5)},HML {round(beta_HML_3, 5)}, alpha {round(intercept3, 5)}\n'
            f'Fama French 5 factor coefficients are:\nMkt-RF {round(beta_Mkt_RF_5, 5)},SMB {round(beta_SMB_5, 5)},HML {round(beta_HML_5, 5)}, alpha {round(intercept5, 5)}\n'
            f'RMW is{round(beta_RMW, 5)},CMA is{round(beta_CMA, 5)}'
            f'Q5 factor coefficients are:\nMkt-RF {round(beta_Mkt_RF_q5,5)}, ME {round(beta_ME,5)}, IA {round(beta_IA,5)}\n'
            f'ROE {beta_ROE}, EG {beta_EG}')
        self.pushButton1.adjustSize()

    def pushButton2Clicked(self):
        self.pushButton1.setText("Click to Run\nFama French Model\non Desinated Stock")
        self.pushButton1.setGeometry(QtCore.QRect(10, 10, 270, 121))

        self.fig_label1.setStyleSheet("")
        self.fig1 = QPixmap('')
        self.fig_label1.setPixmap(self.fig1)
        self.fig_label2.setStyleSheet("")
        self.fig2 = QPixmap('')
        self.fig_label2.setPixmap(self.fig2)
        self.fig_label3.setStyleSheet("")
        self.fig3 = QPixmap('')
        self.fig_label3.setPixmap(self.fig3)
        self.fig_label4.setStyleSheet("")
        self.fig4 = QPixmap('')
        self.fig_label4.setPixmap(self.fig4)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainPage = MainPage()
    page1 = page1()
    page2 = page2()
    page3 = page3()
    page4 = page4()

    MainPage.show()

    MainPage.Btn_menu_1.clicked.connect(page1.show)  # keypoint of page selection
    page1.pushButton_2.clicked.connect(MainPage.show)

    MainPage.Btn_menu_2.clicked.connect(page2.show)
    page2.pushButton_2.clicked.connect(MainPage.show)

    MainPage.Btn_menu_3.clicked.connect(page3.show)
    page3.pushButton_2.clicked.connect(MainPage.show)

    MainPage.Btn_menu_4.clicked.connect(page4.show)
    page4.pushButton_2.clicked.connect(MainPage.show)

    sys.exit(app.exec_())
