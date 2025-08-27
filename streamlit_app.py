import streamlit as st
from snowflake.snowpark.context import get_active_session

# Snowflakeセッションの取得
# Streamlit in Snowflakeでは、get_active_session()を使用して
# 自動的に現在のセッションコンテキストを取得できます
session = get_active_session()

# アプリケーションのタイトル設定
# スペイン語圏の国々の人口を表示することを明示
st.title("Spanish Speaking Countries by Pop")

# 通常テーブルからデータを取得
# POPULATION_DATAは、S3からデータをロード済みの通常テーブル
# 通常テーブルを使用することで、高速なクエリパフォーマンスを実現
created_dataframe = session.table("FROSTY_FRIDAY.POPULATION_DATA.POPULATION_DATA")

# SnowparkデータフレームをPandasデータフレームに変換
queried_data = created_dataframe.to_pandas()

# 棒グラフの作成と表示
# x軸: 国名（COUNTRY）
# y軸: 2023年の人口（POP2023）
st.bar_chart(data=queried_data, x="COUNTRY", y="POP2023")