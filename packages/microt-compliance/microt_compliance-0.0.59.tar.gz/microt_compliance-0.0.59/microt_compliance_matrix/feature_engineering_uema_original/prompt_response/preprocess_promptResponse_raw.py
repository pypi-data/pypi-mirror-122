"""
Functionality: Parse the content of .../logs-watch/PromptResponses.log.csv for individual participant into formatted
matrices day by day and save as csv file in the directory .../participant_id@timestudy_com/appended_response.

Usage: This script is intended mainly to be called by uema_all_features_dataframe.py.

Input: python preprocess_promptResponse_raw.py [PARTICIPANT_ID] [microT_root_path] [start_date]
e.g., python preprocess_promptResponse_raw.py aditya4_internal .../MICROT 2020-01-01

Output: csv file for each day of the participant, with each row indicating a prompted question and response
e.g., aditya4_internal_uEMA_****-**-**.csv in .../aditya4_internal@timestudy_com/appended_response
"""
import os
from os import path, sep, makedirs
import csv
import sys
import pandas.errors
from microt_compliance_matrix.utils.convert_timestamp import *
from glob import glob


columns_list = ["Prompt_Type", "Study_Mode", "Initial_Prompt_Local_Time", "Initial_Prompt_UnixTime",
                "Initial_Prompt_UTC_Offset ",
                "Answer_Status", 'Question_Set_Completion_Local_Time', 'Question_Set_Completion_UnixTime',
                'Reprompt1_Prompt_Date',
                'Reprompt1_Prompt_Local_Time', 'Reprompt1_Prompt_UnixTime',
                'Reprompt2_Prompt_Date', 'Reprompt2_Prompt_Local_Time',
                'Reprompt2_Prompt_UnixTime ', 'Reprompt3_Prompt_Date',
                'Reprompt3_Prompt_Local_Time', 'Reprompt3_Prompt_UnixTime',
                'Reprompt4_Prompt_Date', 'Reprompt4_Prompt_Local_Time',
                'Reprompt4_Prompt_UnixTime', 'Reprompt5_Prompt_Date',
                'Reprompt5_Prompt_Local_Time', 'Reprompt5_Prompt_UnixTime']

prompt_type_excluded = ['None_Sleep', 'None_Empty']

def splitMultiLogsinOneRow(row, participant_id):
    rows = []
    id_index = [i for i, s in enumerate(row) if participant_id in s]
    if len(id_index) > 1:

        error_index = id_index[1]
        split1 = row[error_index].replace(participant_id, "")
        split2 = participant_id

        row1 = row[:error_index] + [split1]
        row2 = [split2] + row[error_index + 1:]
        rows.append(row1)
        rows.append(row2)
        if len(id_index) > 2:
            rows = rows[:-1] + splitMultiLogsinOneRow(rows[-1], participant_id)
    else:
        rows.append(row)

    return rows


def extractRow(row):
    new_row = [row[1], row[2], row[10], row[9], row[8]] + row[33:]
    return new_row


def clean_response_files(intermediate_participant_path, date_in_study, participant_id):
    # Check if date folder exists
    date_folder_path = os.path.join(intermediate_participant_path, date_in_study)

    csv_path = list(glob(os.path.join(date_folder_path, 'watch_promptresponse_clean*.csv')))
    if len(csv_path) == 0:
        print(date_folder_path)
        print("No intermediate watch promptresponse csv file on {}".format(date_in_study))
        quit()


    row_list = []
    with open(csv_path[0], encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            rows = splitMultiLogsinOneRow(row, p_id)
            for single_row in rows:
                new_row = extractRow(single_row)
                row_list.append(new_row)

    df = pd.DataFrame()
    for row in row_list:
        n = 4
        prompt_type = row[0]
        study_mode = row[1]
        completeness = row[2]
        timestamp = row[3]
        time_offset = row[4]
        questions = row[5:]
        questions_grouped_list = [questions[i:i + n] for i in range(0, len(questions), n)]
        grouped_list = [[prompt_type, study_mode, completeness, time_offset, timestamp] + x for x in
                        questions_grouped_list]
        d = pd.DataFrame(grouped_list)
        df = pd.concat([df, d], axis=0)

    df.reset_index(drop=True, inplace=True)
    # write daily response df in long format to a file
    output_save_path = feature_save_path + sep + "compliance_analysis" + sep + "uEMA" + sep + "prompt_response" + sep + p_id + sep + "appended_response"
    if not path.exists(output_save_path):
        makedirs(output_save_path)
    df_temp = df
    df_temp.insert(loc=0, column='Participant_ID', value=p_id)

    if df_temp.shape[0] > 0:
        df_temp.columns = ['Participant_ID', 'Type', 'Study_Mode', 'Completion_Status', 'UTC_Offset',
                           'Prompt_Timestamp',
                           'Question_Key', 'Question_Text', 'Prompt_Response', 'Response_Timestamp']
        time_offset_unique_list = df_temp['UTC_Offset'].unique()
        time_offset_unique_list_nonnan = [x for x in time_offset_unique_list if len(x) > 0 ]
        if len(time_offset_unique_list_nonnan) == 1:
            time_offset = time_offset_unique_list_nonnan[0]
        else:
            print("*** multiple time zones for date {}: {}".format(date, time_offset_unique_list_nonnan))
            time_offset = time_offset_unique_list_nonnan[0]

        df_temp['Prompt_Local_Time'] = convert_timestamp_int_list_to_readable_time(df_temp['Prompt_Timestamp'],
                                                                                   time_offset)
        df_temp['Response_Local_Time'] = convert_timestamp_int_list_to_readable_time(df_temp['Response_Timestamp'],
                                                                                     time_offset)
        df_temp = df_temp[
            ['Participant_ID', 'Prompt_Type', 'Study_Mode', 'Completion_Status', 'UTC_Offset', 'Prompt_Timestamp',
             'Prompt_Local_Time', 'Question_Key', 'Response_Timestamp', 'Response_Local_Time']]


    return df_temp


if __name__ == "__main__":
    p_id = sys.argv[1]
    intermediate_root_path = sys.argv[2]
    feature_save_path = sys.argv[3]
    start_date = sys.argv[4]
    end_date = sys.argv[5]
    create_temporary_appended_response_files(p_id, intermediate_root_path, feature_save_path, start_date, end_date)
