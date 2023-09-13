import logging.config
import mlflow.sklearn
from pyspark.sql import SparkSession
import pandas as pd

logger = logging.getLogger(__name__)


def get_model(parameters):

    model_name = parameters["mlflow"]["model_name"]
    model_version = parameters["mlflow"]["model_version"]

    # load model
    model = mlflow.sklearn.load_model(model_uri=eval(parameters["mlflow"]["model_uri"]))
    return model

def load_model(model):
    return model

def do_pandas_to_spark_dataframe(data: pd.DataFrame):
    spark = SparkSession.builder.getOrCreate()
    return spark.createDataFrame(data).coalesce(1)

def predict_to_spark_dataframe(data: list, model):
    predictions = model.predict(data)
    data_scored = pd.DataFrame({"review": data, "predictions": predictions})

    return do_pandas_to_spark_dataframe(data_scored)

def predict_to_pandas_dataframe(data: list, model):
    predictions = model.predict(data)
    data_scored = pd.DataFrame({"review": data, "predictions": predictions})

    return data_scored, predictions