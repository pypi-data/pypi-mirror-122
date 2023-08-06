import re

def export_events(df_events, filepath, include_interactions=True):
    """[summary]

    Args:
        df_events (pandas.DataFrame): DataFrame obtained usually with the getters.get_events function
        filepath (string): Filepath to the original log
        include_interactions (bool, optional): Should interaction events be included int he output. Defaults to True.
    """
    if include_interactions:
        out_filename = re.sub("\.csv", "_events.csv", filepath)
        df = df_events
    else:
        out_filename = re.sub("\.csv", "_events_nointeract.csv", filepath)
        df = df_events.loc[(~df_events["typ"].str.contains("Interac")),:].to_csv(out_filename, index=False)
    df.to_csv(out_filename, index=False)

