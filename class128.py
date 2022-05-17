from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

START_URL = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"

browser = webdriver.Chrome("./chromedriver.exe")
browser.get(START_URL)


#header=["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date","hrefLink"]
header = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date","Links", "planet_type", "planet_radius", "orbital_radius", "orbital_period", "eccentricity"]
soup = BeautifulSoup(browser.page_source, "html.parser")

ul_Tags=soup.find_all("ul", attrs={"class", "exoplanet"})

planent_info=[]

def scrape():
    for i in range(1,3):
        time.sleep(2)
        for ul_tag in ul_Tags:
            li_tags=ul_tag.find_all("li")
            
            new_planet=[]
            nextPageHrefLink="https://exoplanets.nasa.gov"
            for index,li_tag in enumerate(li_tags):

                if index==0:
                    #print("index" ,index,"=",li_tag.find_all("a")[0].contents[0])
                    data=li_tag.find_all("a")[0].contents[0]
                    new_planet.append(data)
                    nextPageHrefLink=nextPageHrefLink+li_tag.find_all("a")[0]["href"]
                else:
                    #print("index" ,index,"=",li_tag.contents[0])
                    data=li_tag.contents[0]
                    new_planet.append(data)
            
            new_planet.append(nextPageHrefLink)
            planent_info.append(new_planet)

            scrapeMoreData(nextPageHrefLink)
            

        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]').click()
        print("page no",i,"done")

    #print(planent_info)

planet_ExtraInfo=[]
def scrapeMoreData(link):
    time.sleep(2)
    #browser2 = webdriver.Chrome("./chromedriver.exe")
    #browser2.get(link)
    #soup2 = BeautifulSoup(browser2.page_source, "html.parser")
    
    page = requests.get(link)
    soup2 = BeautifulSoup(page.content, "html.parser")

    
    time.sleep(2)
    temp_list = []
    for tr_tag in soup2.find_all("tr", attrs={"class": "fact_row"}):
        td_tags = tr_tag.find_all("td")
        for td_tag in td_tags:
            try:
                tempdata=td_tag.find_all("div", attrs={"class": "value"})[0].contents[0]
                
                temp_list.append(tempdata.strip())
                #print("tempData=",tempdata.strip())
            except:
                temp_list.append("")
    #planet_data.append(temp_list)
    print("tempdata=",temp_list)
    #print("planent data",planet_data)
    planet_ExtraInfo.append(temp_list)


scrape()

complete_planet_data = []
print("before")
for index, data in enumerate(planent_info):
    new_planet_data_element = planet_ExtraInfo[index]
    new_planet_data_element = [elem.replace("\n", "") for elem in new_planet_data_element]
    new_planet_data_element = new_planet_data_element[:7]
    #print("new data",new_planet_data_element)
    complete_planet_data.append(data + new_planet_data_element)



with open("planentInfo.csv","w") as f:
    csvWriter=csv.writer(f)
    csvWriter.writerow(header)
    csvWriter.writerows(complete_planet_data)

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

