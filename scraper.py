import os
import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

# setup the file
date = datetime.datetime.now().strftime("%d, %A, %b, %Y")
folder = datetime.datetime.now().strftime("%Y %m%b")
filepath = Path("Outputs/" + folder)

if not os.path.exists(filepath):
    os.makedirs(filepath)

filename = Path("Outputs/" + folder + "/DailyHeadlines - " + date + ".csv")
f = open(filename, "w")

headers = "Website, Headline, Link\n"
f.write(headers)

# array of websites to scrape
newspages = ["https://www.bbc.com/news/world", # BBC
"https://www.reuters.com/", # Reutuers
"https://www.nytimes.com/section/world", # NYT
"https://www.theguardian.com/world", # Guardian
"https://www.rt.com/news/", # RT
"https://www.wsj.com/news/world"] # WSJ

index = 0

for newspage in newspages:

    # open a connection and grab the page

    req = Request(newspages[index], headers={'User-Agent': 'Mozilla/5.0'})

    uClient = urlopen(req)
    htmlPage = uClient.read()
    uClient.close()

    # parse the html
    soupPage = soup(htmlPage, "html.parser")

    # check for BBC
    if index == 0:

        # grab each headline container
        containers = soupPage.findAll("a", {"class":"gs-c-promo-heading"})

        # write the headline and link to .csv
        for container in containers:

            website = "BBC World News"

            try:
                headline = container.text.strip()
            except:
                headline = "null"

            try:
                link = "=HYPERLINK(\"https://www.bbc.com" + container.get("href") + "\")"
            except:
                link = "null"

            f.write(website + "," + headline.replace(",", "|").replace("Video", "(Video) ") + "," + link + "\n")

    #check for Reutuers
    if index == 1:

        # grab each headline container
        containers = soupPage.findAll("h3", {"class":"article-heading"})
        containers.extend(soupPage.findAll("div", {"class":"story-content"}))
        containers.extend(soupPage.findAll("article", {"class":"story-content"}))

        # write the headline and link to .csv
        for container in containers:

            website = "Reutuers"
            
            try:
                headline = container.a.h3.text
            except:
                try:
                    headline = container.h3.a.text
                except:
                    try:
                        headline = container.a.text
                    except:
                        headline = "null"

            try:
                link = "=HYPERLINK(\"https://www.reuters.com" + container.a.get("href") + "\")"
            except:
                link = "null"

            f.write(website + "," + headline.replace(",", "|").replace("\n", "") + "," + link + "\n")

    # check for NYT
    if index == 2:

        # grab each headline container
        containers = soupPage.findAll("div", {"class":["css-10wtrbd","css-1l4spti"]})

        # write the headline and link to .csv
        for container in containers:

            website = "The New York Times"
            
            try:
                headline = container.h2.a.text
            except:
                try:
                    headline = container.a.h2.text
                except:
                    passheadline = "null"

            try:
                link = "=HYPERLINK(\"https://www.nytimes.com" + container.h2.a.get("href") + "\")"
            except:
                try:
                    link = "=HYPERLINK(\"https://www.nytimes.com" + container.a.get("href") + "\")"
                except:
                    link = "null"            

            f.write(website + "," + headline.replace(",", "|") + "," + link + "\n")

    # check for Guardian
    if index == 3:

        # grab each headline container
        containers = soupPage.findAll("h3", {"class":"fc-item__title"})

        # write the headline and link to .csv
        for container in containers:

            website = "The Guardian"
            
            try:
                headline = container.a.text.strip()
            except:
                headline = "null"

            try:
                link = "=HYPERLINK(\"" + container.a.get("href") + "\")"
            except:
                link = "null"


            f.write(website + "," + headline.replace(",", "|").replace("\n", "") + "," + link + "\n")

    # check for RT
    if index == 4:

        # grab each headline container
        containers = soupPage.findAll("strong", {"class":"card__header"})

        # write the headline and link to .csv
        for container in containers:

            website = "RT"
            
            try:
                headline = container.a.text.strip()
            except:
                headline = "null"

            try:
                link = "=HYPERLINK(\"https://www.rt.com" + container.a.get("href") + "\")"
            except:
                link = "null"

            f.write(website + "," + headline.replace(",", "|") + "," + link + "\n")

    # check for WSJ
    if index == 5:

        # grab each headline container
        containers = soupPage.findAll("div", {"class":"WSJTheme--headline--7VCzo7Ay"})
        containers.extend(soupPage.findAll("a", {"class":"style--link--1n1ZR5I9"}))

        # write the headline and link to .csv
        for container in containers:

            website = "Wall Street Journal"
            
            try:
                headline = container.h2.a.text
            except:
                try:
                   headline = container.h3.a.text
                except:
                    try:
                        headline = container.h3.span.text.strip()
                    except:
                        headline = "null"

            try:
                link = "=HYPERLINK(\"" + container.h2.a.get("href") + "\")"
            except:
                try:
                    link = "=HYPERLINK(\"" + container.h3.a.get("href") + "\")"
                except:
                    try:
                        link = "=HYPERLINK(\"" + container.get("href") + "\")"
                    except:
                        link = "null"

            f.write(website + "," + headline.replace(",", "|") + "," + link + "\n")

    index +=1

f.close()