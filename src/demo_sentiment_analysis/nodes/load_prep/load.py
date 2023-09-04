import pyspark.sql.dataframe as sp
import pandas as pd
import logging.config

logger = logging.getLogger(__name__)

def load_data_as_pandas_df(data: sp.DataFrame) -> pd.DataFrame:
    return data.toPandas()