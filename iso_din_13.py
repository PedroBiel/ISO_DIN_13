"""
DATOS DE LA BASE DE DATOS tornillos.db, TABLA ISO_DIN_13

27/09/2024

__author__ = Pedro Biel

__version__ = 0.0.0

__email__ = pedro.biel@abalsirengineering.com
"""

import pandas as pd
from src.utils.paths import Paths
from src.utils.sqlitepandasdf import SQLitePandasDF


class DatosISODIN13:
    def __init__(self) -> None:
        """
        Inicializa la clase DatosISODIN13, que se encarga de proporcionar acceso a los datos de la base de datos
        'tornillos.db', específicamente la tabla 'ISO_DIN_13'. Contiene métricas de M1 a M100.
        """
        # Ruta a la base de datos de tornillos
        self.ruta_datos = f'{Paths.data}\\'
        self.tornillos_db = 'tornillos.db'
        self.tabla = 'ISO_DIN_13'

        # Clase que gestiona la conexión a SQLite y la conversión a DataFrame
        self.sql_pd = SQLitePandasDF

        # Variable para cachear el DataFrame y evitar accesos repetidos a la base de datos
        self._df_cache = None

    def _load_dataframe(self) -> pd.DataFrame:
        """
        Carga el DataFrame desde la base de datos SQLite y lo cachea en memoria para evitar accesos repetidos.

        :return: DataFrame con los datos de la tabla.
        """
        if self._df_cache is None:  # Solo carga si no está cacheado
            sql_pd = self.sql_pd(f'{self.ruta_datos}{self.tornillos_db}', self.tabla)
            self._df_cache = sql_pd.sql_to_df()  # Cachea el DataFrame
        return self._df_cache

    def metricas(self) -> list[str]:
        """
        Obtiene la lista de métricas disponibles.

        :return: Lista de métricas (columna 'Metrica').
        """
        df = self._load_dataframe()
        return df['Métrica'].to_list()

    def diametros_nominales(self) -> list[float]:
        """
        Obtiene la lista de diámetros nominales (columna 'dnom_mm').

        :return: Lista de diámetros nominales en mm.
        """
        df = self._load_dataframe()
        return df['dnom_mm'].to_list()

    def diametro_nominal(self, metrica: str) -> float:
        """
        Obtiene el diámetro nominal en mm para una métrica específica.

        :param metrica: La métrica para la cual se desea obtener el diámetro nominal.
        :return: Diámetro nominal en mm.
        """
        df = self._load_dataframe()
        return df.loc[df['Métrica'] == metrica, 'dnom_mm'].item()

    def pasos(self) -> list[float]:
        """
        Obtiene la lista de pasos de rosca (columna 'paso_rosca_mm').

        :return: Lista de pasos de rosca en mm.
        """
        df = self._load_dataframe()
        return df['paso_rosca_mm'].to_list()

    def paso(self, metrica: str) -> float:
        """
        Obtiene el paso de rosca en mm para una métrica específica.

        :param metrica: La métrica para la cual se desea obtener el paso de rosca.
        :return: Paso de rosca en mm.
        """
        df = self._load_dataframe()
        return df.loc[df['Métrica'] == metrica, 'paso_rosca_mm'].item()


if __name__ == '__main__':
    from prettytable import PrettyTable

    # Inicializa PrettyTable para mostrar los resultados
    tabla = PrettyTable()

    # Crea una instancia de DatosISODIN13
    datos = DatosISODIN13()

    # Obtiene las métricas, diámetros nominales y pasos
    metricas = datos.metricas()
    diametros = datos.diametros_nominales()
    pasos = datos.pasos()

    # Añade las columnas a la tabla
    tabla.add_column('Métrica', metricas)
    tabla.add_column('Diámetro (mm)', diametros)
    tabla.add_column('Paso (mm)', pasos)

    # Imprime la tabla
    print(tabla)
