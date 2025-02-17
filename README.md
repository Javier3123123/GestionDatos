
# Gestor de Objetos y Análisis de Datos

Script que carga, filtra, ordena y guarda objetos con datos de peso y beneficio. Permite generar gráficos visuales y exportar resultados en formatos CSV, JSON o TXT. Ideal para análisis y mejoras de recursos.




## Características

- Carga de datos desde archivo local o URL
- Cálculo del peso total de los objetos
- Filtrado de objetos según el peso máximo
- Ordenamiento de objetos por beneficio y peso
- Visualización de objetos con detalles en consola
- Generación de gráficos de barras, líneas y pastel
- Guardado de resultados en formatos CSV, JSON o TXT
- Manejo de errores con registro de logs
- Configuración flexible a través de un archivo JSON
- Soporte para modo debug con información detallada
- Exportación de gráficos como imágenes PNG
- Interfaz de consola amigable con limpieza de pantalla



## Documentación

Hay varias maneras de usarlo:

- Podemos usar el script **generate.py** para generar una base de datos adecuada para el script de manera automática en base a las necesidades correspondientes.
- Y una vez generada una base de datos, se puede usar el script **main.py** para que gestione los datos de la misma y los ordene de manera flexible y adecuada a las necesidades del cliente.

Pero antes de usar nada, deberemos configurar el script en base a nuestras necesidades desde el archivo **config.json**, en el cual podremos configurar de que manera el script principal cargará, ordenará y preparará el análisis de la base de datos entregada.

Y los tipos de gráficos y archivos que se pueden guardar son:

- Archivos: csv,json y txt.
- Gráficos: pastel,barras y lineas.

Esto se debe modificar en el **config.json**