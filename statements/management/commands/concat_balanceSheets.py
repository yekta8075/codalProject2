from django.core.management import BaseCommand
from sqlalchemy import create_engine
from statements.models import Statements
import pandas as pd
import dateutil.parser as dparser


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        try:
            statement_json_list = get_balance_sheets_from_db()
            final_balance_sheets = concat_balance_sheets(statement_json_list)
            final_balance_sheet_after_remove_null_index = remove_rows_of_dataframe_with_null_index(final_balance_sheets)
            save_concat_balance_sheets_in_database(final_balance_sheet_after_remove_null_index)
        except Exception as e:
            print(e)


def get_balance_sheets_from_db():
    balance_sheets_from_db = Statements.objects.values()
    balance_sheets_dataframe = pd.DataFrame(balance_sheets_from_db)
    statement_json_list = balance_sheets_dataframe['statement_json']
    return statement_json_list


def concat_balance_sheets(statement_json_list):
    final_balance_sheets = pd.DataFrame()

    for statement_json in statement_json_list:
        statement_json_to_df = pd.DataFrame(statement_json)
        dataframe_of_required_columns = create_dataframe_from_required_columns(statement_json_to_df)
        final_balance_sheets = pd.concat([final_balance_sheets, dataframe_of_required_columns], axis=1)
    return final_balance_sheets


def create_dataframe_from_required_columns(statement_json_to_df):
    body_column = create_body_column(statement_json_to_df)
    index_column = create_index_column(statement_json_to_df)
    column_name = get_column_name(statement_json_to_df)
    dataframe_of_required_columns = pd.DataFrame(data=body_column, columns=[column_name])
    dataframe_of_required_columns = dataframe_of_required_columns.set_index(index_column)
    return dataframe_of_required_columns


def create_body_column(statement_json_to_df):
    body_dataframe = pd.Series()
    dataframe_columns_name = statement_json_to_df.columns
    for item in dataframe_columns_name:
        if 'عملکرد واقعی' in item:
            body_dataframe = body_dataframe.append(statement_json_to_df[item],ignore_index=True)
    return body_dataframe


def create_index_column(statement_json_to_df):
    index_dataframe = pd.Series()
    dataframe_column_name = statement_json_to_df.columns
    for item in dataframe_column_name:
        if 'شرح' in item:
            index_dataframe = index_dataframe.append(statement_json_to_df[item], ignore_index=True)
    return index_dataframe


def get_column_name(statement_json_to_df):
    column_name = None
    for item in statement_json_to_df.columns:
        if 'عملکرد واقعی' in item:
            column_name = get_date(item)
            break
    return column_name


def get_date(item):
    return dparser.parse(item, fuzzy=True).strftime('%Y/%m/%d')


def remove_rows_of_dataframe_with_null_index(final_balance_sheets):
    final_balance_sheets = final_balance_sheets[final_balance_sheets.index.notnull()]
    return final_balance_sheets


def save_concat_balance_sheets_in_database(final_balance_sheet_after_remove_null_index):
    try:
        engine = create_engine('postgresql://postgres:123456@localhost:5432/notifications', echo=False)
        final_balance_sheet_after_remove_null_index.to_sql('concatBalanceSheets', engine, if_exists='replace', index=True)
    except Exception as e:
        print(e)
