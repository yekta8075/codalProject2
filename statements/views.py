# import json
# from functools import reduce
# from io import StringIO
# from django.shortcuts import render
# import pandas as pd
# from selenium import webdriver
# from .models import Statements
# import glob
# import os
#
#
# def read_html(request):
#     driver = webdriver.Chrome(executable_path='C:\\Users\\asus\\PycharmProjects\\codalProject2\\chromedriver.exe')
#     path = 'C:\\Users\\asus\\Desktop\\statements\\*.html'
#     urls = glob.glob(path)
#
#     for url in urls:
#         filename = os.path.basename(url)
#         driver.get(url)
#         page_source = driver.page_source
#         dfs_list = pd.read_html(StringIO(page_source))
#         df_result = create_final_df(dfs_list)
#         df_to_json = df_result.to_json()
#         parsed = json.loads(df_to_json)
#         Statements.objects.update_or_create(statement_json=parsed, statement_title=filename)
#     return render(request, 'statement/statement.html')
#
#
# def create_final_df(dfs_list):
#     df_result = None
#     if len(dfs_list) == 1:
#         df_result = dfs_list[0]
#
#     elif len(dfs_list) > 1:
#         df0_row = dfs_list[0].shape[0]
#         df1_row = dfs_list[1].shape[0]
#         df0_col = dfs_list[0].shape[1]
#         df1_col = dfs_list[1].shape[1]
#         if df0_row == 0 or df1_row == 0:
#             if df0_col == df1_col:
#                 header_df_result = dfs_list[0] if df0_row == 0 else dfs_list[1]
#                 body_df_result = dfs_list[1] if df0_row == 0 else dfs_list[0]
#                 df_result = pd.DataFrame(body_df_result.values, columns=header_df_result.columns)
#             elif df0_col != df1_col:
#                 different_col = abs(df0_col - df1_col)
#                 small_df = dfs_list[0] if df0_col < df1_col else dfs_list[1]
#                 for i in range(different_col):
#                     small_df.insert(0, 'ItemId_' + str(i), None)
#                 header_df_result = small_df
#                 body_df_result = dfs_list[1] if df0_row == 0 else dfs_list[0]
#                 df_result = pd.DataFrame(body_df_result.values, columns=header_df_result.columns)
#
#         elif df0_row > 0 and df1_row > 0:
#             df_result = dfs_list[0] if df0_row > df1_row else dfs_list[1]
#     return df_result
