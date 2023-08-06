import pandas as pd
from vretcity import constants

def convert_events(df):
    """Converts integer events to string names

    Args:
        df ([pd.DataFrame]): loaded dataframe
    """
    df['typ'] = df['typ'].replace(constants.EVENT_CODES)
    return df


def convert_times(df):
    """Converts time columns, adds timesincestart column

    Args:
        df ([type]): [description]

    Returns:
        [type]: [description]
    """
    df["timesincestart"] = (df["cas"] - df.iloc[0,0])/1000
    return df


def convert_values(df, column):
    """[summary]

    Args:
        df ([type]): [description]

    Returns:
        [type]: [description]
    """
    df[column] = pd.to_numeric(df[column].str.replace(",", "."))
    return df


def process_log(df):
    """Processes the dataframe with the most common convertors. The dataframe is modified by reference
    so no return assignment is necessary

    Args:
        df (pandas.DataFrame): vretcity data frame as loaded by load_log

    Returns:
        [pandas.DataFrame]: processed DataFrame
    """
    df = convert_events(df)
    df = convert_times(df)
    return df