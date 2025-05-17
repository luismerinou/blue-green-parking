# Blue parking streamlit app

Tu nueva app para encontrar plazas azules cercanas a tu ubicación en la Zona SER de Madrid 🚀🚙


## **🌍 Transformación de Coordenadas UTM a Latitud y Longitud (WGS84)**

Este proyecto utiliza **datos geoespaciales** provenientes del **Ayuntamiento de Madrid**, que se encuentran en un formato específico basado en las coordenadas **UTM (Universal Transverse Mercator)** del sistema geodésico **ETRS89**, correspondiente a la cartografía base de la ciudad de Madrid, edición 2013, a escala 1:1.000. Estos datos provienen de la restitución de vuelos fotogramétricos y cubren todo el término municipal, siendo la serie de mayor detalle disponible. 

### **❓ ¿Por qué es necesario realizar esta transformación?**

Los **sistemas de referencia de coordenadas** (SRC) son marcos matemáticos que definen cómo se representan las ubicaciones geográficas en un plano. Existen diferentes sistemas que se utilizan para distintos fines, dependiendo de la precisión y el área geográfica en la que se apliquen.

- **UTM (Universal Transverse Mercator)**: Un sistema proyectado que divide la Tierra en zonas, adecuado para representar áreas pequeñas o medianas con alta precisión.
- **WGS84**: El sistema utilizado globalmente en GPS y mapas en línea, basado en latitud y longitud, que es ampliamente compatible con aplicaciones como Google Maps, OpenStreetMap, etc.

Los **datos del Ayuntamiento de Madrid** están en **coordenadas UTM ETRS89**, lo que significa que están representados en un sistema proyectado, específico para España y, más concretamente, para la ciudad de Madrid. Este formato es muy preciso para análisis y planificación urbana, pero **no es compatible directamente** con plataformas de mapas web que suelen trabajar con **latitud y longitud en el sistema WGS84**.

Por esta razón, necesitamos **convertir las coordenadas UTM ETRS89** a **latitud y longitud en WGS84**, para poder visualizar y trabajar con estos datos en aplicaciones geoespaciales globales (como mapas de Google Maps o sistemas de GPS).

## 🌍 Contexto y Necesidad de la Transformación de Coordenadas

### ¿Por qué es necesario transformar las coordenadas? 🤔

Los datos geoespaciales que estamos utilizando provienen del **Ayuntamiento de Madrid**, específicamente de la cartografía base del año **2013**, con una escala de 1:1.000. Estos datos están en un formato específico que utiliza el **sistema de coordenadas UTM ETRS89**. El motivo por el cual es necesario transformar estas coordenadas es que el sistema **UTM** es adecuado para representar áreas locales con gran detalle, pero no es compatible con la mayoría de las herramientas y servicios modernos que utilizan **latitud y longitud**.

### UTM vs WGS84: ¿Cuál es la diferencia? 🌐

**UTM (Universal Transverse Mercator)** y **WGS84 (World Geodetic System 1984)** son dos sistemas de referencia geodésicos diferentes, y cada uno tiene un propósito distinto:

#### **1. UTM (Universal Transverse Mercator)**: 🌍

- **Sistema de proyección plana**: UTM utiliza una proyección cartesiana para representar la superficie curva de la Tierra en un plano.
- **Coordenadas en metros**: Las coordenadas en UTM se expresan en **metros**, con dos valores: **Este (X)** y **Norte (Y)**. Es ideal para áreas locales.
- **División en zonas**: El mundo se divide en 60 zonas de 6 grados de longitud. Cada zona tiene su propio sistema de coordenadas, lo que ayuda a minimizar las distorsiones.
- **Uso principal**: Mapas locales y regionales, análisis geoespacial detallado.

#### **2. WGS84 (World Geodetic System 1984)**: 🌐

- **Sistema global**: WGS84 es un sistema de referencia geodésico global utilizado por GPS y mapas en línea, como Google Maps.
- **Coordenadas en grados**: Las coordenadas en **WGS84** se expresan en **latitud** y **longitud**, en grados. 
- **Sistema esférico**: Modela la Tierra como una esfera (aproximada), lo que permite representar ubicaciones en cualquier parte del planeta.
- **Uso común**: GPS, aplicaciones de mapas en línea, navegación.

