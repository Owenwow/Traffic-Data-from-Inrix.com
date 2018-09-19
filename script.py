from bs4 import BeautifulSoup
import urllib.request as urllib2
import pandas as pd
import requests
import lxml
import csv

#Reading the file locally.
with open('soup.txt','rt', encoding='utf-8') as f:
   soup = BeautifulSoup(f,"lxml")

#Function of Extracting Country from text.
def GetCountry(text):
    text2 = text.split(" ")
    if text2[0]+ text2[1] in ["NorthAmerica","SouthAmerica"] and 'Mega' in text:
        return text[(text.find("America")+len('America')): text.find("Mega")].strip()
    elif text2[0]+ text2[1] in ["NorthAmerica","SouthAmerica"] and "  " in text:
        return text[(text.find("America")+len('America')): text.find("  ")].strip()
    elif text2[0]+ text2[1] in ["NorthAmerica","SouthAmerica"]:
        return text[(text.find("America")+len('America')):].strip()
    
    if text2[0] in ['Asia', 'Europe', 'Africa'] and 'Mega' in text:
        return text[(text.find(text2[0])+len(text2[0])): text.find("Mega")].strip()
    elif text2[0] in ['Asia', 'Europe', 'Africa'] and "  " in text:
        return text[(text.find(text2[0])+len(text2[0])): text.find("  ")].strip()
    else:
        return text[(text.find(text2[0])+len(text2[0])):].strip()


#Generating Dataset from the soup.
#Because of features of this soup, I divided into two parts: 1-200, 200-end.
with open('traffic_by_city1.csv', 'w', encoding='UTF-8', newline='') as fd:
    writer = csv.writer(fd)
    writer.writerow(["City", "Country", "2017 All Cities Rank",
                  "2017 Inrix Traffic Scorecard Rank", "Hours Spent in Congestion",
                  "ICI", "Peak", "Daytime", "Overall"])
#Part I
    for i in range(1,201):
        contain=soup.findAll("tr",{"data-value":i})[0].text.strip()
        row = [
                contain.split("\n")[0].split(", ")[0],
                GetCountry(contain.split("\n")[1].strip()),
                contain.split("\n")[4].split(' (')[0].strip(),
                contain.split("\n")[7].split(' (')[0].strip(),
                contain.split("\n")[10].strip(),
                contain.split("\n")[11].strip(),
                contain.split("\n")[12].strip(),
                contain.split("\n")[13].strip(),
                contain.split("\n")[14].strip()
              ]
        writer.writerow(row)
        
#Part II
    containers = soup.findAll("tr",{"data-value":""})[1:]
    for contain2 in containers:
        a = contain2.text.split("\n")
        row = [
                a[4].split(", ")[0],
                GetCountry(a[5].strip()),
                a[8].split(' (')[0].strip(),
                a[11].split(' (')[0].replace('—','-').strip(),
                a[14].strip(),
                a[15].strip(),
                a[16].strip(),
                a[17].strip(),
                a[18].strip()
             ]
        writer.writerow(row)

