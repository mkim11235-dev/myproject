from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import http.client
import json
from datetime import datetime
from pathlib import Path
import pandas as pd
import csv
import matplotlib.figure as Figure
from io import BytesIO
import base64


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data")
def data():
    url = "https://api.usa.gov/crime/fbi/cde/shr/national/victim/relationship?from=1980&to=2024&API_KEY=iiHnOKfno2Mgkt5AynpvPpUQTEyxE77jo1RU8PIv"


    querystring = {"variable":"relationship","collection":"victim","from":"1980","to":"2024"}

    response = requests.get(url, params=querystring)
    news_results = response.json()

    keys = ['data_year'] + news_results['keys']
    data = news_results['data']

    with open('Names.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    df = pd.read_csv('Names.csv')
    gf_df= df.drop(['Friend','Acquaintance','Boyfriend', 'Brother', 'Common-Law Husband','Daughter','Employee','Employer','Ex-Husband','Father','Homosexual Relationship','Husband', 'In-Law', 'Mother', 'Neighbor', 'Other Family', 'Other - known to victim', 'Sister', 'Son', 'Stepdaugther', 'Stepfather', 'Stepson', 'Stepmother', 'Stranger', 'Unknown'], axis=1)
    gf_df['Female Partner'] = gf_df[['Common-Law Wife','Ex-Wife', 'Girlfriend', 'Wife']].sum(axis=1)
    df_2 = gf_df.drop(['Common-Law Wife','Ex-Wife', 'Girlfriend', 'Wife'], axis=1)
    data = df_2
    labels = df_2['data_year']
    values = df_2['Female Partner']

    '''bf_df= df.drop(['Friend','Acquaintance','Girlfriend', 'Brother', 'Common-Law Wife','Daughter','Employee','Employer','Ex-Wife','Father','Homosexual Relationship','Wife', 'In-Law', 'Mother', 'Neighbor', 'Other Family', 'Other - known to victim', 'Sister', 'Son', 'Stepdaugther', 'Stepfather', 'Stepson', 'Stepmother', 'Stranger', 'Unknown'], axis=1)
    bf_df['Male Partner'] = bf_df[['Common-Law Husband','Ex-Husband', 'Boyfriend', 'Husband']].sum(axis=1)
    df_3 = bf_df.drop(['Common-Law Husband','Ex-Husband', 'Boyfriend', 'Husband'], axis=1)'''

    return render_template("data.html", news_results = news_results, labels=labels,values=values)



'''def scrape_news():
    url = "https://www.foodpro.huds.harvard.edu/foodpro/menu_items.asp?date=4-20-2024&type=30&meal=1"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    menu_items = []
    for item in soup.find_all(class_="menu_item"):
        menu_items.append(item.text.strip())
    return menu_items

if __name__ == "__main__":
    app.run(debug=True)

'''
