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

    for i in glob.glob('tidydata/joined/*.csv'):
        data = p.read_csv(i)
        cityname = i.split('/')[-1].replace('.csv','')
        #print data

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
        data = data[40:]

        Xinput = zip(data.Count.tolist(), data.Friday1.tolist(), data.Friday2.tolist(),data.Friday3.tolist(),data.Friday4.tolist())
        
        Youtput = data.Searches.tolist()

        data.to_csv('derp.csv')
        #print Xinput[:10]
        #print Youtput[:10]
        try:
            clf = Lasso(alpha=0.01)
            clf.fit(Xinput, Youtput)
            #print clf
            print cityname, clf.coef_

            cutoff_date = dt.datetime.strptime('2013-10-24 00:00:00', '%Y-%m-%d %H:%M:%S')

            def predict_searches(row):
                if row['Date'] > cutoff_date:
                    tc_w, f1_w, f2_w, f3_w, f4_w = clf.coef_ 
                    ps = tc_w*row['Count'] + f1_w*row['Friday1'] + f2_w*row['Friday2'] + \
                        f3_w*row['Friday3'] + f4_w*row['Friday4']
                    return ps
                else:
                    return 0

            data['PredictedSearches'] = data.apply(predict_searches, axis=1)

            def predict_last_4_fridays(row):
                if row['Date'] > cutoff_date:
                    f1_w, f2_w, f3_w, f4_w = 0.675, 0.225, 0.075, 0.025
                    ps = f1_w*row['Friday1'] + f2_w*row['Friday2'] + \
                        f3_w*row['Friday3'] + f4_w*row['Friday4']
                    return ps
                else:
                    return 0

            data['LF4Predicted'] = data.apply(predict_last_4_fridays, axis=1)


            predicted_w_t = data.PredictedSearches
            predicted_l4f = data.LF4Predicted
            actual = data.Searches

            rmse_twitter = mean_squared_error(actual, predicted_w_t)
            rmse_twitter = math.sqrt(rmse_twitter)

            #print "RMSE from Model with Twitter is %s"%str(rmse_twitter)

            rmse_l4f = mean_squared_error(actual, predicted_l4f)
            rmse_l4f = math.sqrt(rmse_l4f)
            
            #print "RMSE from L4F is %s"%str(rmse_l4f)

            TWRaw = data.Count.tolist()
            TWinput = [[i] for i in TWRaw]

            clf = Lasso(alpha=0.01)
            clf.fit(TWinput, Youtput)
            just_twitter = [clf.coef_[0]*i for i in TWRaw]

            rmse_jt = mean_squared_error(actual, just_twitter)
            rmse_jt = math.sqrt(rmse_jt)
            
            #print "RMSE from Just Twitter is %s"%str(rmse_jt)

            errors[cityname] = {"RMSE_Twitter": rmse_twitter, 
                        "RMSE_L4F": rmse_l4f, 
                        "RMSE_Just_Twitter": rmse_jt}
        except ValueError:
            print cityname
    
    error_df = p.DataFrame.from_dict(errors, orient="index")
    error_df.to_csv('results.csv')

    print error_df

        



