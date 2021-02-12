import pandas as pd
from bs4 import BeautifulSoup
import csv
import requests

class CryptoCurrencyScraper:
    names = []
    prices = []
    changes = []
    percentChanges = []
    volumeInCurrencyTwentyFourHour = []
    circulatingSupply = []

    cryptoCurrencyURL = ""

    def __init__(self):
        self.cryptoCurrencyURL = "https://in.finance.yahoo.com/cryptocurrencies"

    def scrape(self):
        r = requests.get(self.cryptoCurrencyURL)
        if r.status_code == 200:
            r.close()
            for i in range(0,376,25):
                url = self.cryptoCurrencyURL + "?count=25&offset=" + str(i)
                r = requests.get(url)
                data = r.text
                soup = BeautifulSoup(data, features="html.parser")
                for cclistings in soup.findAll('tbody'):
                    for cclisting in cclistings.contents:
                        self.names.append(cclisting.contents[1].text)
                        self.prices.append(cclisting.contents[2].text)
                        self.changes.append(cclisting.contents[3].text)
                        self.percentChanges.append(cclisting.contents[4].text)
                        self.volumeInCurrencyTwentyFourHour.append(cclisting.contents[7].text)
                        self.circulatingSupply.append(cclisting.contents[9].text)
        else:
            raise Exception("could not retreive data status code: " + r.status_code)

        cc_dataframe = pd.DataFrame(data={
            "Name": self.names,
            "Price": self.prices, 
            "Changes": self.changes,
            "Percent Changes": self.percentChanges,
            "Trade Volume (24hr)": self.volumeInCurrencyTwentyFourHour,
            "Circulating supply": self.circulatingSupply
        })
        print(cc_dataframe)
        return