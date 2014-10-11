__author__ = 'Stefan'

import glob
import pandas as p

def peak_detection(filename, counts, searches):
    df = p.read_csv(filename)

    mean_c = df[counts].mean()
    stdev_c = df[counts].std()

    mean_s = df[searches].mean()
    stdev_s = df[searches].std()

    try:
        del df['Unnamed: 0.1']
    except KeyError:
        pass
    print filename
    print mean_c, stdev_c, mean_s, stdev_s

    if mean_c < stdev_c:

        def classify(k):
            max_threshold = mean_c + 2*stdev_c
            min_threshold = mean_c - 2*stdev_c

            if k > max_threshold:
                return 1
            elif k < min_threshold:
                return 1
            else:
                return 0

        def search_peak(k):
            max_threshold = mean_s + 2*stdev_s
            min_threshold = mean_s - 2*stdev_s

            if k > max_threshold:
                return 1
            elif k < min_threshold:
                return 1
            else:
                return 0

        df['CountPeakToday'] = df[counts].apply(classify)
        df['SearchesPeakToday'] = df[searches].apply(search_peak)

        return df

    else:
        return False


if __name__ == '__main__':
    file = glob.glob('tidydata/twitter/Sochi*')[0]
    print file

    df = peak_detection(file, 'Count')

    df.to_csv('Sochi-peaks.csv')

