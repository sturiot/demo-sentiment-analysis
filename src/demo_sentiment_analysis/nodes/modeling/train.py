import logging.config
import os
from pathlib import Path
from typing import Dict, List

import pandas as pd
import matplotlib.pyplot as plt
import time
import shap
from .metrics import calculate_metrics, confusion_matrix_as_figure
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

import mlflow
import mlflow.sklearn

logger = logging.getLogger(__name__)

def dummy_function(data):
    return data

def split_data(data: pd.DataFrame, parameters: Dict) -> List:
    X_train, X_test, y_train, y_test = train_test_split(
        data["review"].to_list(),
        data["sentiment"].to_list(),
        test_size=parameters["test_size"],
        random_state=parameters["random_state"]
    )

    return [X_train, X_test, y_train, y_test]


def training(X_feat_train, X_feat_test, y_train, y_test, model, params):
    logger.info("\n(node:train.training): start ==================================\n")

    mlflow.set_tracking_uri(params["mlflow"]["tracking_uri"])
    mlflow.set_experiment(params["mlflow"]["experiment_name"])

    with mlflow.start_run(run_name=params["mlflow"]["run_name"]):
        # 1 - Load model params
        penalty = params["linear_regression"]["penalty"]
        max_iter = params["linear_regression"]["max_iter"]
        C = params["linear_regression"]["C"]

        # 2 - Log model parameters into mlflow
        mlflow.log_param("penalty", penalty)
        mlflow.log_param("max_iter", max_iter)
        mlflow.log_param("C", C)

        # 3 - Build the model
        logger.info("\n(node:trin.training): training model ==================================\n")
        tic = time.time()

        log_reg_model = LogisticRegression(
            penalty=penalty,
            max_iter=max_iter,
            C=C
        ).fit(X_feat_train, y_train)
        logger.info("secs: {0}".format(time.time() - tic))
        
        # 4 - Load the model itself
        log_reg_model_model_info = mlflow.sklearn.log_model(
            sk_model=log_reg_model,
            artifact_path='log_reg_model',
            conda_env=str(Path(os.getcwd()).joinpath(params["mlflow"]["conda_env"]))
        )

        # 5 - Log model performance metrics into mlflow
        predictions = log_reg_model.predict(X_feat_test)
        accuracy, precision, recall, F1_score = calculate_metrics(y_test, predictions)
        confusion_matrix = confusion_matrix_as_figure(y_test, predictions)
        mlflow.log_figure(confusion_matrix.plot().figure_, 'confusion_matrix.png')
        plt.clf()

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("F1_score", F1_score)

        # 6 - Explained the model with Shap
        vectorizer = model["bow_model"]
        explainer = shap.LinearExplainer(log_reg_model, X_feat_train, feature_names=vectorizer.get_feature_names_out())
        shap_values = explainer.shap_values(X_feat_test)
        shap.summary_plot(shap_values, X_feat_test.toarray(), feature_names=vectorizer.get_feature_names_out(), show=False)
        mlflow.log_figure(plt.gcf(), 'shap_summary_plot.png')
        plt.clf()

        # 7 - Complete model performance metrics and explainability with mlflow auto evaluate feature
        # mlflow.evaluate(
        #     model=log_reg_model_model_info.model_uri,
        #     dataset_name='imdb',
        #     data=X_feat_test.toarray(),
        #     targets=y_test,
        #     model_type="classifier",
        #     evaluators=["default"],
        #     feature_names=vectorizer.get_feature_names_out()
        # )

        # 8 - Add model to the pipeline
        model.steps.append(['log_reg_model', log_reg_model])

        # 9 - Log the pipeline into mlflow       
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path=params["mlflow"]["model_name"],
            #registered_model_name=params["mlflow"]["model_name"],
            conda_env=str(Path(os.getcwd()).joinpath(params['mlflow']['conda_env']))
        )        

    logger.info("\n(node:train.training): done ==================================\n")

    return model
