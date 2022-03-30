from json import JSONDecodeError

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QCompleter, QComboBox
import sys
import requests
from pandas.io.json import json_normalize
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import geopandas as gpd
from keplergl import KeplerGl


class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.setGeometry(200,200, 600, 600)
		self.setWindowTitle("Covid Tracker App")
		img = QImage("147907952_1036917130125246_6661745496331239301_n.png")
		sImage = img.scaled(QSize(600,600))
		palette = QPalette()
		palette.setBrush(QPalette.Window, QBrush(sImage))
		self.setPalette(palette)
		self.initUI()

	def initUI(self):		
		kraje = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola',
	   'Anguilla', 'Antigua_and_Barbuda', 'Argentina', 'Armenia', 'Aruba',
	   'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain',
	   'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
	   'Bermuda', 'Bhutan', 'Bolivia',
	   'Bonaire, Saint Eustatius and Saba', 'Bosnia_and_Herzegovina',
	   'Botswana', 'Brazil', 'British_Virgin_Islands',
	   'Brunei_Darussalam', 'Bulgaria', 'Burkina_Faso', 'Burundi',
	   'Cambodia', 'Cameroon', 'Canada', 'Cape_Verde',
	   'Cases_on_an_international_conveyance_Japan', 'Cayman_Islands',
	   'Central_African_Republic', 'Chad', 'Chile', 'China', 'Colombia',
	   'Comoros', 'Congo', 'Costa_Rica', 'Cote_dIvoire', 'Croatia',
	   'Cuba', 'Curaçao', 'Cyprus', 'Czechia',
	   'Democratic_Republic_of_the_Congo', 'Denmark', 'Djibouti',
	   'Dominica', 'Dominican_Republic', 'Ecuador', 'Egypt',
	   'El_Salvador', 'Equatorial_Guinea', 'Eritrea', 'Estonia',
	   'Eswatini', 'Ethiopia', 'Falkland_Islands_(Malvinas)',
	   'Faroe_Islands', 'Fiji', 'Finland', 'France', 'French_Polynesia',
	   'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar',
	   'Greece', 'Greenland', 'Grenada', 'Guam', 'Guatemala', 'Guernsey',
	   'Guinea', 'Guinea_Bissau', 'Guyana', 'Haiti', 'Holy_See',
	   'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran',
	   'Iraq', 'Ireland', 'Isle_of_Man', 'Israel', 'Italy', 'Jamaica',
	   'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kosovo',
	   'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho',
	   'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg',
	   'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta',
	   'Marshall_Islands', 'Mauritania', 'Mauritius', 'Mexico',
	   'Micronesia_(Federated_States_of)', 'Moldova', 'Monaco',
	   'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique',
	   'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'New_Caledonia',
	   'New_Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North_Macedonia',
	   'Northern_Mariana_Islands', 'Norway', 'Oman', 'Pakistan',
	   'Palestine', 'Panama', 'Papua_New_Guinea', 'Paraguay', 'Peru',
	   'Philippines', 'Poland', 'Portugal', 'Puerto_Rico', 'Qatar',
	   'Romania', 'Russia', 'Rwanda', 'Saint_Kitts_and_Nevis',
	   'Saint_Lucia', 'Saint_Vincent_and_the_Grenadines', 'San_Marino',
	   'Sao_Tome_and_Principe', 'Saudi_Arabia', 'Senegal', 'Serbia',
	   'Seychelles', 'Sierra_Leone', 'Singapore', 'Sint_Maarten',
	   'Slovakia', 'Slovenia', 'Solomon_Islands', 'Somalia',
	   'South_Africa', 'South_Korea', 'South_Sudan', 'Spain', 'Sri_Lanka',
	   'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan',
	   'Tajikistan', 'Thailand', 'Timor_Leste', 'Togo',
	   'Trinidad_and_Tobago', 'Tunisia', 'Turkey',
	   'Turks_and_Caicos_islands', 'Uganda', 'Ukraine',
	   'United_Arab_Emirates', 'United_Kingdom',
	   'United_Republic_of_Tanzania', 'United_States_of_America',
	   'United_States_Virgin_Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu',
	   'Venezuela', 'Vietnam', 'Wallis_and_Futuna', 'Western_Sahara',
	   'Yemen', 'Zambia', 'Zimbabwe']
		self.label = QtWidgets.QLabel(self)
		self.label.setText("Ustaw opcje: ")
		self.label.setFont(QFont('Arial', 16))
		self.label.setStyleSheet('color: white')
		self.label.adjustSize()
		self.label.move(30,100)

		self.comboBox1 = QComboBox(self)
		self.comboBox1.addItems(['Caly rok','Marzec, Kwiecień, Maj', 'Czerwiec, Lipiec, Sierpień', 'Wrzesień, Październik, Listopad', 'Grudzień, Styczeń, Luty'])
		self.comboBox1.move(220,100)

		self.comboBox2 = QComboBox(self)
		self.comboBox2.addItems(['Ogólna liczba przypadków (tygodniowo)', 'Liczba przypadków na 100 tys mieszkańców'])
		self.comboBox2.move(330,100)

		self.label2 = QtWidgets.QLabel(self)
		self.label2.setText("Okres:")
		self.label2.setFont(QFont('Arial', 16))
		self.label2.setStyleSheet('color: white')
		self.label2.adjustSize()
		self.label2.move(240, 70)

		self.label3 = QtWidgets.QLabel(self)
		self.label3.setText("Dane: ")
		self.label3.setFont(QFont('Arial', 16))
		self.label3.setStyleSheet('color: white')
		self.label3.adjustSize()
		self.label3.move(340, 70)

		# kraj
		self.label4 = QtWidgets.QLabel(self)
		self.label4.setText("Wybierz kraj: ")
		self.label4.setFont(QFont('Arial', 16))
		self.label4.setStyleSheet('color: white')
		self.label4.adjustSize()
		self.label4.move(30, 150)

		self.comboBox3 = QComboBox(self)
		self.comboBox3.addItems(kraje)
		self.comboBox3.move(220,150)


		okButton = QtWidgets.QPushButton("Pokaż", self)
		okButton.move(30, 190)
		okButton.clicked.connect(self.raport)

		# TOP 10

		self.label5 = QtWidgets.QLabel(self)
		self.label5.setText("Pokaż top 10: ")
		self.label5.setFont(QFont('Arial', 16))
		self.label5.setStyleSheet('color: white')
		self.label5.adjustSize()
		self.label5.move(30,330)

		self.comboBox4 = QComboBox(self)
		self.comboBox4.addItems(['10 krajów z najwyższą sumą wszystkich przypadków', '10 krajów z najwyższą sumą wszystkich zgonów', '10 krajów z najwyższą sumą przypadków w ciągu ostatnich 7 dni', '10 krajów z największą liczbą aktywnych przypadków', '10 krajów z najwyższą liczbą przypadków na 100 tysięcy mieszkańców'])
		self.comboBox4.move(220,330)

		okButton2 = QtWidgets.QPushButton("Pokaż", self)
		okButton2.move(30, 280)
		okButton2.clicked.connect(self.porownaj)

		# POROWNANIE

		self.label6 = QtWidgets.QLabel(self)
		self.label6.setText("Porównaj: ")
		self.label6.setFont(QFont('Arial', 16))
		self.label6.setStyleSheet('color: white')
		self.label6.move(30,240)

		self.comboBox5 = QComboBox(self)
		self.comboBox5.addItems(kraje)
		self.comboBox5.move(220,240)

		self.comboBox6 = QComboBox(self)
		self.comboBox6.addItems(kraje)
		self.comboBox6.move(330,240)


		okButton3 = QtWidgets.QPushButton("Pokaż", self)
		okButton3.move(30, 370)
		okButton3.clicked.connect(self.raport_top10)

		# MAPA

		self.label7 = QtWidgets.QLabel(self)
		self.label7.setText("Wygeneruj HTML do mapy")
		self.label7.setFont(QFont('Arial', 16))
		self.label7.setStyleSheet('color: white')
		self.label7.adjustSize()
		self.label7.move(30,420)

		okButton4 = QtWidgets.QPushButton("Generuj", self)
		okButton4.move(30, 460)
		okButton4.clicked.connect(self.mapa)

	def create_df(self):
		url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/json/'
		response = requests.get(url).json()['records']
		def new_format(record):
			return {
				"Country": record['countriesAndTerritories'],
				"Date": record['dateRep'],
				"Cases": record["cases_weekly"],
				"Cases_Per_100k": record["notification_rate_per_100000_population_14-days"]
			}

		api = [new_format(record) for record in response]

		df = json_normalize(api)
		df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
		df["Cases_Per_100k"] = pd.to_numeric(df["Cases_Per_100k"], downcast="float")
		# Uogólniam dane tak żeby wszystkie były od 1.03.2020 (tak żeby nam wyszły 4 okresy po 3 mies łącznie z tym lutym 2021)
		df = df[df['Date'] >= '2020-03-01']
		return df

	def create_df2(self):
		url = 'https://api.covid19api.com/summary'
		response = requests.get(url).json()['Countries']

		def new_format2(record):
			return {
				"Country": record['Country'],
				"TotalDeaths": record['TotalDeaths'],
				"TotalCases": record["TotalConfirmed"],
				"TotalRecovered": record["TotalRecovered"]
			}

		api = [new_format2(record) for record in response]
		df = json_normalize(api)
		df['ActiveCases'] = df['TotalCases'] - df['TotalRecovered']
		return df

	def raport(self):

		country = str(self.comboBox3.currentText())
		okres = str(self.comboBox1.currentText())
		per = str(self.comboBox2.currentText())
		df = self.create_df()

		if okres == 'Caly rok':
			period = 'Date'
			locator = mdates.DayLocator(interval=30)
			locator_min = mdates.DayLocator(interval=10)
		elif okres == 'Marzec, Kwiecień, Maj':
			df = df[df['Date']< '2020-06-01']
			period = 'Date'
			locator = mdates.DayLocator(interval=10)
			locator_min = mdates.DayLocator(interval=7)
		elif okres == 'Czerwiec, Lipiec, Sierpień':
			df = df[(df['Date'] >= '2020-06-01') & (df['Date'] < '2020-09-01')]
			period = 'Date'
			locator = mdates.DayLocator(interval=10)
			locator_min = mdates.DayLocator(interval=7)
		elif okres == 'Wrzesień, Październik, Listopad':
			df = df[(df['Date'] >= '2020-09-01') & (df['Date'] < '2020-12-01')]
			period = 'Date'
			locator = mdates.DayLocator(interval=10)
			locator_min = mdates.DayLocator(interval=7)
		elif okres == 'Grudzień, Styczeń, Luty':
			df = df[(df['Date'] >= '2020-12-01')]
			period = 'Date'
			locator = mdates.DayLocator(interval=10)
			locator_min = mdates.DayLocator(interval=7)
			
		if per == 'Ogólna liczba przypadków (tygodniowo)':
			way = "Cases"
		elif per == 'Liczba przypadków na 100 tys mieszkańców':
			way = "Cases_Per_100k"

		sns.set_style('dark')

		fig, ax = plt.subplots()
		fig.set_size_inches(10,5)
		sns.lineplot(ax=ax,data=df[df['Country']==country], x=pd.to_datetime(df[df['Country']==country][period]), y=way)
		formatter = mdates.DateFormatter('%d-%m-%Y')
		ax.xaxis.set_major_formatter(formatter)
		ax.xaxis.set_major_locator(locator)
		ax.xaxis.set_minor_locator(locator_min)

		ax.set_title('Kraj: {}, okres: {}, sposób: {}'.format(country,okres,per))
		plt.grid()
		plt.show()

	# TOP 10 --------------------

	def raport_top10(self):

		df1 = self.create_df()
		try:
			df2 = self.create_df2()
		except JSONDecodeError:
			print("API nie odpowiada")
		except:
			print('API nie odpowiada')

		choice = str(self.comboBox4.currentText())
		if choice == '10 krajów z najwyższą sumą wszystkich przypadków':
			df = pd.DataFrame(df2[['Country', 'TotalCases']]).sort_values(by='TotalCases',ascending=False).head(10)
			x='Country'
			y='TotalCases'
			
		elif choice == '10 krajów z najwyższą sumą wszystkich zgonów':
			df = pd.DataFrame(df2[['Country', 'TotalDeaths']]).sort_values(by='TotalDeaths',ascending=False).head(10)
			x='Country'
			y='TotalDeaths'
		elif choice == '10 krajów z najwyższą sumą przypadków w ciągu ostatnich 7 dni':
			df = pd.DataFrame(df1[['Country', 'Cases']]).sort_values(by='Cases',ascending=False).drop_duplicates(subset=['Country']).head(10)
			x='Country'
			y='Cases'
		
		elif choice == '10 krajów z największą liczbą aktywnych przypadków':
			# wyrzuciłam te kraje które nie podają liczby wyzdrowiałych
			df=df2[df2['TotalRecovered'] != 0]
			df = pd.DataFrame(df[['Country', 'ActiveCases']]).sort_values(by='ActiveCases',ascending=False).head(10)
			x='Country'
			y='ActiveCases'
		elif choice == '10 krajów z najwyższą liczbą przypadków na 100 tysięcy mieszkańców':
			df = pd.DataFrame(df1[['Country', 'Cases_Per_100k']]).sort_values(by='Cases_Per_100k',ascending=False).drop_duplicates(subset=['Country']).head(10)
			x='Country'
			y='Cases_Per_100k'
			
		fig, ax = plt.subplots()
		fig.set_size_inches(10,5)
		sns.barplot(x=df[x], y=df[y], palette="Blues_d")
		ax.set_title(choice)
		ax.grid(linewidth=0.2, linestyle='-')
		ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
		ax.get_yaxis().get_major_formatter().set_scientific(False)
		plt.tight_layout()
		plt.grid()
		plt.show()

	# POROWNANIE ----------------------------

	def porownaj(self):
		country1 = str(self.comboBox5.currentText())
		country2 = str(self.comboBox6.currentText())
		period = str(self.comboBox1.currentText())
		way = str(self.comboBox2.currentText())

		df = self.create_df()

		if period == 'Caly rok':
			period = 'Date'
			locator = mdates.DayLocator(interval=30)
			locator_min = mdates.DayLocator(interval=10)
		elif period == 'Marzec, Kwiecień, Maj':
			df = df[df['Date']< '2020-06-01']
			period = 'Date'
			locator = mdates.DayLocator(interval=10)
			locator_min = mdates.DayLocator(interval=7)
		elif period == 'Czerwiec, Lipiec, Sierpień':
			df = df[(df['Date'] >= '2020-06-01') & (df['Date'] < '2020-09-01')]
			period = 'Date'
			locator = mdates.DayLocator(interval=10)
			locator_min = mdates.DayLocator(interval=7)
		elif period == 'Wrzesień, Październik, Listopad':
			df = df[(df['Date'] >= '2020-09-01') & (df['Date'] < '2020-12-01')]
			period = 'Date'
			locator = mdates.DayLocator(interval=10)
			locator_min = mdates.DayLocator(interval=7)
		elif period == 'Grudzień, Styczeń, Luty':
			df = df[(df['Date'] >= '2020-12-01')]
			period = 'Date'
			locator = mdates.DayLocator(interval=10)
			locator_min = mdates.DayLocator(interval=7)
			
		if way == 'Ogólna liczba przypadków (tygodniowo)':
			way = "Cases"
		elif way == 'Liczba przypadków na 100 tys mieszkańców':
			way = "Cases_Per_100k"
		
		fig, ax = plt.subplots()
		fig.set_size_inches(10,5)
		sns.lineplot(ax=ax, data=df[(df['Country']==country1) | (df['Country']==country2)], x=pd.to_datetime(df[(df['Country']==country1) | (df['Country']==country2)][period]), y=way, hue="Country")
		formatter = mdates.DateFormatter('%d-%m-%Y')
		ax.xaxis.set_major_formatter(formatter)
		ax.xaxis.set_major_locator(locator)
		ax.xaxis.set_minor_locator(locator_min)

		period = str(self.comboBox1.currentText())
		way = str(self.comboBox2.currentText())
		ax.set_title('Kraje: 1:{}, 2:{}, okres: {}, sposób: {}'.format(country1,country2,period,way))
		plt.grid()
		plt.show()

	def mapa(self):
		gdf = gpd.read_file('countries/99bfd9e7-bb42-4728-87b5-07f8c8ac631c2020328-1-1vef4ev.lu5nk.shp')
		gdf.loc[((gdf['CNTRY_NAME'] == 'Vietnam')), 'CNTRY_NAME'] = 'Viet Nam'
		gdf.loc[((gdf['CNTRY_NAME'] == 'Venezuela')), 'CNTRY_NAME'] = 'Venezuela (Bolivarian Republic)'
		gdf.loc[((gdf['CNTRY_NAME'] == 'United States')), 'CNTRY_NAME'] = 'United States of America'
		gdf.loc[((gdf['CNTRY_NAME'] == 'Tanzania')), 'CNTRY_NAME'] = 'Tanzania, United Republic of'
		gdf.loc[((gdf['CNTRY_NAME'] == 'Taiwan')), 'CNTRY_NAME'] = 'Taiwan, Republic of China'
		gdf.loc[((gdf['CNTRY_NAME'] == 'Syria')), 'CNTRY_NAME'] = 'Syrian Arab Republic (Syria)'
		gdf.loc[((gdf['CNTRY_NAME'] == 'American Samoa')), 'CNTRY_NAME'] = 'Samoa'
		gdf.loc[((gdf['CNTRY_NAME'] == 'St. Vincent and the Grenadines')), 'CNTRY_NAME'] = 'Saint Vincent and Grenadines'
		gdf.loc[((gdf['CNTRY_NAME'] == 'St. Lucia')), 'CNTRY_NAME'] = 'Saint Lucia'
		gdf.loc[((gdf['CNTRY_NAME'] == 'St. Kitts and Nevis')), 'CNTRY_NAME'] = 'Saint Kitts and Nevis'
		gdf.loc[((gdf['CNTRY_NAME'] == 'Russia')), 'CNTRY_NAME'] = 'Russian Federation'
		gdf.loc[((gdf['CNTRY_NAME'] == 'Myanmar')), 'CNTRY_NAME'] = 'Myanmar (Burma)'
		gdf.loc[((gdf['CNTRY_NAME'] == 'Macedonia')), 'CNTRY_NAME'] = 'Macedonia, Republic of'
		gdf.loc[((gdf['CNTRY_NAME'] == 'South Korea')), 'CNTRY_NAME'] = 'Korea (South)'
		gdf.loc[((gdf['CNTRY_NAME'] == 'Iran')), 'CNTRY_NAME'] = 'Iran, Islamic Republic of'
		gdf.loc[((gdf['CNTRY_NAME'] == 'Congo')), 'CNTRY_NAME'] = 'Congo (Kinshasa)'
		try:
			df = self.create_df2()
		except JSONDecodeError:
			print("API nie odpowiada")
		except:
			print('API nie odpowiada')
		df = df.merge(gdf, left_on='Country', right_on='CNTRY_NAME')
		crs = {'init': 'epsg:4326'}
		geometry = df['geometry']
		df = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)
		map = KeplerGl(height=800)
		map.add_data(data=df, name='Covid')
		map.save_to_html()


def window():
	app = QApplication(sys.argv)
	win = MainWindow()
	win.show()
	sys.exit(app.exec_())

window()
