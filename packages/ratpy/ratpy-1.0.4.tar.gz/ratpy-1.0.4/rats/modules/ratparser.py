from rats.modules.RATS_CONFIG import packet_structure, rats_input
import rats.modules.topoparser as topo
from datetime import datetime
import pandas as pd
import numpy as np
import platform
import pathlib

if __name__ == "__main__":
    from rats.modules.RATS_CONFIG import packet_structure as _packet_structure

if platform.system() == 'Windows':
    splitchar = '\\'
else:
    splitchar = '/'

packagepath = pathlib.Path(__file__).parent.parent.resolve()

def create_first_frame(filename):
    """
    Function takes in the RATS.txt file and generates an initial datafrmae which is to be operated on by subsequent
    functions. The output of this function doesn't produce a 'useable' dataframe in itself, it returns the lines of the
    text file in rows of a dataframe to facilitate manipulation with supported Pandas operations, rather than custom code
    """
    series_stream = []
    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            series_stream.append(line.strip())
            line = f.readline()

    reject_characters = ['-', ']', ':']
    df = pd.DataFrame(series_stream,columns=['bytes'])
    df = df[~df['bytes'].str.contains('|'.join(reject_characters))]
    df['index_count'] = df.index.values
    deltas = df['index_count'].diff()[1:]
    gaps = deltas[deltas>1]
    packet_number_dictionary ={}
    for i in range(len(gaps.index.values)):
        packet_number_dictionary[gaps.index.values[i]] = i
    df['packet_number'] = df['index_count'].map(packet_number_dictionary)
    df.reset_index(inplace=True)
    df.fillna(method='ffill',inplace=True)
    df.drop('index_count',axis=1,inplace=True)
    return(df)

def partition_packet_data(dataframe):
    """
    Operates on the output of create_first_frame()
    Partitions the packets into the header segments and data stream, as defined by RATS_CONFIG.py
    """
    data = dataframe.bytes.tolist()
    stream = ' '.join(data).split()
    counter = 0
    packet_dictionary = {}
    for i in packet_structure:
        if i == 'data':
            bytes = stream[counter:]
        else:
            bytes = stream[counter:counter+packet_structure[i]]

        bytes = ' '.join(bytes)
        packet_dictionary[i] = bytes
        counter += packet_structure[i]

    dataframe = pd.DataFrame.from_records([packet_dictionary])

    return(dataframe)

def validate_initial_partition(dataframe):
    """
    Take output from previous wrapper and make sure packet_number and packet_count line up, then delete packet_number
    Uses pandas built-in testing functions for now. Likely to be replaced later with better method of validation
    """
    comp1 = dataframe['packet_number'].apply(int)+1
    comp2 = dataframe['packet_count'].str.replace(' ','').apply(int,base=16)
    comp1.name = 'Test'
    comp2.name = 'Test'
    try:
        pd.testing.assert_series_equal(comp1, comp2)
        dataframe = dataframe.drop('packet_number', axis=1)
        return dataframe
    except AssertionError as e:
        print('='*5)
        print('Assertion Error has been caught:')
        print(e)
        print('=' * 5)
        print('partition_packet_data did not yield valid results; packet_number and packet_count columns are not equal')


