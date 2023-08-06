# patient
This is under review.

Patients need to know effects of medication and exercise for alleviating diseases. 
Biomarkers are used to monitor the status of individual diseases.

phope.py (Patient for Hospital Observation and Predicting Effects of medication and exercise)
with five determinants such as "day" (tested date), "hgb" of hbA1c value (biomarker for diabetes), "ntbnp" of NT-proBNP value (biomarker for heart failure), "degree1" (polynomial regression for hbA1c), and "degree2" (polynomial regression for NT-proBNP) is a universal biomarker prediction tool that can be used for evaluating the performance and predicting values of biomarkers in the next hospital visit.

To run phope.py after creating a data.csv, type python phope.py in the terminal.

In phope.py, you can change it for your use.

phope is a PyPI application. phope allows users to run on Windows, MacOS, and Linux operating systems as long as Python is installed on the system. phope can set left vertical axis and right vertical axis of two biomakers with data.csv.

data.csv is a data file composed of seven determinants such as "day" (tested date), "hgb" of hbA1c value (biomarker for diabetes), "ntbnp" of NT-proBNP value (biomarker for heart failure), "degree1" (polynomial regression for hbA1c), "degree2" (polynomial regression for NT-proBNP), the first vertical-axis range on left side (low and high), and the second vertical-axis range on right side (low and high).

The data.csv file must be created by the patient or physician before running the program.

<img src="https://github.com/ytakefuji/patient/raw/main/fig.png" height=90 width=400>

phope is a universal biomarker prediction tool with the past data. This example shows two biomarkers such as hbA1c and NT-proBNP. 

phope can predict any two biomakers simultaneously using the data in the second and third columns.

Columns 4 and 5 show the degree of polynomial regression for the first and second biomarkers, respectively.

Columns 6 and 7 set the range of vertical axis for the first and second biomarkers, respectively.

Based on data.csv with state-of-the-art technology, phope or phope.py can calculate and predict values of biomarkers for the next visit.

Predicting biomarker values allows patients to know the progress and trends of improvement in their diseases. 

Predictive values are hopes of patients.

# How to install phope
$ pip install phope

# How to run phope
$ phope