#### **¿Por qué necesitamos la transformación?**

La **transformación de coordenadas UTM a WGS84** es necesaria porque el formato de datos que estamos utilizando está basado en UTM (coordenadas cartesianas en metros), mientras que la mayoría de las aplicaciones y servicios modernos utilizan **latitud y longitud en grados** (WGS84). Para poder integrar estos datos en herramientas como **Google Maps** o para realizar cálculos geoespaciales globales, necesitamos transformar las coordenadas de **metros a grados**.

## 🛠️ Uso de la Extensión PostGIS en PostgreSQL

### ¿Qué es PostGIS? 🔍

**PostGIS** es una extensión de **PostgreSQL** que permite almacenar, consultar y analizar datos espaciales en una base de datos. Esta extensión añade soporte para tipos de datos geoespaciales, como puntos, líneas y polígonos, y proporciona una serie de funciones poderosas para realizar operaciones geográficas.

#### **Funciones principales de PostGIS**:

- **Tipos de datos espaciales**: Permite trabajar con coordenadas geográficas y proyecciones, como **puntos, líneas y polígonos**, almacenando estos datos en un formato optimizado.
- **Transformaciones de coordenadas**: Con PostGIS podemos transformar coordenadas de un sistema a otro, como convertir coordenadas UTM a WGS84.
- **Operaciones geoespaciales**: Funciones para calcular distancias, áreas, intersección entre objetos geográficos, y más.

### **Beneficios de usar PostGIS**:

- **Optimización en el manejo de datos espaciales**: Al usar PostGIS, las consultas espaciales se optimizan, lo que permite realizar operaciones geoespaciales de manera más rápida y eficiente.
- **Transformación de sistemas de coordenadas**: Gracias a funciones como `ST_Transform`, podemos realizar conversiones entre diferentes sistemas de referencia geodésica (como UTM y WGS84), lo que es esencial para trabajar con datos geoespaciales provenientes de diferentes fuentes.
- **Facilidad de integración con otras herramientas**: PostGIS permite una integración fluida con sistemas como **QGIS**, **ArcGIS** y otros servicios de mapas en línea, que generalmente requieren coordenadas en WGS84.
- **Análisis geoespacial avanzado**: Podemos calcular distancias, áreas, intersecciones, y realizar otras operaciones geoespaciales complejas para análisis más profundos.



### **🔧 Funciones `ST_*` utilizadas en la transformación:**
Las funciones `ST_*` que usamos en nuestras consultas son proporcionadas por esta extensión y están diseñadas para trabajar con datos geoespaciales de manera optimizada.


1. **`ST_MakePoint(gis_x, gis_y)`**:
   - Crea un **punto geográfico** a partir de las coordenadas **X** y **Y** proporcionadas en la base de datos. En este caso, las coordenadas están en el sistema UTM, por lo que inicialmente solo tenemos una representación en ese sistema.
   
   - **Por qué es importante**: Necesitamos esta función para crear una geometría que podamos trabajar y manipular en PostgreSQL.

2. **`ST_SetSRID(point, 25830)`**:
   - Asigna un **Sistema de Referencia de Coordenadas (SRID)** a la geometría creada. En este caso, el SRID **25830** corresponde a **UTM ETRS89** para la zona 30N.
   
   - **Por qué es importante**: Asignar el SRID correcto le dice a PostgreSQL qué tipo de sistema de coordenadas estamos utilizando, lo que es crucial para realizar cálculos geoespaciales precisos.

3. **`ST_Transform(point, 4326)`**:
   - Convierte las coordenadas de **UTM** (SRID 25830) a **WGS84** (SRID 4326), que es el sistema de coordenadas basado en **latitud y longitud**.
   
   - **Por qué es importante**: La transformación es esencial porque los sistemas de coordenadas pueden tener diferentes proyecciones y escalas. **ST_Transform** asegura que las coordenadas se conviertan correctamente de un sistema a otro.

