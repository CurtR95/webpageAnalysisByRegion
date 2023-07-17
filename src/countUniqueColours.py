import cv2
import numpy as np
import pandas

def countUniqueColours(countries):
    for country in countries:
        df = pandas.read_csv("data/"+country+"/popular_websites.csv");
        for i in range(len(df['website'])):
            if df.loc[i, 'screenShotTaken'] == "True":
                # set variables
                website = df.loc[i,'website'];
                print(website);
                screenshotSrc = cv2.imread("data/"+country+"/"+website+".png");
                unique, counts = np.unique(screenshotSrc.reshape(-1, screenshotSrc.shape[-1]), axis=0, return_counts=True)
                df.loc[i, 'numberOfColours'] = counts.size;
                df.to_csv("data/"+country+"/popular_websites.csv", index=False)
