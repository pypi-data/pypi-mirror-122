import plotly.express as px

def plot_path(data, times=[], downsample=10):
    dat = data.loc[(data['objekt'] == 'VRCamera') & (data['typ'] == 'Transform'),:]
    dat = dat.iloc[range(1, dat.shape[0], downsample)]
    fig = px.line_3d(dat, x="pozice_x", y="pozice_z", z="pozice_y")
    return fig


def plot_event_value(df, timesincestart=True):
    """Plots an evolution of the value

    Wrapper around plotly.express.Line standardized so that new events can be added

    Args:
        df (pandas.DataFrame): dataframe with a specific event as collected with get_events functions
        timesincestart (bool): Should the time be displayed as is in the data or as time since the log start
    """
    xname = "cas"
    if timesincestart: xname = "timesincestart"
    fig = px.line(df, x=df[xname], y="hodnota")
    return fig