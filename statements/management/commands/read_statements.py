from django.core.management.base import BaseCommand
from io import StringIO
import json
import pandas as pd
from selenium import webdriver
import glob
import os
from statements.models import Statements


class Command(BaseCommand):
    help = 'read html file and extract data from tables'

    def handle(self, *args, **kwargs):

        try:
            driver = webdriver.Chrome(executable_path = 'C:\\Users\\asus\\PycharmProjects\\codalProject2\\chromedriver.exe')
            path_of_html_files = 'C:\\Users\\asus\\Desktop\\statements\\balanceSheet\\zob\\*.html'
            urls_of_html_files = glob.glob(path_of_html_files)

            for url in urls_of_html_files:
                statement_filename = os.path.basename(url)
                driver.get(url)
                html_page_source = driver.page_source
                list_of_dataframes = pd.read_html(StringIO(html_page_source))
                final_dataframe = merge_dataframes(list_of_dataframes)
                dataframe_to_json = final_dataframe.to_json()
                dataframe_to_json_to_string = json.loads(dataframe_to_json)
                Statements.objects.update_or_create(statement_json=dataframe_to_json_to_string,
                                                    statement_title=statement_filename)

        except Exception as e:
                print(e , statement_filename)


def merge_dataframes(list_of_dataframes):

    if len(list_of_dataframes) == 1:
        df_result = list_of_dataframes[0]
    elif len(list_of_dataframes) > 1:
        if is_dataframe_header_and_body_separate(list_of_dataframes):
            df_result = concat_dataframe_header_and_body(list_of_dataframes)
        elif are_dataframes_different(list_of_dataframes):
            df_result = get_major_table(list_of_dataframes)
    return df_result


def concat_dataframe_header_and_body(list_of_dataframes):
    if get_column_count(list_of_dataframes[0]) == get_column_count(list_of_dataframes[1]):
        df_result = dataframe_has_same_columns(list_of_dataframes)

    elif get_column_count(list_of_dataframes[0]) != get_column_count(list_of_dataframes[1]):
        df_result = dataframe_has_different_columns(list_of_dataframes)
    return df_result


def is_dataframe_header_and_body_separate(list_of_dataframes):
    return get_row_count(list_of_dataframes[0]) == 0 or\
           get_row_count(list_of_dataframes[1]) == 0


def are_dataframes_different(list_of_dataframes):
    return get_row_count(list_of_dataframes[0]) > 0 and\
           get_row_count(list_of_dataframes[1]) > 0


def get_major_table(list_of_dataframes):
    df_result = list_of_dataframes[0] if \
        get_row_count(list_of_dataframes[0]) > get_row_count(list_of_dataframes[1]) \
        else list_of_dataframes[1]
    return df_result


def dataframe_has_same_columns(list_of_dataframes):
    header_of_dataframe = list_of_dataframes[0] if get_row_count(list_of_dataframes[0]) == 0 else list_of_dataframes[1]
    body_of_dataframe = list_of_dataframes[1] if get_row_count(list_of_dataframes[0]) == 0 else list_of_dataframes[0]
    df_result = pd.DataFrame(body_of_dataframe.values, columns=header_of_dataframe.columns)
    return df_result


def dataframe_has_different_columns(list_of_dataframes):
    col0 = get_column_count(list_of_dataframes[0])
    col1 = get_column_count(list_of_dataframes[1])
    different_col = abs(col0 - col1)
    small_df = list_of_dataframes[0] if col0 < col1 else list_of_dataframes[1]
    for i in range(different_col):
        small_df.insert(0, 'ItemId_' + str(i), None)
    header_df_result = small_df
    body_df_result = list_of_dataframes[1] if get_row_count(list_of_dataframes[0]) == 0 else list_of_dataframes[0]
    df_result = pd.DataFrame(body_df_result.values, columns=header_df_result.columns)
    return df_result


def get_row_count(list_of_dataframes):
    return list_of_dataframes.shape[0]


def get_column_count(list_of_dataframes):
    return list_of_dataframes.shape[1]



