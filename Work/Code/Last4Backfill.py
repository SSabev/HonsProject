# Borrowed from Ewan

import pandas as p
import numpy as np
import datetime as dt
from dateutil.relativedelta import relativedelta

class Analyser:
    def __init__(self, df):
        self.df = df
        self.convertdates()
        self.createblankdf()

    def convertdates(self):
        def conversion(date):
            return dt.datetime.strptime(date, '%Y-%m-%d')
        if 'Datetime' in self.df:
            self.df['Date'] = self.df.Datetime.apply(conversion)
        else:
            try:
                self.df.Date = self.df.Date.apply(conversion)
            except TypeError:
                pass

    def createblankdf(self):
        start = dt.datetime.strptime(str(self.df.Date.irow(0)), "%Y-%m-%d %H:%M:%S")

        lastdate = self.df.Date.irow(-1)
        self.lastdate = lastdate
        startdate = dt.datetime(lastdate.year, lastdate.month, 1)
        enddate = startdate + relativedelta(days=-1, months=1)
        currentdate = start
        daterange = []
        while currentdate <= lastdate:
            daterange.append(currentdate)
            currentdate = currentdate + relativedelta(days = 1)

        self.results = p.DataFrame({
            "Date" : daterange})
        self.results['Forecast'] = 0.0
        self.results = self.results.merge(self.df, how="outer")

    def backfill(self, variable):
        self.forecastdates = self.results[(self.results.Forecast == 0)
               & (np.isnan(self.results['%s'%variable]))]['Date']
        #for forecastdate in self.forecastdates:
        #    print forecastdate

        for forecastdate in self.forecastdates:
            # figure out the dates 1, 2, 3 and 4 weeks ago
            tm1 = forecastdate - relativedelta(days = 7)
            tm2 = forecastdate - relativedelta(days =14)
            tm3 = forecastdate - relativedelta(days =21)
            tm4 = forecastdate - relativedelta(days =28)

            # now figure out the values to use for the forecast
            # logic is, if there is a true value to use then use that. if there
            # isn't, then use a previously forecasted value.

            # these are the relevant rows from the data frame.
            r1 = self.results[self.results.Date == tm1]
            r2 = self.results[self.results.Date == tm2]
            r3 = self.results[self.results.Date == tm3]
            r4 = self.results[self.results.Date == tm4]

            r1 = r1.to_dict(outtype='records')
            r2 = r2.to_dict(outtype='records')
            r3 = r3.to_dict(outtype='records')
            r4 = r4.to_dict(outtype='records')

            if r1:
                r1 = r1[0]
            else:
                r1 = {'%s'%variable: np.nan, 'Forecast': 0}

            if r2:
                r2 = r2[0]
            else:
                r2 = {'%s'%variable: np.nan, 'Forecast': 0}

            if r3:
                r3 = r3[0]
            else:
                r3 = {'%s'%variable: np.nan, 'Forecast': 0}

            if r4:
                r4 = r4[0]
            else:
                r4 = {'%s'%variable: np.nan, 'Forecast': 0}



            if np.isnan(r1['%s'%variable]):
                v1 = float(r1['Forecast'])
            else:
                v1 = float(r1['%s'%variable])

            if np.isnan(r2['%s'%variable]):
                v2 = float(r2['Forecast'])
            else:
                v2 = float(r2['%s'%variable])

            if np.isnan(r3['%s'%variable]):
                v3 = float(r3['Forecast'])
            else:
                v3 = float(r3['%s'%variable])

            if np.isnan(r4['%s'%variable]):
                v4 = float(r4['Forecast'])
            else:
                v4 = float(r4['%s'%variable]) if r4['%s'%variable] else v3


            f = (v1 * 0.675 + v2 * 0.225 + v3 * 0.075 + v4 * 0.025)
              #print self.results.ix[self.results.Date == forecastdate]
            self.results.ix[self.results.Date == forecastdate, '%s'%variable] = f
            #print self.results.ix[self.results.Date == forecastdate]


if __name__ == '__main__':
    data = p.read_csv('tc/London.csv')
    a = Analyser(data)
    a.forecast()
    a.results.to_csv('prediction.csv')
