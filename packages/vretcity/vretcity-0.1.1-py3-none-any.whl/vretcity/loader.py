import pandas as pd
import numpy as np

from vretcity.preprocessor import convert_values

def load_log(filepth, dec="."):
    """Loads the csv log as downlaoded from the website. No data processing is done, this
    is just a wrapper around pandas.read_table having correct setup

    Args:
        filepth ([type]): path to the valid csv.
        dec (str, optional): Depending on the system locale, it is possible that different
        machines might downlaod and save the csv with a different decimal point. This
        can override the decimal values in case you get strings where there 
        should be nu,bers. Defaults to ".".

    Returns:
        pandas.DataFrame: returns a data frame
    """
    data = pd.read_table(filepth, sep=';', header=0, decimal=dec, index_col=False)
    # Tries the opposite decimal point
    if data["pozice_x"].dtype != np.float64:
        new_dec = "."
        if dec == ".": new_dec = ","
        for column in data.columns:
            if ("pozice" in column) | ("rotace" in column):
                data = convert_values(data, column)
    return data


def is_valid(df):
    """Returns if the log is valid or not. NOT IMPLEMENTED. ALWAYS RETURNS TRUE

    Args:
        df pandas.DataFrame: dataframe loaded with the load_log function
    Returns:
        bool: is dataframe valid or not
    """
    return True