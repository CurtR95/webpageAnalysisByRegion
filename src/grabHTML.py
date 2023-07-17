from bs4 import BeautifulSoup;
import re;

def grabHTML(driver, country, website):
    soup = BeautifulSoup(driver.page_source, 'html.parser');
    with open("data/"+country+"/"+website+".html", "w", encoding="utf-8") as file:
        file.write(str(soup))
    imgCount = len(soup.find_all("svg")) + len(soup.find_all("img"));
    count = 0;
    arrayOfText = [];
    regex = re.compile('[^ぁ-ゔァ-ヴー一-龠a-zA-Z0-9ａ-ｚＡ-Ｚ０-９々〆〤ヶ]')
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
    for i in arrayOfText:
        if i != "":
            count += len(i);
    return imgCount, count, website.split(".",1)[1];