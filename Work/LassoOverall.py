import pandas as p
import numpy as np

from dateutil.relativedelta import relativedelta

import datetime as dt
import glob

from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error
import math


class LASSOOverallPredictor(object):

    def __init__(self, alphas, output=True):
        self.output = output
        self.alphas = alphas
        self.load_df()
        self.get_fridays()
        self.errors = {}
        self.weights = {}
        self.classify_with_dynamic_fridays()
        self.classify_with_static_fridays()
        self.output_errors()


    def load_df(self):
        data = p.DataFrame()
        for i in glob.glob('tidydata/joined/*.csv'):
            data = data.append(p.read_csv(i))
        def conversion(date):
            return dt.datetime.strptime(date, '%Y-%m-%d')
        data.Date = data.Date.apply(conversion)
        data = data.groupby(['Date'])
        data = data.sum()
        del data['NSearches']
        del data['Unnamed: 0']
        if self.output:
            data.to_csv('tidydata/joined/OVERALL.CSV')
        data = data.reset_index()
        self.data = data

    def get_fridays(self):
        fridays = []
        for forecastdate in self.data['Date'][36:]:
            tm1 = forecastdate - relativedelta(days = 7)
            tm2 = forecastdate - relativedelta(days =14)
            tm3 = forecastdate - relativedelta(days =21)
            tm4 = forecastdate - relativedelta(days =28)
            r1 = self.data[self.data.Date == tm1]
            r2 = self.data[self.data.Date == tm2]
            r3 = self.data[self.data.Date == tm3]
            r4 = self.data[self.data.Date == tm4]

            r1 = r1.to_dict(outtype='records')
            r2 = r2.to_dict(outtype='records')
            r3 = r3.to_dict(outtype='records')
            r4 = r4.to_dict(outtype='records')

            if r1:
                r1 = r1[0]
            else:
                r1 = {'Searches': np.nan, 'Forecast': 0}

            if r2:
                r2 = r2[0]
            else:
                r2 = {'Searches': np.nan, 'Forecast': 0}

            if r3:
                r3 = r3[0]
            else:
                r3 = {'Searches': np.nan, 'Forecast': 0}

            if r4:
                r4 = r4[0]
            else:
                r4 = {'Searches': np.nan, 'Forecast': 0}

            if np.isnan(r1['Searches']):
                v1 = float(0)
            else:
                v1 = float(r1['Searches'])

            if np.isnan(r2['Searches']):
                v2 = float(0)
            else:
                v2 = float(r2['Searches'])

            if np.isnan(r3['Searches']):
                v3 = float(0)
            else:
                v3 = float(r3['Searches'])

            if np.isnan(r4['Searches']):
                v4 = float(0)
            else:
                v4 = float(r4['Searches'])

            fridays.append((forecastdate, v1,v2,v3,v4))

        data_compound_friday = [(i, 0.675*j + 0.225*k + 0.075*l + 0.025*m) \
              for (i,j,k,l,m) in fridays]
        self.data_fridays = p.DataFrame(fridays, \
              columns = ['Date', 'Friday1', 'Friday2', 'Friday3', 'Friday4'])
        self.data_compfriday = p.DataFrame(data_compound_friday, \
              columns = ['Date', 'Fridays'])

    def classify_with_dynamic_fridays(self):
        def predict_last_4_fridays(row):
            if row['Date'] > cutoff_date:
                f1_w, f2_w, f3_w, f4_w = 0.675, 0.225, 0.075, 0.025
                ps = f1_w*row['Friday1'] + f2_w*row['Friday2'] + \
                    f3_w*row['Friday3'] + f4_w*row['Friday4']
                return ps
            else:
                return 0

        data = self.data.copy(deep=True)
        data = data.merge(self.data_fridays, on='Date', how='outer')
        data = data[36:]
        data = data.fillna(0)

        Xinput = p.DataFrame(zip(data.Count.tolist(), data.Friday1.tolist(), \
                data.Friday2.tolist(),data.Friday3.tolist(),data.Friday4.tolist()),\
                columns = ['Count', 'Friday1', 'Friday2', 'Friday3', 'Friday4'])

        Youtput = data.Searches.tolist()

        for alpha in self.alphas:
            clf = Lasso(alpha=alpha)
            clf.fit(Xinput[:130].values, Youtput[:130])
            print clf.coef_

            self.weights['OVERALL-%s'%str(alpha)] = {'Twitter': clf.coef_[0],
                    'F1': clf.coef_[1],
                    'F2': clf.coef_[2],
                    'F3': clf.coef_[3],
                    'F4': clf.coef_[4],
                    }

            cutoff_date = dt.datetime.strptime('2013-09-24 00:00:00', '%Y-%m-%d %H:%M:%S')

            data['LF4Predicted'] = data.apply(predict_last_4_fridays, axis=1)

            predicted_w_t_by_lass = clf.predict(Xinput[130:].values)
            predicted_l4f = data.LF4Predicted
            actual = data.Searches

            rmse_twitter = mean_squared_error(actual[130:].tolist(), predicted_w_t_by_lass)
            rmse_twitter = math.sqrt(rmse_twitter)

            rmse_l4f = mean_squared_error(actual[130:].tolist(), predicted_l4f[130:])
            rmse_l4f = math.sqrt(rmse_l4f)

            try:
                del data['Unnamed: 0']
            except KeyError:
                pass
            data.to_csv('tidydata/overall prediction/OVERALL-dynamic-%s.csv'%alpha)

            self.errors['Overall-dynamic-%s'%str(alpha)] = {"RMSE_Twitter": rmse_twitter,
                        "RMSE_L4F": rmse_l4f,
                        "R^2_twitter": clf.score(Xinput[130:], actual[130:]),
                        }
            del clf

    def classify_with_static_fridays(self):
        data = self.data.copy(deep=True)
        data = data.merge(self.data_compfriday, on='Date', how='outer')
        data = data[35:]
        data = data.fillna(0)

        Xinput = p.DataFrame(zip(data.Count.tolist(), data.Fridays.tolist()),
                columns = ['Count', 'Fridays'])
        Youtput = data.Searches.tolist()

        for alpha in self.alphas:
            clf = Lasso(alpha=alpha)
            clf.fit(Xinput[:130].values, Youtput[:130])
            print clf.coef_

            self.weights['OVERALL-%s'%str(alpha)] = {'Twitter': clf.coef_[0],
                    'Fridays': clf.coef_[1]
                    }

            cutoff_date = dt.datetime.strptime('2013-09-24 00:00:00', '%Y-%m-%d %H:%M:%S')

            predicted_w_t_by_lass = clf.predict(Xinput[130:].values)
            actual = data.Searches

            rmse_twitter = mean_squared_error(actual[130:].tolist(), predicted_w_t_by_lass)
            rmse_twitter = math.sqrt(rmse_twitter)

            rmse_l4f = mean_squared_error(actual[130:].tolist(), data.Fridays.tolist()[130:])
            rmse_l4f = math.sqrt(rmse_l4f)

            try:
                del data['Unnamed: 0']
            except KeyError:
                pass
            data.to_csv('tidydata/overall prediction/OVERALL-static-%s.csv'%alpha)

            self.errors['Overall-static-%s'%str(alpha)] = {"RMSE_Twitter": rmse_twitter,
                        "RMSE_L4F": rmse_l4f,
                        "R^2_twitter": clf.score(Xinput[130:], actual[130:]),
                        }
            del clf

    def output_errors(self):
        error_df = p.DataFrame.from_dict(self.errors, orient="index")
        error_df.to_csv('results/OVERALLLassos.csv')

        weights_df = p.DataFrame.from_dict(self.weights, orient='index')
        weights_df.to_csv('results/OVERALLweights.csv')





if __name__ == '__main__':

    a = LASSOOverallPredictor([0.1, 2, 50, 100, 1000, 32000, 100000])