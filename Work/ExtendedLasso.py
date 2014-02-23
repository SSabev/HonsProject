import pandas as p
import numpy as np

from dateutil.relativedelta import relativedelta

import datetime as dt
import glob

from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error
import math


if __name__ == '__main__':
    errors = {}
    list_of_feature_files = [i.split('/')[-1].replace('.csv', '') for i in glob.glob('tidydata/rawfeatures/*.csv')]
    print list_of_feature_files
    alphas = [0.5, 1, 2,5, 10, 20, 50, 125, 250, 500, 1000]
    for alpha in alphas:
        for cityname in list_of_feature_files:
            print cityname
            i = r'tidydata/joined/%s.csv'%cityname
            j = r'tidydata/rawfeatures/%s.csv'%cityname
            
            
            data = p.read_csv(i)
            features = p.read_csv(j)
            features['Date'] = features['Unnamed: 0']
            del features['Unnamed: 0']
            del data['Unnamed: 0']
            merged = data.merge(features, on='Date', how='outer')
            merged = merged.fillna(merged.mean())
            cityname = i.split('/')[-1].replace('.csv','')

            fridays = []

            def get_fridays():
                for forecastdate in data.Date[39:]:
                    tm1 = forecastdate - relativedelta(days = 7)
                    tm2 = forecastdate - relativedelta(days =14)
                    tm3 = forecastdate - relativedelta(days =21)
                    tm4 = forecastdate - relativedelta(days =28)
                    r1 = data[data.Date == tm1]
                    r2 = data[data.Date == tm2]
                    r3 = data[data.Date == tm3]
                    r4 = data[data.Date == tm4]
                    
                    if np.isnan(r1.Searches):
                        v1 = float(0)
                    else:
                        v1 = float(r1.Searches)
                    
                    if np.isnan(r2.Searches):
                        v2 = float(0)
                    else:
                        v2 = float(r2.Searches)

                    if np.isnan(r3.Searches):
                        v3 = float(0)
                    else:
                        v3 = float(r3.Searches)

                               
                    if np.isnan(r4.Searches):
                        v4 = float(0)   
                    else:
                        v4 = float(r4.Searches)
                    
                    fridays.append((forecastdate, v1,v2,v3,v4)) 

            def conversion(date):
                return dt.datetime.strptime(date, '%Y-%m-%d')

            
            data.Date = data.Date.apply(conversion)

            get_fridays()

            data_fridays = p.DataFrame(fridays, columns = ['Date', 'Friday1', 'Friday2', 'Friday3', 'Friday4'])
            data = data.merge(data_fridays, on='Date', how='outer')
            data = data[40:172]
            merged = merged[40:172]


            dict_of_features = {i: merged[i].tolist() for i in merged.columns if i not in ['Date', 'Friday1', 'Friday2', 'Friday3', 'Friday4', 'Exits', 'Searches'
                'NSearches']}
            dict_of_items = {i: data[i].tolist() for i in data.columns if i in [ 'Friday1', 'Friday2', 'Friday3', 'Friday4']}
            dict_of_all = dict(dict_of_features.items() + dict_of_items.items())
            Xinput = p.DataFrame.from_dict(dict_of_all)

            print Xinput.columns
            try: 
                del Xinput['Searches']
                del Xinput['NSearches']
                del Xinput['Exits']
                
            except KeyError:
                print "Failed deleting some of the columns"
            Xinput = Xinput.fillna(0)
            Youtput = data.Searches.tolist()

            Xinput.to_csv('tidydata/withfeatures/%s.csv'%cityname)

            clf = Lasso(alpha=alpha, max_iter = 1000)
            clf.fit(Xinput[:110].values, Youtput[:110])
            #print cityname, clf.coef_

            wdata = zip(Xinput.columns, clf.coef_)
            wdata = p.DataFrame.from_dict(dict(wdata), orient='index')
            wdata = wdata.reset_index()
            wdata.columns = ['Word', 'Weight']
            wdata.to_csv('tidydata/weights/%s.csv'%cityname)

            cutoff_date = dt.datetime.strptime('2013-09-25 00:00:00', '%Y-%m-%d %H:%M:%S')

            def predict_last_4_fridays(row):
                if row['Date'] > cutoff_date:
                    ps = 0.675*row['Friday1'] + 0.225*row['Friday2'] + \
                            0.075*row['Friday3'] + 0.025*row['Friday4']
                    return ps
                else:
                    return 0

            data['LF4Predicted'] = data.apply(predict_last_4_fridays, axis=1)

            predicted_w_t = clf.predict(Xinput[110:].values)
            predicted_l4f = data.LF4Predicted[110:]

            actual = data.Searches[110:]

            data.to_csv('tidydata/withfeatures/%s_with_prediction.csv'%cityname)

            rmse_twitter = mean_squared_error(actual, predicted_w_t)
            rmse_twitter = math.sqrt(rmse_twitter)

            #print "RMSE from Model with Twitter is %s"%str(rmse_twitter)

            rmse_l4f = mean_squared_error(actual, predicted_l4f)
            rmse_l4f = math.sqrt(rmse_l4f)
            
            #print "RMSE from L4F is %s"%str(rmse_l4f)

            errors[cityname] = {"RMSE_Twitter": rmse_twitter, 
                        "RMSE_L4F": rmse_l4f, 
                        "R^2_twitter": clf.score(Xinput[110:].values, actual),
                        "Non0Weights": sum([1 for i in clf.coef_ if i>0])
                        }

        print errors
        #except ValueError:
        #    print cityname

        error_df = p.DataFrame.from_dict(errors, orient="index")
        error_df.to_csv('results/ext-results%s.csv')
    #print error_df

    



