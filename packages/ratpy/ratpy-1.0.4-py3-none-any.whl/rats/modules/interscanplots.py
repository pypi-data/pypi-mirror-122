import rats.modules.ratparser as ratparser
import pandas as pd
import plotly_express as px
pd.options.mode.chained_assignment = None

def interscanplot(df, timescale=1000000):
    title = 'title'
    df = df[['function_number', 'time', 'llc_trigger_count']].drop_duplicates()
    df = df.set_index(['function_number', 'llc_trigger_count']).diff()
    df = df.reset_index()
    df = df.iloc[1:]
    df.loc[:, 'timescale'] = timescale
    df.loc[:, 'time'] = df['time']/df['timescale']
    df = df.sort_values('function_number', ascending=False)

    fig = px.violin(df, x='time', y='function_number', color='function_number', orientation='h',
                    title=title).update_traces(side='positive', width=2.5)
    fig.update_yaxes(type='category')
    fig.update_layout(plot_bgcolor='#fff')

    return fig


def test_case(absolutepath):
    df = ratparser.generate_frame_from_file(absolutepath)
    print(df.data.max())
    df['time'] = [i+100 for i in range(len(df.time))]
    fig = interscanplot(df)
    fig.write_html('test2.html')

# test_case('gds_000C00_30_14092021_1520.txt')