def generate_final_frame(dataframe, rats_input={}, protocol_fudge = 0):
    """
    Takes the output of partition_packet_data() and segments the data into appropriately sized chunks. Uses the protocol
    byte to determine the data format

    Used in a wrapper function rather than directly called to modify the dataframe
    """

    # TODO: remove protocol fudge when the bug is fixed in the protocol number

    gds_protocol_version = dataframe['rats_gds_protocol_version'].iloc[0].replace(' ','')
    if (int(gds_protocol_version,16) - protocol_fudge) > 0:
        input_bytes = 4
    else:
        input_bytes = 2

    # This will generate the number and 'ID' of each EDB which is active on the RATS inputs
    active_edb_flags = f"{int(dataframe['rats_capture_enable'].iloc[0].replace(' ',''), 16):0<b}"
    flaglist = [i+1 for i, x in enumerate(active_edb_flags) if x == '1']
    bytes = dataframe['data'].iloc[0].split()
    bytes = [bytes[i:i + input_bytes] for i in range(0, len(bytes), input_bytes)]
    bytes = [''.join(x) for x in bytes]
    bytes = [bytes[i:i + len(flaglist)] for i in range(0, len(bytes), len(flaglist))]
    df_dict = dataframe.iloc[0].drop('data').to_dict()
    df_dict['data'] = bytes

    for i in df_dict:
        if i != 'data' and type(df_dict[i]) == str:
            df_dict[i] = df_dict[i].replace(' ','')

    # propagate sample rate into time column
    packet_start_time = int(df_dict['time'].replace(' ',''),16)
    number_of_samples = len(bytes)
    sample_rate = int(df_dict['rats_sample_rate'].replace(' ',''),16)
    propagated_time_column = [packet_start_time + (i*sample_rate) for i in range(number_of_samples)]

    # generate bufiss and sip columns
    # TODO: keep an eye on how the rats input edb might be formatted in future..
    #  This might need updating so that it's not in config, but is parsed
    llc_edb_index = flaglist.index(rats_input['edb'])
    siplist = []
    bufisslist = []

    #TODO: tidy up this horrendous logical fudge
    for i in bytes:
        binary_llc_edb = f"{int(i[llc_edb_index],16):0>16b}"
        siplist.append(int(binary_llc_edb[15-rats_input['llc_bit']]))
        bufisslist.append(int(binary_llc_edb[15-rats_input['bufiss_bit']]))

    df_dict['time'] = propagated_time_column
    df_dict['rats_capture_enable'] = [flaglist]
    df_dict['bufiss'] = bufisslist
    df_dict['sip'] = siplist

    df = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in df_dict.items()]))
    df.drop('level_1',axis=1,inplace=True)
    df.fillna(method='ffill',inplace=True)

    df = df.set_index(['rats_gds_protocol_version','payload_size','packet_count','time','rats_sample_rate',
                       'llc_trigger_count','function_number','sample_number','barcode_hash','retention_time',
                       'reserved','bufiss','sip']).apply(pd.Series.explode).reset_index()

    df = df[df['rats_capture_enable'] != rats_input['edb']]

    # TODO: convert to generic function and pass list of columns somehow from the definitions in the config file

    def signed_q_format(x):
        # TODO: look at scaling values here, maybe, and make sure this doesn't clash with topo - if so, move this about
        x = int(x,input_bytes*8)
        if (x & (1 << (input_bytes*8 - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
            x = x - (1 << input_bytes*8)  # compute negative value
        return x

    df['data'] = df['data'].apply(signed_q_format)

    df['function_number'] = df['function_number'].apply(int, base=16)
    df['llc_trigger_count'] = df['llc_trigger_count'].apply(int,base=16)
    df['packet_count'] = df['packet_count'].apply(int,base=16)
    df['rats_capture_enable'] = df['rats_capture_enable'].astype(int)
    df['llc_trigger_count'] = df['llc_trigger_count'].astype(int)

    return df

def generate_wrapper(dataframe):
    """
    Wraps the generate_final_frame function so that it can be used with pandas .apply() method
    """
    return generate_final_frame(dataframe,rats_input=rats_input,protocol_fudge=240) #TODO: remove fudge when possible

def find_outliers(dataframe):
    """
    Takes the final dataframe, detects the mode of the average EDB setting per function number. Uses that mode to detect
    if there has been an error and on which EDB the error occurred.
    """
    mean_df = dataframe[dataframe['sip'] == 1].groupby(['function_number','llc_trigger_count','rats_capture_enable']).mean()
    mean_df.reset_index(inplace=True)
    mean_df = mean_df[['llc_trigger_count','function_number', 'rats_capture_enable', 'data']]
    filter_df = mean_df[['function_number', 'rats_capture_enable', 'data']].groupby(['function_number', 'rats_capture_enable']).agg(pd.Series.mode)
    filter_df.reset_index(inplace=True)

    functions = mean_df.function_number.unique()
    edbs = mean_df.rats_capture_enable.unique()
    mean_df['filter'] = 0

    for i in functions:
        for j in edbs:
            mean_df['filter'] = np.where((mean_df['function_number'] == i) &
                                         (mean_df['rats_capture_enable'] == j),
                                          filter_df.loc[(filter_df['function_number'] == i) &
                                                        (filter_df['rats_capture_enable'] == j),
                                                        'data'].tolist()[0], mean_df['filter'])

    errordf = mean_df[mean_df['data'] != mean_df['filter']]
    grouped_errors = errordf.groupby('llc_trigger_count')
    error_dict = dict([(i, k.rats_capture_enable.unique().tolist()) for i,k in grouped_errors])
    dataframe['anomalous'] = 0
    for i in error_dict:
        dataframe['anomalous'] = np.where((dataframe['llc_trigger_count'] == i) & (dataframe['rats_capture_enable'].isin(error_dict[i])),
                                            1,dataframe.anomalous)
    return dataframe

def scale_and_rename_rats_inputs(dataframe,filename,protocol_fudge=240):
    active_edbs = dataframe.rats_capture_enable.unique()

    #TODO: decide if the protocol byte is enough here or if this needs to get more granular w.r.t. EDS parsing
    gds_protocol_version = dataframe['rats_gds_protocol_version'].iloc[0].replace(' ', '')
    if (int(gds_protocol_version, 16) - protocol_fudge) > 0:
        input_bytes = 4
    else:
        input_bytes = 2
    try:
        netid = filename.split(splitchar)[-1]
        netid = netid.split('.')[0]  # everything before the extension
        topodata = topo.extractscale(netid, active_edbs)

        dataframe['scaling_factors'] = dataframe['rats_capture_enable'].map(topodata[0]['scalingfactors'])
        dataframe['rats_capture_enable'] = dataframe['rats_capture_enable'].map(topodata[0]['description'])
        dataframe['minimum'] = dataframe['rats_capture_enable'].map(topodata[0]['minimum'])
        dataframe['data'] = dataframe['data'] + 2 ** ((input_bytes * 8) - 1) # This is a key step and may have to be done from EDS data
        dataframe['data'] = dataframe['minimum'] + (dataframe['data']*dataframe['scaling_factors'])
        dataframe['board'] = topodata[1]

        return dataframe

    except Exception as e:
        print(f'Failed to parse topography files and datasheets. Exception reported: {e}')
        dataframe['board'] = 'UNDEFINED - UNABLE TO PARSE TOPOLOGY DATA'
        # dataframe['data'] = dataframe['data'] + 2**((input_bytes*8)-1) # This is a key step and may have to be done from EDS data
        #
        # res = 2*(2**((input_bytes*8)-1))
        # input_range = 40
        # input_minimum = -40
        # steps = input_range/res
        # print(res)
        #
        # dataframe.data = input_minimum + (dataframe.data * steps)

        return dataframe


def generate_frame_from_file(filename):
    start_time = datetime.now()
    df = create_first_frame(filename)
    df = df.groupby('packet_number').apply(partition_packet_data)
    df.reset_index(inplace=True)
    df = validate_initial_partition(df)
    df = df.groupby('packet_count').apply(generate_wrapper)
    df = df.droplevel(0).reset_index(drop=True)
    df = scale_and_rename_rats_inputs(df,filename)
    df = find_outliers(df)

    print(f'Dataframe construction completed in: {datetime.now() - start_time}')
    print(f'dataframe for {filename} uses {df.memory_usage().sum() / 10e6} Mb in memory')

    return df



# Test Case
filename = 'C:\\Users\\uksayr\\OneDrive - Waters Corporation\\Desktop\\gds_000C00_30_14092021_1520.txt'
df = generate_frame_from_file(filename)
