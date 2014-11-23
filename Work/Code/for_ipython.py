import json
import datetime
import csv
from terms import terms, countries
import pandas as p
import glob
import io
import nltk
import string
import numpy as np


from FeatureExtractor import FeatureExtractor

a = FeatureExtractor("traveltweets_expanded")


import numpy as np
import pandas as p

from detect_cusum import detect_cusum

data = np.array(p.read_csv('../test_data/Sochi-weekly.csv').Searches.dropna().tolist())
mean = np.median(data)/5.0
drift = np.median(data)/10.0
ta, tai, taf, amp = detect_cusum(data, mean, drift, False, False)


