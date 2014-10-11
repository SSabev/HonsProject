__author__ = 'Stefan'

import glob
import pandas as p

def peak_detection(filename, metric):
    df = p.read_csv(filename)
    median = df[metric].median()
    stdev = df[metric].std()
    del df['Unnamed: 0.1']

    print median
    print stdev

    if median < stdev:

        def classify(k):
            max_threshold = median + 2*stdev
            min_threshold = median - 2*stdev

            if k > max_threshold:
                return 'Peak'
            elif k < min_threshold:
                return 'MinPeak'
            else:
                return 'NoPeak'

        df['%sPeakToday'%metric] = df[metric].apply(classify)

        return df

    else:
        return False


if __name__ == '__main__':
    file = glob.glob('tidydata/twitter/Sochi*')[0]
    print file

    df = peak_detection(file, 'Count')

    df.to_csv('Sochi-peaks.csv')

