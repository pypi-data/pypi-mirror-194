"""
Read Data Module
"""

import pandas as pd

class readData:
    """Class to read data from input file and create dataframe from it"""        
   
    def readFile(file_name):
        """
        Create dataframe using the input file.

        Parameters
        ----------
        file_name : Files with .csv or .txt format
                    Input File.

        Returns
        -------
        in_file : dataframe
                Returns the input dataframe.
        """        
        if file_name.endswith(('.csv', '.txt')):
            in_file = pd.read_csv(file_name)   # reading the file
        else:
            print("\nReading the input file failed...")
            raise Exception('\nInvalid File or File Format')

        return in_file