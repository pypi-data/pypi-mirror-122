from rats.modules import ratparser
import numpy as np
import pandas as pd
import plotly_express as px
pd.options.mode.chained_assignment = None

def decimate_bp_plot(df):
    first = df.drop_duplicates(subset='function_number', keep='first')
    last = df.drop_duplicates(subset='function_number', keep='last')
    return pd.concat([first,last])


# function to run on initial upload
def bigpictureplot(df, decimate=True, timescale=1000000):
    title = df.board.unique()[0]
    df = df[['function_number', 'packet_count', 'llc_trigger_count','rats_capture_enable', 'anomalous', 'time']]
    df.drop_duplicates(subset=['llc_trigger_count', 'anomalous'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.loc[:,'state'] = np.where(df['anomalous'] == 0, 'GOOD', 'ERRORS')
    df.loc[:,'timescale'] = timescale
    # df['time'] = df['time'] / df['timescale']

    if decimate:
        df = df.groupby('state').apply(decimate_bp_plot)
        df.function_number = df.function_number.astype('category')
        print(df.head())
        errors = df[df['state'] == 'ERRORS']

        df['rats_capture_enable'] = np.where(df['state'] == 'ERRORS',df['rats_capture_enable'],'NA')
        df['EDBs in error'] = df['rats_capture_enable']

        fig = px.scatter(df, x='llc_trigger_count', y='function_number', color='state', hover_data=['llc_trigger_count','EDBs in error'],
                         title=title, render_mode='webgl', template='simple_white')

        fig.update_traces(mode='lines+markers')

        # must find a way here to include the EDB number responsible for the error state...

        if len(errors) > 0:
            fig.data[1].mode = 'markers'
            fig.data[1].marker.color = 'red'
            print(fig.data[1].hovertemplate)

    else:
        fig = px.scatter(df, x='llc_trigger_count', y='function_number', color='state', hover_data=['llc_trigger_count'],
                         title=title, render_mode='webgl')

    fig.update_layout(showlegend=False)
    fig.update_traces(marker=dict(size=12))
    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)

    return fig

def test_case(absolutepath):
    import pickle
    df = ratparser.generate_frame_from_file(absolutepath)
    fig = bigpictureplot(df,decimate=True)
    fig.write_html('test2.html')

# test_case('C:\\Users\\uksayr\\OneDrive - Waters Corporation\\Desktop\\gds_000C00_30_14092021_1520.txt')
# test_case('/users/steve/documents/workwaters/5.txt')
