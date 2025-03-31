import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
DB_URL = os.environ.get("DB_URL")


def query_near_parking_lots_from_me(
    distance_from_me=500, current_longitude=0, current_latitude=0
):
    return text(
        f"""
               with transform_coordenates AS (
                   select
                       distrito, barrio,
                       calle, num_finca, color,
                       bateria_linea, num_plazas,
                       gis_x, gis_y,
                       ST_X(ST_Transform(ST_SetSRID(ST_MakePoint(gis_x::double precision, gis_y::double precision), 25830), 4326)) AS longitud,
                       ST_Y(ST_Transform(ST_SetSRID(ST_MakePoint(gis_x::double precision, gis_y::double precision), 25830), 4326)) AS latitud
                   from 
                       public.calles_zona_ser_formatted
                ),
                distance_from_me as (
                   select 
                       *,
                       ST_Distance(
                           ST_SetSRID(ST_MakePoint({current_longitude}, {current_latitude}), 4326)::geography,
                           ST_SetSRID(ST_MakePoint(transform_coordenates.longitud, transform_coordenates.latitud), 4326)::geography
                       ) AS distancia_metros  
                   from 
                       transform_coordenates
                )
                select 
                    *
                from 
                   distance_from_me
                where 
                   distancia_metros <= {distance_from_me} and color like '%Azul%'
                order by distancia_metros; 
           """
    )


def get_nearest_parking_lot(current_longitude=0, current_latitude=0):
    return text(
        f"""
            with transform_coordenates AS (
                select
                    distrito, barrio,
                    calle, num_finca, color,
                    bateria_linea, num_plazas,
                    gis_x, gis_y,
                    ST_X(ST_Transform(ST_SetSRID(ST_MakePoint(gis_x::double precision, gis_y::double precision), 25830), 4326)) AS longitud,
                    ST_Y(ST_Transform(ST_SetSRID(ST_MakePoint(gis_x::double precision, gis_y::double precision), 25830), 4326)) AS latitud
                from 
                    public.calles_zona_ser_formatted
             ),
             distance_from_me as (
                select 
                    *,
                    ST_Distance(
                        ST_SetSRID(ST_MakePoint({current_longitude}, {current_latitude}), 4326)::geography,
                        ST_SetSRID(ST_MakePoint(transform_coordenates.longitud, transform_coordenates.latitud), 4326)::geography
                    ) AS distancia_metros  
                from 
                    transform_coordenates
             ),
             select 
                 *
             from 
                distance_from_me
             where 
                distance_from_me.distancia_metros <= 800 and color like '%Azul%'
             order by distancia_metros 
             limit 1; 
        """
    )


def get_parking_lots_around_me(
    logger, distance_from_me=500, current_longitude=0, current_latitude=0
):
    query = query_near_parking_lots_from_me(
        distance_from_me, current_longitude, current_latitude
    )
    try:
        engine = create_engine(DB_URL)
        with engine.connect() as conn:
            result = conn.execute(query)

            logger.info(f"EXECUTED QUERY: {query}\n\n")

            return result.fetchall()

    except Exception as e:
        logger.error(e)
