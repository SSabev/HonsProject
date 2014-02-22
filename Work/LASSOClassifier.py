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
    weights = {}

    for i in glob.glob('~/Dev/HonsProject/Work/tidydata/joined/*.csv'):
        data = p.read_csv(i)
        cityname = i.split('/')[-1].replace('.csv','')
        #print data

        fridays = []

        def get_fridays():
            for forecastdate in data.Date[40:]:
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
                    if cityname=='Denver':
                        print r1.Searches

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
        data = data.fillna(data.mean())

        Xinput = p.DataFrame(zip(data.Count.tolist(), data.Friday1.tolist(), \
                data.Friday2.tolist(),data.Friday3.tolist(),data.Friday4.tolist()),\
                columns = ['Count', 'Friday1', 'Friday2', 'Friday3', 'Friday4'])
        
        Youtput = data.Searches.tolist()
        clf = Lasso(alpha=0.01)
        clf.fit(Xinput[:110].values, Youtput[:110])
        print cityname, clf.coef_

        weights[cityname] = {'Twitter': clf.coef_[0],
                'F1': clf.coef_[1],
                'F2': clf.coef_[2],
                'F3': clf.coef_[3],
                'F4': clf.coef_[4],
                }

        cutoff_date = dt.datetime.strptime('2013-09-24 00:00:00', '%Y-%m-%d %H:%M:%S')

        def predict_last_4_fridays(row):
            if row['Date'] > cutoff_date:
                f1_w, f2_w, f3_w, f4_w = 0.675, 0.225, 0.075, 0.025
                ps = f1_w*row['Friday1'] + f2_w*row['Friday2'] + \
                    f3_w*row['Friday3'] + f4_w*row['Friday4']
                return ps
            else:
                return 0

        data['LF4Predicted'] = data.apply(predict_last_4_fridays, axis=1)

        predicted_w_t_by_lass = clf.predict(Xinput[110:].values)
        predicted_l4f = data.LF4Predicted
        actual = data.Searches

        rmse_twitter = mean_squared_error(actual[110:].tolist(), predicted_w_t_by_lass)
        rmse_twitter = math.sqrt(rmse_twitter)

        #print "RMSE from Model with Twitter is %s"%str(rmse_twitter)

        rmse_l4f = mean_squared_error(actual[110:].tolist(), predicted_l4f[110:])
        rmse_l4f = math.sqrt(rmse_l4f)

        del data['Unnamed: 0']
        data.to_csv('~/Dev/HonsProject/Work/tidydata/predictions/%s.csv'%cityname)
        
        #print "RMSE from L4F is %s"%str(rmse_l4f)

        errors[cityname] = {"RMSE_Twitter": rmse_twitter,
                    "RMSE_L4F": rmse_l4f,
                    "R^2_twitter": clf.score(Xinput[110:], actual[110:]),
                    }
    
    error_df = p.DataFrame.from_dict(errors, orient="index")
    error_df.to_csv('~/Dev/HonsProject/Work/results/results.csv')

    weights_df = p.DataFrame.from_dict(weights, orient='index')
    weights_df.to_csv('~/Dev/HonsProject/Work/results/weights.csv')
