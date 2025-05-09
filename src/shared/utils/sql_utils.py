import streamlit as st
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


load_dotenv()
CONNECTION_STRING = os.getenv("CONNECTION_STRING")
DB_SCHEMA = os.getenv("DB_SCHEMA")
DB_TABLE = os.getenv("DB_TABLE")

def load_sql_template(filename: str) -> str:
    """Carga un archivo .sql como string"""
    current_dir = os.path.dirname(__file__)
    sql_path = os.path.join(current_dir, "sql", filename)
    with open(sql_path, "r") as file:
        return file.read()

def execute_query(logger, query_text: str):
    """Ejecuta una query en la base de datos"""
    try:
        engine = create_engine(CONNECTION_STRING)
        with engine.connect() as conn:
            result = conn.execute(query_text)
            logger.info(f"Query ejecutada: {query_text}")
            return result.fetchall()
    except Exception as e:
        logger.error(f"Error ejecutando query: {str(e)}")
        return []

@st.cache_data
def get_nearest_parking_lot_from_user(
    _logger, distance_from_me=500, current_longitude=0, current_latitude=0
):
    """Ejecuta una consulta para obtener el aparcamiento más cercano al usuario."""
    sql_template = load_sql_template("user_nearest_parking_lot.sql")
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
    """Ejecuta una consulta para obtener aparcamientos cercanos a la ubicación del usuario."""
    sql_template = load_sql_template("near_parking_lots.sql")
    formatted_query = sql_template.format(
        distance_from_me=distance_from_me,
        current_longitude=current_longitude,
        current_latitude=current_latitude,
        table_schema=DB_SCHEMA,
        table_name=DB_TABLE
    )
    query =  text(formatted_query)
    return execute_query(_logger, query)
