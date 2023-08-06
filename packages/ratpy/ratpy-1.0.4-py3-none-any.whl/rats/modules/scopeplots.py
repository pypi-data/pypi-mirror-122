import rats.modules.ratparser as ratparser
import plotly_express as px
import pandas as pd
import numpy as np
pd.options.plotting.backend = 'plotly'
pd.options.mode.chained_assignment = None  # get rid of SettingWithCopyWarning. Default='warn'


def scopeplot(df, llc=0, buffer=1, facet=False, timescale=1000000):
    start = llc - buffer
    end = llc + buffer
    title = df.board.unique()[0]
    df['llc_trigger_count'] = df['llc_trigger_count'].astype('int')
    df['function_number'] = df['function_number'].astype('int')
    df = df[(df['llc_trigger_count'] >= start) & (df['llc_trigger_count'] <= end)]  # subsequent operations will throw SettingWithCopyWarning - false positive warning in this case
    df.reset_index(drop=True, inplace=True)
    df['timescale'] = timescale
    df['time'] = df['time'] / df['timescale']

    # time to do some DF melting to try and get SIP into a plottable format...

    sip_df = pd.melt(df, id_vars=['sip'],value_vars=['time'])
    print(sip_df.head())


    if facet:
        fig = px.line(df, x='llc_trigger_count', y='data', color='rats_capture_enable', facet_row='rats_capture_enable', hover_data=['llc_trigger_count', 'function_number'], title=title,
                      template='simple_white')
        fig.update_yaxes(matches=None)
        fig.update_layout(showlegend=False)
    #TODO: Change x to time when the info in the rats packets is correct
    else:
        #Problem here is that it won't really work for more than one active EDB....
        fig = px.line(df, x='time', y='data', color='rats_capture_enable', hover_data=['llc_trigger_count', 'function_number'], title=title,
                      template='simple_white')


        sip_series = df.sip.diff()
        sip_transitions = sip_series[sip_series != 0].index.to_list()[1:]

        sip_transitions = [(sip_transitions[i],sip_transitions[i+1]) for i in range(0,len(sip_transitions)-1,2)]
        print(sip_transitions)

        for i in sip_transitions:
            fig.add_vrect(
                x0=df.loc[i[0]:i[1], 'time'].min(),
                x1=df.loc[i[0]:i[1], 'time'].max()-1,
                fillcolor="LightSalmon", opacity=0.5,
                layer="below", line_width=0,
            )

    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)



    # make sure markers are there in case user wants a single MRM scan, which would just be a single datapoint per edb
    fig.update_traces(mode='markers+lines', marker=dict(size=4))
    return fig

def test_case(absolutepath):
    df = ratparser.generate_frame_from_file(absolutepath)
    df['time'] = [i+100 for i in range(len(df['time']))]
    fig = scopeplot(df,timescale=1)
    fig.write_html('test2.html')
    # fig2 = scopeplot(df2,timescale=1)
    # fig2.write_html('test3.html')
    # fig3 = scopeplot(df3,timescale=1)
    # fig3.write_html('test4.html')

# test_case('C:\\Users\\uksayr\\OneDrive - Waters Corporation\\Desktop\\gds_000C00_30_14092021_1520.txt')
