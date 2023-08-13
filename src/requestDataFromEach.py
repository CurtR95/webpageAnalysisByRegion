from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from src.grabHTML import grabHTML
import time;
import pandas;

chromeLanguages = {
    "jp": "ja_JP",
    "gb": "en_GB",
    "us": "en_US",
    "cn": "zh_CN",
    "kr": "ko_KR"
}


def requestDataFromEach(countries):
    """
    This function will count images and text for each website and call grabHTML.
    :param countries: a list of countries to iterate through
    :type countries: list
    """
    # iterate through the countries
    for country in countries:
        # initialize the webdriver
        service = Service();
        options = webdriver.ChromeOptions();
        options.add_argument("start-maximized");
        options.add_argument("lang="+chromeLanguages[country]);
        driver = webdriver.Chrome(service=service, options=options);
        # read the CSV file
        df = pandas.read_csv("data/"+country+"/popular_websites.csv")
        # request user to connect to VPN
        input("Please Ensure that a VPN is connected the current country is "+country+". Press Enter to continue...\n")
        # iterate through websites
        for i in range(len(df['website'])):
            # if the screenshot has not been taken
            if df.loc[i, 'screenShotTaken'] != "True":
                # if the screenshot is not broken
                if df.loc[i, 'screenShotTaken'] != "Broken":
                    # set variables
                    website = df.loc[i,'website'];
                    # amend the url to include https://www.
                    if website[:8] == "https://":
                        url = website;
                    elif website[:4] == "www.":
                        url = f'https://' + website;
                    else:
                        url = f'https://www.' + website;
                    print(url);
                    try:
                        # navigate to the URL using Selenium Webdriver
                        driver.get(url);
                        # wait for the page to load
                        time.sleep(20);
                        # save the screenshot
                        if website[:8] == "https://":
                            string = website[8:];
                        elif website[:4] == "www.":
                            string = website[4:];
                        else:
                            string = website;
                        driver.save_screenshot("data/"+country+"/"+string+".png");
                        # grab the HTML and data from the page
                        imgCount, letterCount, domainLoc = grabHTML(driver, country, website);
                        # update the CSV file
                        df.loc[i, 'screenShotTaken'] = "True";
                        df.loc[i, 'imgCount'] = imgCount;
                        df.loc[i, 'letterCount'] = letterCount;
                        df.loc[i, 'domainLoc'] = domainLoc;
                        df.to_csv("data/"+country+"/popular_websites.csv", index=False)
                    except WebDriverException:
                        print("WebDriverException");
                        df.loc[i, 'screenShotTaken'] = "Broken";
                        df.to_csv("data/"+country+"/popular_websites.csv", index=False)
                        continue;
        driver.quit();