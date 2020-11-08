import os
import datetime
import urllib.request as request
from pathlib import Path
from bs4 import BeautifulSoup as soup

# setup the file
date = datetime.datetime.now().strftime("%A, %d, %b, %Y")
folder = datetime.datetime.now().strftime("%Y %b")
filepath = Path("Outputs/" + folder)

if not os.path.exists(filepath):
    os.makedirs(filepath)

filename = Path("Outputs/" + folder + "/DailyHeadlines - " + date + ".csv")
f = open(filename, "w")

headers = "Website, Headline, Link\n"
f.write(headers)

# array of websites to scrape
newspages = ["https://www.bbc.com/news/world", # BBC
"https://edition.cnn.com/world", # CNN
"https://www.nytimes.com/section/world", # NYT
"https://www.theguardian.com/world", # Guardian
"https://www.rt.com/news/"] # RT

index = 0

for newspage in newspages:

    # open a connection and grab the page
    uClient = request.urlopen(newspages[index])
    htmlPage = uClient.read()
    uClient.close()

    # parse the html
    soupPage = soup(htmlPage, "html.parser")

    # check for BBC
    if index == 0:

        # grab each headline
        containers = soupPage.findAll("a", {"class":"gs-c-promo-heading"})

        # write the headline to .csv file
        for container in containers:

            website = "BBC World News"

            try:
                headline = container.text.strip()
            except:
                headline = ""

            f.write(website + "," + headline.replace(",", "|").replace("Video", "(Video) ") + "\n")

    #check for CNN
    if index == 1:

        # grab each headline
        containers = soupPage.findAll("h3", {"class":"cd__headline"}) # not finding all

        # write the headline to .csv file
        for container in containers:

            website = "CNN World News"
            
            try:
                headline = container.a.span.text
            except:
                headline = ""

            f.write(website + "," + headline.replace(",", "|") + "\n")

    # check for NYT
    if index == 2:

        # grab each headline
        containers = soupPage.findAll("div", {"class":["css-10wtrbd","css-1l4spti"]})

        # write the headline to .csv file
        for container in containers:

            website = "The New York Times"
            
            try:
                headline = container.h2.a.text
            except:
                headline = ""

            if headline == "":
                try:
                    headline = container.a.h2.text
                except:
                    pass

            f.write(website + "," + headline.replace(",", "|") + "\n")

    # check for Guardian
    if index == 3:

        # grab each headline
        containers = soupPage.findAll("h3", {"class":"fc-item__title"})

        # write the headline to .csv file
        for container in containers:

            website = "The Guardian"
            
            try:
                headline = container.a.text.strip()
            except:
                headline = ""

            f.write(website + "," + headline.replace(",", "|").replace("\n", "") + "\n")

    # check for RT
    if index == 4:

        # grab each headline
        containers = soupPage.findAll("strong", {"class":"card__header"})

        # write the headline to .csv file
        for container in containers:

            website = "RT"
            
            try:
                headline = container.a.text.strip()
            except:
                headline = ""

            f.write(website + "," + headline.replace(",", "|") + "\n")   
    
    index +=1

f.close()