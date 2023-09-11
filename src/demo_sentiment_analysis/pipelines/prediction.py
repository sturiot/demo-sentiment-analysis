from kedro.pipeline import Pipeline, node
from demo_sentiment_analysis.nodes.prediction import get_model, predict_to_spark_dataframe
from demo_sentiment_analysis.nodes.load_prep.load import load_data_as_pandas_df
from demo_sentiment_analysis.nodes.load_prep.load_prep import preprocess_data, format_data_to_score

def create_prediction_pipeline(**kwargs):

    return Pipeline(
        [
            node(
                func=get_model,
                inputs="params:predict",
                outputs="model",
                name="predict_load_model_from_mlflow_server",
            ),
            node(
                func=load_data_as_pandas_df,
                inputs="data_to_score",
                outputs="data_to_score_pd",
                name="predict_load_data_as_pandas_dataframe",
            ),
            node(
                func=preprocess_data,
                inputs="data_to_score_pd",
                outputs="prep_data_to_score",
                name="predict_preprocessing_data_for_scoring",
            ),
            node(
                func=format_data_to_score,
                inputs="prep_data_to_score",
                outputs="data_to_score_formatted",
                name="predict_formatting_data_for_scoring",
            ),
            node(
                func=predict_to_spark_dataframe,
                inputs=["data_to_score_formatted", "model"],
                outputs="data_scored",
                name="predict_create_prediction_for_production_data",
            ),
        ],
        tags="prediction_pipeline"
    )

