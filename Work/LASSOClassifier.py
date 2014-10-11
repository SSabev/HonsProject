import pandas as p
import numpy as np

from dateutil.relativedelta import relativedelta

import datetime as dt
import glob

from sklearn.linear_model import Lasso, Ridge
from sklearn.metrics import mean_squared_error
import math

from PeakDetector import peak_detection


class LASSOOverallPredictor(object):
    def __init__(self, alphas, cutoff, output=True):
        self.output = output
        self.alphas = alphas
        self.errors = {}
        self.weights = {}
        self.cutoff = cutoff
        self.go_and_classify()
        self.output_errors()

    @staticmethod
    def get_fridays(data):
        fridays = []

        def conversion(date):
            return dt.datetime.strptime(date, '%Y-%m-%d')

        data.Date = data.Date.apply(conversion)

        for forecastdate in data['Date'][36:]:
            tm1 = forecastdate - relativedelta(days=7)
            tm2 = forecastdate - relativedelta(days=14)
            tm3 = forecastdate - relativedelta(days=21)
            tm4 = forecastdate - relativedelta(days=28)
            r1 = data[data.Date == tm1]
            r2 = data[data.Date == tm2]
            r3 = data[data.Date == tm3]
            r4 = data[data.Date == tm4]

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

            fridays.append((forecastdate, v1, v2, v3, v4))

        data_compound_friday = [(i, 0.675 * j + 0.225 * k + 0.075 * l + 0.025 * m) \
                                for (i, j, k, l, m) in fridays]
        data_fridays = p.DataFrame(fridays, \
                                   columns=['Date', 'Friday1', 'Friday2', 'Friday3', 'Friday4'])
        data_compfriday = p.DataFrame(data_compound_friday, \
                                      columns=['Date', 'Fridays'])

        return data_fridays, data_compfriday

    def go_and_classify(self):
        for i in glob.glob('tidydata/joined/*.csv'):
            place = i.split('/')[-1].replace('.csv', '')
            a = peak_detection(i, 'RMCount')
            if a is not False:
                data = a
                df1, df2 = self.get_fridays(data)
                self.classify(data, place, df1, df2)
                print "Done with %s"%place

    def classify(self, df, place, data_fridays, data_compfriday):
        def predict_last_4_fridays(row):
            if row['Date'] > cutoff_date:
                f1_w, f2_w, f3_w, f4_w = 0.675, 0.225, 0.075, 0.025
                ps = f1_w * row['Friday1'] + f2_w * row['Friday2'] + \
                     f3_w * row['Friday3'] + f4_w * row['Friday4']
                return ps
            else:
                return 0

        data = df.copy(deep=True)
        data = data.merge(data_fridays, on='Date', how='outer')
        data = data[36:]
        # print data
        data = data.fillna(0)

        data_sf = df.copy(deep=True)
        data_sf = data_sf.merge(data_compfriday, on='Date', how='outer')
        data_sf = data_sf[36:]
        data_sf = data_sf.fillna(0)

        Xinput = p.DataFrame(zip(data.Count.tolist(), data.Friday1.tolist(), \
                                 data.Friday2.tolist(), data.Friday3.tolist(), data.Friday4.tolist()), \
                             columns=['RMCount', 'Friday1', 'Friday2', 'Friday3', 'Friday4'])

        X2 = p.DataFrame(zip(data_sf.Count.tolist(), data_sf.Fridays.tolist()), \
                         columns=['RMCount', 'Fridays'])

        Youtput = data.Searches.tolist()

        for alpha in self.alphas:
            clf = Lasso(alpha=alpha)
            clf.fit(Xinput[:self.cutoff].values, Youtput[:self.cutoff])
            #print clf.coef_

            clf2 = Lasso(alpha=alpha)
            clf2.fit(X2[:self.cutoff].values, Youtput[:self.cutoff])
            #print clf2.coef_

            self.weights['%s-dynamic-%s' % (place, str(alpha))] = {'Twitter': clf.coef_[0],
                                                                   'F1': clf.coef_[1],
                                                                   'F2': clf.coef_[2],
                                                                   'F3': clf.coef_[3],
                                                                   'F4': clf.coef_[4],
            }

            ridge1 = Ridge(alpha=alpha)
            ridge1.coef_ = clf.coef_
            ridge1.intercept_ = clf.intercept_

            ridge2 = Ridge(alpha=alpha)
            ridge2.coef_ = clf2.coef_
            ridge2.intercept_ = clf2.intercept_

            cutoff_date = dt.datetime.strptime('2013-09-24 00:00:00', '%Y-%m-%d %H:%M:%S')

            data['LF4Predicted'] = data.apply(predict_last_4_fridays, axis=1)

            predicted_tw_d_f = clf.predict(Xinput[self.cutoff:].values)
            predicted_tw_d_f_r = ridge1.predict(Xinput[self.cutoff:].values)
            predicted_tw_s_f = clf2.predict(X2[self.cutoff:].values)
            predicted_tw_s_f_r = ridge2.predict(X2[self.cutoff:].values)

            predicted_l4f = data.LF4Predicted
            actual = data.RMSearches

            rmse_twitter = mean_squared_error(actual[self.cutoff:].tolist(), predicted_tw_d_f)
            rmse_twitter = math.sqrt(rmse_twitter)

            rmse_static = mean_squared_error(actual[self.cutoff:].tolist(), predicted_tw_s_f)
            rmse_static = math.sqrt(rmse_static)

            rmse_rtdf = math.sqrt(mean_squared_error(actual[self.cutoff:].tolist(), predicted_tw_d_f_r))
            rmse_rtcf = math.sqrt(mean_squared_error(actual[self.cutoff:].tolist(), predicted_tw_s_f_r))

            rmse_l4f = mean_squared_error(actual[self.cutoff:].tolist(), predicted_l4f[self.cutoff:])
            rmse_l4f = math.sqrt(rmse_l4f)

            predictions = p.DataFrame(zip(actual, clf.predict(Xinput), clf2.predict(X2), \
                                          predicted_l4f, ridge1.predict(Xinput), ridge2.predict(X2)), \
                                      columns=['Actual', 'TwitterDF', 'TwitterCF', 'L4F', 'RTwitterDF', 'RTwitterCF'])
            predictions.to_csv('tidydata/predictions/%s.csv' % place)

            try:
                del data['Unnamed: 0']
            except KeyError:
                pass
            #data.to_csv('tidydata/predictions/%s-dynamic-%s.csv'%(place, alpha))
            winner = ''
            errors = {rmse_l4f: 'L4F',
                      rmse_static: 'TCF',
                      rmse_twitter: 'TDF',
                      rmse_rtdf: 'RTDF',
                      rmse_rtcf: 'RTCF'}

            winner2 = 'L4F' if rmse_l4f < rmse_twitter else 'Twitter'

            self.errors[place] = {"TwitterDF": rmse_twitter,
                                  "TwitterCF": rmse_static,
                                  "L4F": rmse_l4f,
                                  "RidgeTwitterDF": rmse_rtdf,
                                  "RidgeTwitterCF": rmse_rtcf,
                                  "R^2_twitter": clf.score(Xinput[self.cutoff:], actual[self.cutoff:]),
                                  "Twitter weight": clf.coef_[0],
                                  "Fridays weight": clf.coef_[1],
                                  "Winner": errors[min(errors.keys())],
                                  "WinnerBin": winner2,
            }

    def output_errors(self):
        error_df = p.DataFrame.from_dict(self.errors, orient="index")
        error_df.to_csv('results/lasso-static-and-dynamic.csv')

        weights_df = p.DataFrame.from_dict(self.weights, orient='index')
        weights_df.to_csv('results/static-and-dynamic.csv')


if __name__ == '__main__':
    a = LASSOOverallPredictor([1], 140)
