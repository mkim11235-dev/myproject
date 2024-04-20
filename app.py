from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data")
def data():
    menu_items = scrape_news()
    return render_template("data.html", menu_items=menu_items)

def scrape_news():
    url = "https://www.foodpro.huds.harvard.edu/foodpro/menu_items.asp?date=4-20-2024&type=30&meal=1"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    menu_items = []
    for item in soup.find_all(class_="menu_item"):
        menu_items.append(item.text.strip())
    return menu_items

if __name__ == "__main__":
    app.run(debug=True)
