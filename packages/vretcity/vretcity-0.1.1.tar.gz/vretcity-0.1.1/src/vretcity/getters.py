import pandas as pd

from vretcity.preprocessor import convert_values

def get_events(df):
    """Returns significant events from the log. The output ignores transform and ray information etc.

    Args:
        df ([pd.DataFrame]): The full log already preprocessed with `process_log`
    Returns:
        [pandas.DataFrame]: Dataframe with the event information
    """
    # TODO - this should be solved with some enums or other exhaustive list
    df_events = df.loc[~df["typ"].isin(["Transform", "RayBegin", "RayEnd", "EyeBegin", "EyeEnd",
        "Score", "HeartRate"]), :]
    df_events = df_events.loc[((df_events["druhy_objekt"] == "Head") & (df_events["typ"].str.contains("Trigger"))) | 
                                (~(df_events["typ"].str.contains("Trigger"))), :]
    df_events = df_events.loc[df_events["objekt"] != "UserInElevator"]
    df_events = df_events.loc[:, ["timesincestart", "typ", "objekt", "druhy_objekt", "hodnota"]]
    return df_events
    

def get_heartrate(df):
    """Extracts heartrate information form the log

    Args:
        df ([pd.DataFrame]): The full log already preprocessed with `process_log`
    Returns:
        [pandas.DataFrame]: Dataframe with the heartrate information and necessary values
    """
    df_heartrate = df.loc[df["objekt"] == "HeartRate"]
    df_heartrate = df_heartrate[["cas", "timesincestart", "hodnota"]]
    df_heartrate = convert_values(df_heartrate, "hodnota")
    return df_heartrate
