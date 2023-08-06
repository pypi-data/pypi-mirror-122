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

'''
This program takes in a dataframe, checks for validity and then returns a boolean if the file is ready to be sent to S3

return: boolean if file can be sent
'''

import pandas as pd
import numpy as np
import pickle


class ErrorHandler():
    def __init__(self, pickle_df, master_df):
        df = pickle.loads(pickle_df)
        self.master_df = master_df

        self.df = ErrorHandler.pad_data(df, self.master_df)

    def pad_data(self, df, master_df):
        """
        Pads the data into master dataframe.

        returns::self.df
        """
    
    
    def pad_check(self):
        """
        Checks the validity of pickle_df before progressing to next check

        returns::bool
        """

        return True

    def info_check(self):
        """
        checks that the rows and columns are correct

        returns::bool
        """
        return (len(self.df.columns) == len(self.master_df.columns) & len(self.df) > 10)

    def check_mising(self):
        """
        Checks for missing values in the df, this wont work because padded df will have a lot missing

        returns::bool
        """
        return (self.df.isnull().sum().sum() < 10)

    def verify():
        """
        Calls all checks

        returns::bool
        """
        if ((ErrorHandler.pickle_check() == True) & (ErrorHandler.info_check() == True) & (ErrorHandler.check_mising() == True)):
            return True
        else:
            return False

