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
