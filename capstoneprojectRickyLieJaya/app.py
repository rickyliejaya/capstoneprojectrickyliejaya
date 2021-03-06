from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

table = soup.find('table', attrs={'class':'table table-striped table-hover table-hover-solid-row table-simple history-data'})
tr = table.find_all('tr')
kurs = [] #initiating a tuple

for i in range(1, len(tr)):
    row = table.find_all('tr')[i]
    
    #get bulan
    period = row.find_all('td')[0].text
    period = period.strip() #for removing the excess whitespace
    
    #get kurs
    harga = row.find_all('td')[2].text
    harga = harga.strip() #for removing the excess whitespace
    
    kurs.append((period,harga))   
#insert the scrapping process here
    
    kurs.append((period,harga)) 

kurs = kurs[::-1]

#change into dataframe
kurs_rupiah = pd.DataFrame(kurs, columns = ('period','harga'))

#insert data wrangling here
import pandas as pd
import numpy as np


kurs_rupiah['period'] = kurs_rupiah['period'].astype('datetime64')
kurs_rupiah['harga'] = kurs_rupiah['harga'].str.replace(" IDR","")
kurs_rupiah['harga'] = kurs_rupiah['harga'].str.replace(",","")
kurs_rupiah['harga'] = kurs_rupiah['harga'].astype('float64')
kurs_rupiah['harga'] = kurs_rupiah['harga'].round(2)


#end of data wranggling 

#plotting data
kurs_rupiah = kurs_rupiah.set_index('period')

@app.route("/")
def index(): 
	
	card_data = f'USD {kurs_rupiah["harga"].mean()}'

	# generate plot
	ax = kurs_rupiah.plot(figsize = (20,9))
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]


	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)
