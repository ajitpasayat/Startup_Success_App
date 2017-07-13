import sys
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QWidget, QMessageBox, QDialog, QApplication, QPushButton, QLineEdit, QFormLayout
import numpy as np
import pandas as pd
import math

df = pd.read_csv('Final - Copy.csv')
startup_year = pd.read_csv('Startup_failure.csv')
startup_indus = pd.read_csv('startup_indus.csv')

def country_lookup(country):
    if(sum(df['Economy'].isin([country.lower()])) == 1):
        output = ("The Rating of the country is: "+ str(df[df['Economy'] == country.lower()]['Rating'].values[0]))
    else:
        output = ('Enter the below mentioned details')
    return output

def input_lookup(hdi, exp_growth, govt_support, peop_perc, start_opp, fear_fail):

    rating = 1.86326674 + 1.878060667*(hdi**2) + 0.007876521*exp_growth + 0.094112735*govt_support + 0.005572445*peop_perc + 0.004247178*start_opp - -0.00446717*fear_fail 
    output = ("The expected Entrepreneurship rating for your region will be: " + str(round(math.exp(rating),2)))
    return output

def success_lookup(year):
    return (1 - startup_year[startup_year['Year'] == year]['Failure'])

def success_indus_lookup(industry):
    #print((startup_indus[startup_indus['Serial'] == industry]['Success']))
    return (startup_indus[startup_indus['Serial'] == industry]['Success'])
    
class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        
        self.le = QLineEdit()
        self.le.setObjectName("host")
        self.le.setText("Enter the Country Name")

        #Push Button 1
        self.pb = QPushButton()
        self.pb.setObjectName("connect")
        self.pb.setText("Connect with country")
        #self.pb.resize(100,80)

        # HDI
        self.le1 = QLineEdit()
        self.le1.setObjectName("hdi")
        self.le1.setText("Enter the HDI of the Country 0-1")

        # Expected Growth
        self.le2 = QLineEdit()
        self.le2.setObjectName("exp growth")
        self.le2.setText("Expected Growth of the start up during nascent stage 1-100")

        # Government Support and Policies
        self.le3 = QLineEdit()
        self.le3.setObjectName("govt_Support")
        self.le3.setText("Government support and policies 1-10")

        #People perception whether product is new?
        self.le4 = QLineEdit()
        self.le4.setObjectName("peop_perc")
        self.le4.setText("Population perception of novelty of product 1-100")        

        #% people who think working in a startup is an opportunity
        self.le5 = QLineEdit()
        self.le5.setObjectName("startup_opp")
        self.le5.setText("% of people who believe Start-up is an opportunity 1-100")

        # Fear of failure
        self.le6 = QLineEdit()
        self.le6.setObjectName("fear_fail")
        self.le6.setText("Population perception about failure of business 1-100")
        
        #Push Button 2
        self.pb2 = QPushButton()
        self.pb2.setObjectName("connect")
        self.pb2.setText("Connect with other inputs")

        # Year
        self.le7 = QLineEdit()
        self.le7.setObjectName("Year")
        self.le7.setText("Year the startup is in 1-10")

        # Rating
        self.le8 = QLineEdit()
        self.le8.setObjectName("Rating")
        self.le8.setText("Rating of the region 1-100")

        #Industry
        self.le9 = QLineEdit()
        self.le9.setObjectName("Industry")
        self.le9.setText("Serial Number of the Industry 1-11")

        #Push Button 3
        self.pb3 = QPushButton()
        self.pb3.setObjectName("connect")
        self.pb3.setText("Calculate Probability")

        
        layout = QFormLayout()
        layout.addWidget(self.le)
        layout.addWidget(self.pb)
        layout.addWidget(self.le1)
        layout.addWidget(self.le2)
        layout.addWidget(self.le3)
        layout.addWidget(self.le4)
        layout.addWidget(self.le5)
        layout.addWidget(self.le6)
        layout.addWidget(self.pb2)
        layout.addWidget(self.le7)
        layout.addWidget(self.le8)
        layout.addWidget(self.le9)
        layout.addWidget(self.pb3)
        
        self.setLayout(layout)
        self.connect(self.pb, SIGNAL("clicked()"),self.button_click)
        self.connect(self.pb2, SIGNAL("clicked()"),self.button_click_2)
        self.connect(self.pb3, SIGNAL("clicked()"),self.button_click_3)
        self.setWindowTitle("Entrepreneurship Locator")
        self.resize(1200, 800)
        
    def button_click(self):
        # shost is a QString object
        country = self.le.text()
        result = country_lookup(country)

        #Message Box
        
        self.msg = QMessageBox()
        self.msg.setText(result)
        self.msg.setWindowTitle("Result")
        self.msg.exec_()
        
    def button_click_2(self):
        hdi = float(self.le1.text())
        exp_growth = float(self.le2.text())
        govt_support = float(self.le3.text())
        peop_perc = float(self.le4.text())
        start_opp = float(self.le5.text())
        fear_fail = float(self.le6.text())
        result = input_lookup(hdi, exp_growth, govt_support, peop_perc, start_opp, fear_fail)


        #Message Box
        self.msg = QMessageBox()
        self.msg.setText(result)
        self.msg.setWindowTitle("Result")
        self.msg.exec_()
    
    def button_click_3(self):
        year = float(self.le7.text())
        rating = float(self.le8.text())
        industry = int(self.le9.text())
        result = float((success_lookup(year).values[0] * rating * success_indus_lookup(industry))/(83.4*0.58))

        #Message Box
        self.msg = QMessageBox()
        self.msg.setText("The probability of success of the startup is: "+str(round(result,2)))
        self.msg.setWindowTitle("Result")
        self.msg.exec_()       


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
