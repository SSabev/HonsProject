import pandas as p
import numpy as np

from dateutil.relativedelta import relativedelta

import datetime as dt
import glob

from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error
import math


class ExtendedFeaturesLasso(object):

    def __init__(self, alphas, features, cutoff, output=True):
        self.output = output
        self.alphas = alphas
        self.features = features
        self.cutoff = cutoff
        self.errors = {}
        self.weights_rmse = {}
        #for i in alphas:
        #    self.weights_rmse[i] = {}
        #    self.weights_rmse[i]['TCF'] = []
        #    self.weights_rmse[i]['TDF'] = []
        #    self.weights_rmse[i]['WTDF'] = []
        #    self.weights_rmse[i]['WTCF'] = []

        self.weights = {}
        self.writer = p.ExcelWriter('results/extendedLassoResults.xlsx')
        self.go_and_classify()
        self.output_errors()
        self.output_weight_reduction()


    def get_fridays(self, data):
        fridays = []
        def conversion(date):
            return dt.datetime.strptime(date, '%Y-%m-%d')
        data.Date = data.Date.apply(conversion)

        for forecastdate in data['Date'][36:]:
            tm1 = forecastdate - relativedelta(days = 7)
            tm2 = forecastdate - relativedelta(days =14)
            tm3 = forecastdate - relativedelta(days =21)
            tm4 = forecastdate - relativedelta(days =28)
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

            fridays.append((forecastdate, v1,v2,v3,v4))

        data_compound_friday = [(i, 0.675*j + 0.225*k + 0.075*l + 0.025*m) \
              for (i,j,k,l,m) in fridays]
        data_fridays = p.DataFrame(fridays, \
              columns = ['Date', 'Friday1', 'Friday2', 'Friday3', 'Friday4'])
        data_compfriday = p.DataFrame(data_compound_friday, \
              columns = ['Date', 'Fridays'])

        return data_fridays, data_compfriday

    def go_and_classify(self):
        def predict_last_4_fridays(row):
            cutoff_date = dt.datetime.strptime('2013-09-25 00:00:00', \
                                                '%Y-%m-%d %H:%M:%S')
            if row['Date'] > cutoff_date:
                ps = 0.675*row['Friday1'] + 0.225*row['Friday2'] + \
                        0.075*row['Friday3'] + 0.025*row['Friday4']
                return ps
            else:
                return 0

        for placename in self.features:
            i = r'tidydata/joined/%s.csv'%placename
            j = r'tidydata/rawfeatures/%s.csv'%placename
            data = p.read_csv(i)
            features = p.read_csv(j)
            if 'Unnamed: 0' in features.columns:
                features['Date'] = features['Unnamed: 0']
                del features['Unnamed: 0']
            if 'Unnamed: 0' in data.columns:
                del data['Unnamed: 0']

            merged = data.merge(features, on='Date', how='outer')
            merged = merged.fillna(merged.mean())
            placename = i.split('/')[-1].replace('.csv','')

            fridays, comp_fridays = self.get_fridays(data)

            data = data.merge(fridays, on='Date', how='outer')
            data = data[36:209]
            merged = merged[36:209]
            dict_of_features = {i: merged[i].tolist() for i in merged.columns \
            if i not in ['Date', 'Friday1', 'Friday2', 'Friday3', 'Friday4', 'Searches', 'NSearches']}
            dict_of_items = {i: data[i].tolist() for i in data.columns if i in [ 'Friday1', 'Friday2', 'Friday3', 'Friday4']}
            dict_of_all = dict(dict_of_features.items() + dict_of_items.items())
            Xinput = p.DataFrame.from_dict(dict_of_all)
            Xinput = Xinput.fillna(0)

            #print Xinput.columns
            try:
                del Xinput['Searches']
                del Xinput['NSearches']
                del Xinput['Exits']

            except KeyError:
                pass

            #Xinput.to_csv('tidydata/withfeatures/%s.csv'%placename)
            Youtput = data.Searches.tolist()

            data['LF4Predicted'] = data.apply(predict_last_4_fridays, axis=1)

            X2 = Xinput.copy(deep=True)
            del X2['Friday1']
            del X2['Friday2']
            del X2['Friday3']
            del X2['Friday4']

            X2['Fridays'] = comp_fridays.Fridays
            X2 = X2.fillna(0)

            actual = data.Searches[self.cutoff:].tolist()
            #data.to_csv('tidydata/withfeatures/%s_with_prediction.csv'%placename)

            self.classify(placename, Xinput, X2, data['LF4Predicted'], \
                          Youtput, actual)
            
    def output_weights(self, input,coef, placename, alpha, typeo):
        wdata = zip(input.columns, coef)
        wdata = p.DataFrame.from_dict(dict(wdata), orient='index')
        wdata = wdata.reset_index()
        wdata.columns = ['Word', 'Weight']
        wdata = wdata[wdata.Weight != 0]
        if typeo == 'LassoW':
            wdata.to_csv('tidydata/weights/DynamicFridays/%s-%s.csv'\
                          %(placename, alpha))
        else:
            wdata.to_csv('tidydata/weights/CompoundFridays/%s-%s.csv'\
                          %(placename, alpha))

    def output_predictions(self, data, placename):
        data = p.DataFrame(data, columns=['TwitterDF', 'TwitterCF', \
                            'L4F', 'Actual'])
        try:
            del data['X']
        except KeyError:
            pass
        data.to_csv('tidydata/predictions/%s.csv'%placename, index=False)

    def classify(self, placename, Xinput, X2, l4f, Youtput, actual):
        for alpha in self.alphas:
            print alpha
            print placename

            clf = Lasso(alpha=alpha, max_iter = 500)
            clf.fit(Xinput[:self.cutoff].values, Youtput[:self.cutoff])
            #print placename, clf.coef_
            self.output_weights(Xinput, clf.coef_, placename, alpha, 'LassoW')

            clf2 = Lasso(alpha=alpha, max_iter = 500)
            clf2.fit(X2[:self.cutoff].values, Youtput[:self.cutoff])
            #print placename, clf.coef_

            self.output_weights(X2, clf2.coef_, placename, alpha, 'L4FW')


            predicted_w_t = clf.predict(Xinput[self.cutoff:].values)
            predicted_tw_s_f = clf2.predict(X2[self.cutoff:].values)
            predicted_l4f = l4f[self.cutoff:]

            self.output_predictions(zip(predicted_w_t, predicted_tw_s_f,
                            predicted_l4f, actual), placename)

            rmse_twitter = mean_squared_error(actual, predicted_w_t)
            rmse_twitter = math.sqrt(rmse_twitter)
            rmse_cf = mean_squared_error(actual, predicted_tw_s_f)
            rmse_cf = math.sqrt(rmse_cf)
            rmse_l4f = mean_squared_error(actual, predicted_l4f)
            rmse_l4f = math.sqrt(rmse_l4f)

            winner = ''
            errors = [rmse_l4f, rmse_cf, rmse_twitter]

            if rmse_l4f == min(errors):
                winner = 'L4F'
            elif rmse_twitter == min(errors):
                winner = 'TDF'
            else:
                winner = 'TCF'

            winner2 = 'L4F' if rmse_l4f < rmse_twitter else 'Twitter'

            # self.weights_rmse[alpha]['TDF'] = self.weights_rmse[alpha]['TDF'].append(rmse_twitter)
            # self.weights_rmse[alpha]['TCF'] = self.weights_rmse[alpha]['TCF'].append(rmse_cf)
            # self.weights_rmse[alpha]['WTDF'] = self.weights_rmse[alpha]['WTDF'].append(sum([1 for i in clf.coef_ if i!=0]))
            # self.weights_rmse[alpha]['WTCF'] = self.weights_rmse[alpha]['WTCF'].append(sum([1 for i in clf2.coef_ if i!=0]))


            #print "RMSE from L4F is %s"%str(rmse_l4f)
            placeerror = self.errors.get(placename, [])
            placeerror.append({"Aplha": alpha,
                        "RMSE_T_DF": rmse_twitter,
                        "RMSE_T_CF": rmse_cf,
                        "RMSE_L4F": rmse_l4f,
                        "winner": winner,
                        "WinnerBin": winner2,
        #"R^2_twitter": clf.score(Xinput[self.cutoff:].values, actual),
                        "Non0WeightsDF": sum([1 for i in clf.coef_ if i!=0]),
                        "Non0WeightsCF": sum([1 for i in clf2.coef_ if i!=0]),
                        })
            self.errors[placename] = placeerror

    def output_errors(self):
          for place in self.errors:
              error_df = p.DataFrame.from_records(self.errors[place])
              error_df.to_excel(self.writer,'%s'%place)

          self.writer.save()


    def output_weight_reduction(self):
        df = p.DataFrame.from_dict(self.weights_rmse)
        df.to_csv('results/weight_rmse.csv')

if __name__ == '__main__':
    list_of_feature_files = [i.split('/')[-1].replace('.csv', '') \
                for i in glob.glob('tidydata/rawfeatures/*.csv')]
    alphas = [0.5, 1, 2,5, 10, 20, 50, 125, 250, 500, 1000, 2000, \
                4000, 8000, 16000, 32000]

    a = ExtendedFeaturesLasso(alphas, list_of_feature_files, 140)
