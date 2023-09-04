"""Project pipelines."""
from typing import Dict

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline
from demo_sentiment_analysis.pipelines.modeling import create_modeling_pipeline
from demo_sentiment_analysis.pipelines.prediction import create_prediction_pipeline



def register_pipelines() -> Dict[str, Pipeline]:
    modeling_pipeline = create_modeling_pipeline()
    prediction_pipeline = create_prediction_pipeline()

    return {
        "train": modeling_pipeline,
        "predict": prediction_pipeline,
        "__default__": modeling_pipeline,
    }
