from bs4 import BeautifulSoup;
import re;

def grabHTML(driver, country, website):
    """
    This function will grab the HTML of a website and save it to a file
    
    :param driver: the Selenium Webdriver
    :type driver: Selenium Webdriver
    :param country: the country that the website is from
    :type country: str
    :param website: the website to grab the HTML from
    :type website: str
    """
    # navigate to the URL using Selenium Webdriver
    soup = BeautifulSoup(driver.page_source, 'html.parser');
    # Strip the website of any prefixes
    if website[:8] == "https://":
        string = website[8:];
    elif website[:4] == "www.":
        string = website[4:];
    else:
        string = website;
    # Save the HTML to a file
    with open("data/"+country+"/"+string+".html", "w", encoding="utf-8") as file:
        file.write(str(soup))
    # Count the number of images and svgs
    imgCount = len(soup.find_all("svg")) + len(soup.find_all("img"));
    count = 0;
    arrayOfText = [];
    # Create a regex to find all characters, including Japanese characters
    regex = re.compile('[^ぁ-ゔァ-ヴー一-龠a-zA-Z0-9ａ-ｚＡ-Ｚ０-９々〆〤ヶ]')
    # Get all the text from the HTML
    for i in soup.findAll('p'):
        arrayOfText.append(regex.sub('', i.text));
    for i in soup.findAll('div'):
        arrayOfText.append(regex.sub('', i.text));
    for i in soup.findAll('span'):
        arrayOfText.append(regex.sub('', i.text));
    for i in soup.findAll('h1'):
        arrayOfText.append(regex.sub('', i.text));
    for i in soup.findAll('h2'):
        arrayOfText.append(regex.sub('', i.text));
    for i in soup.findAll('h3'):
        arrayOfText.append(regex.sub('', i.text));
    for i in soup.findAll('h4'):
        arrayOfText.append(regex.sub('', i.text));
    for i in soup.findAll('h5'):
        arrayOfText.append(regex.sub('', i.text));
    for i in soup.findAll('h6'):
        arrayOfText.append(regex.sub('', i.text));
    for i in soup.findAll('a'):
        arrayOfText.append(regex.sub('', i.text));
    for i in soup.findAll('li'):
        arrayOfText.append(regex.sub('', i.text));
    for i in soup.findAll('td'):
        arrayOfText.append(regex.sub('', i.text));
    for i in soup.findAll('th'):
        arrayOfText.append(regex.sub('', i.text));
    for i in soup.findAll('button'):
        arrayOfText.append(regex.sub('', i.text));
    for i in soup.findAll('label'):
        arrayOfText.append(regex.sub('', i.text));
    for i in soup.findAll('option'):
        arrayOfText.append(regex.sub('', i.text));
    # remove duplicate text
    arrayOfText = list(dict.fromkeys(arrayOfText));
    # count the number of characters
    for i in arrayOfText:
        if i != "":
            count += len(i);
    # return the number of images, the number of characters, and the website's extension
    return imgCount, count, string.split(".",1)[1];