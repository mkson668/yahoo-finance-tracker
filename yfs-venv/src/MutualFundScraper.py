import pandas as pd
from bs4 import BeautifulSoup
import csv
import requests


class MutualFundScraper:
    names = []
    changes = []
    percentChanges = []
    prices_intraday = []
    fifty_day_avg = []
    twohundred_day_avg = []
    three_month_ret = []
    YTD_ret = []

    mfURL = ""

    def __init__(self):
        self.mfURL = "https://in.finance.yahoo.com/mutualfunds"

    def scrape(self):
        r = requests.get(self.mfURL)
        if r.status_code == 200:
            r.close()
            for i in range(0,601,100):
                url = self.mfURL + "?count=100&offset=" + str(i)
                r = requests.get(url)
                data = r.text
                soup = BeautifulSoup(data, features="html.parser")
                for mtflistings in soup.findAll('tbody'):
                    for mtflisting in mtflistings.contents:
                        self.names.append(mtflisting.contents[1].text)
                        self.changes.append(mtflisting.contents[2].text)
                        self.percentChanges.append(mtflisting.contents[3].text)
                        self.prices_intraday.append(mtflisting.contents[4].text)
                        self.fifty_day_avg.append(mtflisting.contents[5].text)
                        self.twohundred_day_avg.append(mtflisting.contents[6].text)
                        self.three_month_ret.append(mtflisting.contents[7].text)
                        self.YTD_ret.append(mtflisting.contents[8].text)
                    
        else:
            raise Exception("could not retreive data status code: " + r.status_code)

        mtf_dataframe = pd.DataFrame(data={"Name": self.names, 
        "Changes": self.changes, 
        "percent change": self.percentChanges, 
        "intraday price": self.prices_intraday, 
        "50 day avg": self.fifty_day_avg, 
        "200 day avg": self.twohundred_day_avg,
        "3 month return": self.three_month_ret,
        "YTD return": self.YTD_ret})
        print(mtf_dataframe)
        return