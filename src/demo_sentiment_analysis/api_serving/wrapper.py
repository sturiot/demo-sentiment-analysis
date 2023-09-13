import logging
import json, os
from kedro.framework.project import configure_project
from kedro.framework.session import KedroSession
from typing import Any, Dict

logger = logging.getLogger(__name__)


class DemoSentimentAnalysis(object):
    """
    Model template. You can load your model parameters in __init__ from a location accessible at runtime
    """

    def __init__(self):
        """
        Add any initialization parameters. These will be passed at runtime from the graph definition parameters defined in your seldondeployment kubernetes resource manifest.
        """
        logger.info("Initializing")
        self.project_name = 'demo_sentiment_analysis'
        self.pipeline_name = 'predict_api'
        self.env = 'seldon'
        configure_project(self.project_name)
        self._load_model()
        logger.info("Initialized")

    def _load_model(self):
        with KedroSession.create(env=self.env) as session:
            self._model = session.run(pipeline_name=self.pipeline_name, node_names=['predict_api_load_model_from_mlflow_server']) 

    @property
    def project_name(self):
        return self._project_name

    @project_name.setter
    def project_name(self, value):
        self._project_name = value       

    @property
    def pipeline_name(self):
        return self._pipeline_name

    @pipeline_name.setter
    def pipeline_name(self, value):
        self._pipeline_name = value 

    @property
    def env(self):
        return self._env

    @env.setter
    def env(self, value):
        self._env = value 

    def predict(self, X, features_names=None):
        """
        Return a prediction.

        Parameters
        ----------
        X : array-like
        feature_names : array of feature names (optional)
        """
        logger.info("Predict called.")
        logger.info(X)
        
        X = eval(X) if type(X) is str else X.tolist()

        data_uri = 'data/01_raw/api/data.json'

        with open(data_uri, 'w') as f:
            json.dump(X, f)
                    
        with KedroSession.create(env=self.env) as session:
            outputs = session.run(pipeline_name=self.pipeline_name, from_nodes=['predict_api_load_data_as_pandas_dataframe'], to_nodes=['predict_api_create_prediction_for_production_data'])
            return outputs["data_outputs"]
