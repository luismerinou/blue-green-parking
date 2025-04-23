with
distance_from_me as (
    select  
    longitud,
    latitud,
    barrio,
    calle,
    num_finca,
    color,
    bateria_linea,
    num_plazas,
        ST_Distance(
            ST_SetSRID(ST_MakePoint({current_longitude}, {current_latitude}), 4326)::geography,
            ST_SetSRID(ST_MakePoint(longitud, latitud), 4326)::geography
        ) AS distancia_metros  
    from 
        {table_schema}.{table_name}
)
select 
    *
from 
    distance_from_me
where 
    distancia_metros <= {distance_from_me}
order by distancia_metros 
limit 50; 