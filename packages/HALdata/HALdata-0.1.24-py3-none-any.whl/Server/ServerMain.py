#!/usr/bin/env python

'''
MIT License
Copyright (c) 2021 Mikhail Hyde & Cole Crescas
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from ErrorHandler import ErrorHandler
import pandas as pd
import pickle

"""ALERT THIS FILE IS IN TESTING & DEVELOPMENT STAGE"""

"""
This main file will be used for testing at the moment to:
1. load a pickled df
2. load a master df
3. unpickle, check for errors
4. pad missing columns in df
5. if there are no errors then upload to s3 bucket
6. store local copy onto server 
"""
sample_df = pd.read_csv("C:/Users/ccrescas/Downloads/BAY_4_sample.csv")

pickle_df = pickle.dumps(sample_df)

master_df =  pd.read_csv("C:/Users/ccrescas/Python/TransferData/HALdata/master_df.csv")






