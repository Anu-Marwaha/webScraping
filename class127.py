from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

START_URL = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"

browser = webdriver.Chrome("./chromedriver.exe")
browser.get(START_URL)


header=["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date"]
soup = BeautifulSoup(browser.page_source, "html.parser")

ul_Tags=soup.find_all("ul", attrs={"class", "exoplanet"})

planent_info=[]

def scrape():
    for i in range(1,3):
        time.sleep(2)
        for ul_tag in ul_Tags:
            li_tags=ul_tag.find_all("li")
            
            new_planet=[]
            for index,li_tag in enumerate(li_tags):

                if index==0:
                    #print("index" ,index,"=",li_tag.find_all("a")[0].contents[0])
                    data=li_tag.find_all("a")[0].contents[0]
                    new_planet.append(data)
                else:
                    #print("index" ,index,"=",li_tag.contents[0])
                    data=li_tag.contents[0]
                    new_planet.append(data)
            
            planent_info.append(new_planet)

        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]').click()
        print("page no",i,"done")

    #print(planent_info)

scrape()

with open("planentInfo.csv","w") as f:
    csvWriter=csv.writer(f)
    csvWriter.writerow(header)
    csvWriter.writerows(planent_info)

data=[]

with open("planentInfo.csv","r") as input:
    input_csvRead=csv.reader(input)
    for row in input_csvRead:
        #print("row1=",row[0])
        if any(field for field in row):
            data.append(row)

with open("FinalplanentInfo.csv","w",newline='') as output:
    output_csvWrite=csv.writer(output)
    output_csvWrite.writerows(data)

