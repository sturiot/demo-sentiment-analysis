import logging.config
import mlflow.sklearn
from pyspark.sql import SparkSession
import pandas as pd

logger = logging.getLogger(__name__)


def get_model(parameters):

    model_name = parameter["mlflow"]["model_name"]
    model_version = parameter["mlflow"]["model_version"]

    # load model
    model = mlflow.sklearn.load_model(model_uri=eval(parameters["mlflow"]["model_uri"]))
    return model

def do_pandas_to_spark_dataframe(data: pd.DataFrame):
    spark = SparkSession.builder.getOrCreate()
    return spark.createDataFrame(data).coalesce(1)

def predict(data: list, model):
    predictions = model.predict(data)
    data_scored = pd.DataFrame({"review": data, "predictions": predictions})

    return do_pandas_to_spark_dataframe(data_scored)