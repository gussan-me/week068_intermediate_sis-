# Snowflake 世界人口データ可視化プロジェクト

このプロジェクトは、S3に保存された世界人口データをSnowflakeで取得し、Streamlitで可視化するサンプルです。

## 概要

- **データソース**: S3バケット (`s3://frostyfridaychallenges/challenge_68/`)
- **データ内容**: 各国の2023年人口データと人口密度（JSON形式）
- **可視化**: Streamlit in Snowflakeでバーチャート表示

## セットアップ手順

### 1. Snowflakeでのデータベース準備

`setup.sql`の内容を順番に実行してください。

#### ステップ1: データベースとスキーマの作成
```sql
CREATE DATABASE IF NOT EXISTS FROSTY_FRIDAY;
USE DATABASE FROSTY_FRIDAY;
CREATE SCHEMA IF NOT EXISTS POPULATION_DATA;
USE SCHEMA POPULATION_DATA;
```

#### ステップ2: 外部ステージの作成
S3バケットへのアクセスを設定します。
```sql
CREATE OR REPLACE STAGE population_stage
    URL = 's3://frostyfridaychallenges/challenge_68/'
    FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1);
```

#### ステップ3: データの確認（オプション）
ステージ内のファイルを確認できます。
```sql
LIST @population_stage;
SELECT $1 FROM @population_stage;
```

#### ステップ4: 通常テーブルの作成
人口データを格納するテーブルを作成。
```sql
CREATE OR REPLACE TABLE POPULATION_DATA (
    country VARCHAR,      -- 国名
    pop2023 NUMBER,       -- 2023年の人口
    density NUMBER(38,10) -- 人口密度
);
```

#### ステップ5: データのロード
S3からJSON形式のデータをテーブルにロード。
```sql
COPY INTO POPULATION_DATA (country, pop2023, density)
FROM (
    SELECT 
        $1:country::VARCHAR,
        $1:pop2023::NUMBER,
        $1:density::NUMBER(38,10)
    FROM @population_stage
)
FILE_FORMAT = (TYPE = JSON STRIP_OUTER_ARRAY = TRUE)
ON_ERROR = 'CONTINUE';
```

#### ステップ6: データの確認
ロードされたデータを確認。
```sql
-- テーブルのデータを確認
SELECT * FROM POPULATION_DATA;

-- データ件数の確認
SELECT COUNT(*) AS total_countries FROM POPULATION_DATA;
```

### 2. Streamlitアプリケーションの実行

#### Streamlit in Snowflakeでの手順

1. **Snowflakeコンソールにログイン**

2. **Streamlitアプリケーションの作成**
   - 左側メニューから「Streamlit」を選択
   - 「+ Streamlit App」をクリック

3. **アプリケーション設定**
   - アプリ名を入力（例: `population_visualization`）
   - Warehouseを選択
   - データベースとスキーマを選択:
     - Database: `FROSTY_FRIDAY`
     - Schema: `POPULATION_DATA`

4. **コードの貼り付け**
   `streamlit_app.py`の内容をエディタに貼り付けます

5. **アプリケーションの実行**
   「Run」ボタンをクリックして実行
"# week068_intermediate_sis-" 
