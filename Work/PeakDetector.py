__author__ = 'Stefan'

import glob
import pandas as p

def peak_detection(filename, metric):
    df = p.read_csv(filename)
    mean = df[metric].mean()
    stdev = df[metric].std()
    try:
        del df['Unnamed: 0.1']
    except KeyError:
        pass
    print filename
    print mean
    print stdev

    if mean < stdev:

        def classify(k):
            max_threshold = mean + 2*stdev
            min_threshold = mean - 2*stdev

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