4. **`ST_X` y `ST_Y`**:
   - Después de la conversión, **`ST_X`** y **`ST_Y`** extraen las coordenadas de **longitud** (X) y **latitud** (Y)** de la geometría transformada.
   
   - **Por qué es importante**: Estas funciones nos permiten acceder a los valores específicos de latitud y longitud después de la conversión, que es lo que utilizaremos en el proyecto.

### **💡 ¿Por qué PostGIS es necesario?**

Sin **PostGIS**, sería muy difícil realizar cálculos de distancias y conversiones de coordenadas de manera eficiente dentro de la base de datos. Las funciones `ST_*` proporcionan un conjunto de herramientas avanzadas para trabajar con datos espaciales sin necesidad de exportar los datos a otro software o realizar cálculos manualmente.

Con PostGIS, podemos realizar tareas complejas directamente desde la base de datos, como:

- **Conversión de coordenadas** (de UTM a WGS84).
- **Cálculo de distancias** entre puntos geográficos.
- **Búsqueda de puntos cercanos** a una ubicación específica.

Todo esto mejora la eficiencia y precisión del manejo de datos geoespaciales en el proyecto y nos permite construir aplicaciones geoespaciales potentes y fáciles de usar.

### **¿Qué pasaría si no usamos PostGIS?** 🚫

Si no utilizamos PostGIS y no transformamos las coordenadas, nos enfrentaríamos a varias dificultades:

- **Incompatibilidad con herramientas modernas**: Las coordenadas en UTM no se integran fácilmente con plataformas globales como **Google Maps**, **GPS**, y otros sistemas que requieren coordenadas en **latitud y longitud (WGS84)**.
- **Cálculos complejos y lentos**: Sin PostGIS, tendríamos que escribir consultas personalizadas y mucho más complejas para realizar operaciones como la transformación de coordenadas o el cálculo de distancias.
- **Dificultades en el análisis geoespacial**: Sin PostGIS, no podríamos aprovechar las poderosas funciones geoespaciales que ofrece PostgreSQL, lo que haría que las tareas de análisis espacial fueran mucho más difíciles y menos eficientes.

---


---

### **📊 Formato de los Datos de Origen**

Los datos de coordenadas UTM provienen del Ayuntamiento de Madrid y están organizados de la siguiente manera:

| Descripción       | Valores esperados   |
|-------------------|---------------------|
| **1. Gis_X**      | Coordenada X, proyección UTM, ETRS89 |
| **2. Gis_Y**      | Coordenada Y, proyección UTM, ETRS89 |
| **3. Cod_Distrito**| Código numérico del distrito |
| **4. Distrito**   | Nombre del distrito |
| **5. Cod_Barrio** | Código del barrio dentro del distrito |
| **6. Barrio**     | Nombre del barrio |
| **7. Calle**      | Nombre de la calle |
| **8. Número de Finca** | Número de finca |
| **9. Color**      | Codificación RGB (Ej. Verde, Azul, Rojo, Naranja) |
| **10. Batería/Línea** | Tipo de aparcamiento |
| **11. Número de Plazas** | Número de plazas disponibles |

Estas coordenadas están en el sistema **UTM ETRS89**, el cual es un sistema proyectado utilizado principalmente en España, basado en la proyección **Transversa de Mercator**. Esto es adecuado para representar áreas grandes de forma precisa, pero **no se puede usar directamente en aplicaciones de mapas globales**, como los que utilizan **latitud y longitud en el sistema WGS84**. Por ello, es necesario realizar la **transformación** de estas coordenadas UTM a latitud y longitud.

---

## 💡 Conclusión

La transformación de coordenadas y el uso de PostGIS son pasos esenciales para poder trabajar con los datos geoespaciales de manera eficiente y compatible con herramientas globales y modernas. PostGIS nos proporciona las funcionalidades necesarias para manipular, transformar y analizar datos espaciales de forma efectiva, asegurando la integridad y precisión de los resultados.

Gracias a estas herramientas, podemos convertir las coordenadas UTM del Ayuntamiento de Madrid a un formato más accesible y utilizado globalmente (WGS84), lo que nos permite integrar los datos con plataformas de mapas, realizar análisis espaciales y ofrecer resultados precisos.


