from flask import Flask, redirect, url_for, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        url = request.form["url"]

        if ("mojauto.rs" not in url) or (url.split('/')[3] != "polovni-automobili"):
            return render_template("error_not_a_car.html") # basic url validity check

        return render_template("index.html", data=scrape(url))
    else:
        return render_template("base.html")

def scrape(link):
    data = []
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    main = soup.find('div', class_='breadcrumb breadcrumbsingle')
    breadcrumbs = main.find_all('span')
    data.append(breadcrumbs[2].text.strip()) # manufacturer
    data.append(breadcrumbs[3].text.strip()) # model

    main1 = soup.find(id='sidebar')
    price = main1.find('span', class_='priceReal')
    data.append(price.text.strip()) # price

    main2 = main1.find('ul', class_='basicSingleData')
    li = main2.find_all('li')

    for item in li:
        stats = item.find_all('span')
        for span in stats:
            data.append(span.text.strip()) # other specifications

    if len(data) == 10: # ############
        data.pop(9) # removing unneccesary information
    data.pop(7) ###########

    mainImg = soup.find(id='galleryDialogImageContainer') # getting image
    data.append("https://www.mojauto.rs" + mainImg.img['src'])

    data[2] = data[2].split()[0] # formatting price
    data[3] = data[3].split()[0][0:4] # formatting year
    data[4] = data[4].split()[0] # formatting engine cm3

    return data

if __name__ == "__main__":
    app.run(debug=True)   