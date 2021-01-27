import pandas as pd
from bs4 import BeautifulSoup
import csv
import requests


class CurrencyScraper:
    names = []
    prices = []
    changes = []
    percentChanges = []
    currencyURL = ""

    def __init__(self):
        self.currencyURL = "https://ca.finance.yahoo.com/currencies"

    def scrape(self):
        r = requests.get(self.currencyURL)
        if r.status_code == 200:
            data = r.text
            soup = BeautifulSoup(data, features="html.parser")

            for currencylistings in soup.findAll('tbody'):
                for currencylisting in currencylistings.contents:
                    names.append(currencylisting.contents[1].text)
                    prices.append(currencylisting.contents[2].text)
                    changes.append(currencylisting.contents[3].text)
                    percentChanges.append(currencylisting.contents[4].text)
        else:
            raise Exception("could not retreive data status code: " + r.status_code)

        currency_dataframe = pd.DataFrame(data={"Name": names, "Prices": prices, "Changes": changes, "Change Percentage": percentChanges})
        print(currency_dataframe)
        return

cs = CurrencyScraper()
cs.scrape