import os

import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
CONNECTION_STRING = os.getenv("CONNECTION_STRING")
DB_SCHEMA = os.getenv("DB_SCHEMA")
DB_TABLE = os.getenv("DB_TABLE")

def load_sql_template(filename: str) -> str:
    current_dir = os.path.dirname(__file__)
    sql_path = os.path.join(current_dir, filename)
    print(sql_path)
    with open(sql_path, "r") as file:
        return file.read()

def execute_query(_logger, query):
    try:
        engine = create_engine(CONNECTION_STRING)
        with engine.connect() as conn:
            result = conn.execute(query)

            _logger.info(f"EXECUTED QUERY: {query}\n\n")

            return result.fetchall()

    except Exception as e:
        _logger.error(e)
        return []

@st.cache_data
def get_nearest_parking_lot_from_user(
    _logger, distance_from_me=500, current_longitude=0, current_latitude=0
):
    sql_template = load_sql_template("sql/user_nearest_parking_lot.sql")
    formatted_query = sql_template.format(
        distance_from_me=distance_from_me,
        current_longitude=current_longitude,
        current_latitude=current_latitude,
        table_schema=DB_SCHEMA,
        table_name=DB_TABLE
    )
    query =  text(formatted_query)
    return execute_query(_logger, query)

@st.cache_data
def get_parking_lots_around_me(
    _logger, distance_from_me=500, current_longitude=0, current_latitude=0
):
    sql_template = load_sql_template("sql/near_parking_lots.sql")
    formatted_query = sql_template.format(
        distance_from_me=distance_from_me,
        current_longitude=current_longitude,
        current_latitude=current_latitude,
        table_schema=DB_SCHEMA,
        table_name=DB_TABLE
    )
    query =  text(formatted_query)
    return execute_query(_logger, query)
