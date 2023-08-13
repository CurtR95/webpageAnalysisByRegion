from selenium import webdriver
from src.xpath_soup import xpath_soup;
from bs4 import BeautifulSoup;
import pandas;
import os;

def getTop100(countries):
    """
    This function will get the top 100 websites for each country
    :param countries: a list of countries to iterate through
    :type countries: list
    """
    driver = webdriver.Chrome();
    # initialize a dictionary to store the information
    d = {
        'country':[],
        'website':[],
        'visits':[]
    }
    print(countries);
    # iterate through that list
    for country in countries:
        # follow semrush's URL formatting and plug in the country using a formatted string
        url = f'https://www.semrush.com/trending-websites/{country}/all'
        # navigate to the URL using Selenium Webdriver
        driver.get(url)
        # feed the page information into BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # while the table has less than 100 rows, click the "Show 20 more" button
        while len(soup.find("table").find("tbody").find_all("tr")) < 100:
            a = soup.find_all("button");
            for i in a:
                if i.text == "Show 20 more":
                    print(i);
                    xpath_soup(i);
                    driver.find_element("xpath", xpath_soup(i)).click();
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    break;
        # iterate through the table and save the information into the dictionary
        results = {
            'country':[],
            'website':[],
            'visits':[],
            'emptyCell':[]
        }
        # iterate through the table and save the information into the dictionary
        for x in soup.find("table").find("tbody").find_all("tr"):
            results['country'].append(country);
            results['website'].append(x.find_all("td")[1].find("a").text);
            results['visits'].append(x.find_all("td")[2].text);
            results['emptyCell'].append("N/A");
        # feed the results into the dictionary
        d['country'] = results['country']
        d['website'] = results['website']
        d['visits'] = results['visits']
        d['screenShotTaken'] = results['emptyCell']
        d['imgCount'] = results['emptyCell']
        d['letterCount'] = results['emptyCell']
        d['domainLoc'] = results['emptyCell']
        d['numberOfColours'] = results['emptyCell']
        # save this into some sort of file
        df = pandas.DataFrame(d);
        # create a folder for the country if it doesn't exist
        if not os.path.exists("data/"+country): os.mkdir("data/"+country);
        saveString = "data/"+country+"/popular_websites.csv";
        df.to_csv(saveString, index=False)
    driver.quit();