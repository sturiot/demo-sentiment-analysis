from kedro.pipeline import Pipeline, node
from demo_sentiment_analysis.nodes.prediction import load_model, predict_to_pandas_dataframe
from demo_sentiment_analysis.nodes.load_prep.load import load_json_data_as_pandas_df
from demo_sentiment_analysis.nodes.load_prep.load_prep import preprocess_data, format_data_to_score

def create_prediction_api_pipeline(**kwargs):

    return Pipeline(
        [
            node(
                func=load_model,
                inputs='model', 
                outputs='model_loaded',
                name="predict_api_load_model_from_mlflow_server",
            ),
            node(
                func=load_json_data_as_pandas_df,
                inputs="data",
                outputs="data_pd",
                name="predict_api_load_data_as_pandas_dataframe",
            ),
            node(
                func=preprocess_data,
                inputs="data_pd",
                outputs="prep_data_pd",
                name="predict_api_preprocessing_data_for_scoring",
            ),
            node(
                func=format_data_to_score,
                inputs="prep_data_pd",
                outputs="data_formatted",
                name="predict_api_formatting_data_for_scoring",
            ),
            node(
                func=predict_to_pandas_dataframe,
                inputs=["data_formatted", "model"],
                outputs="data_scored",
                name="predict_api_create_prediction_for_production_data",
            ),            

        ],
        tags="prediction_pipeline_api"
    )

