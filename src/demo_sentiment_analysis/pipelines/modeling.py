from kedro.pipeline import Pipeline, node
from demo_sentiment_analysis.nodes.load_prep.load import load_data_as_pandas_df
from demo_sentiment_analysis.nodes.load_prep.load_prep import preprocess_data
from demo_sentiment_analysis.nodes.feat_engin import train_bag_of_words, apply_bag_of_words
from demo_sentiment_analysis.nodes.modeling.train import training, split_data, dummy_function

def create_modeling_pipeline(**kwargs):

    return Pipeline(
        [
            node(
                func=load_data_as_pandas_df,
                inputs="data",
                outputs="data_pd",
            ),
            node(
                func=dummy_function,
                inputs="data_pd",
                outputs="data_pd_after_dummy",
            ),
            node(
                func=preprocess_data,
                inputs="data_pd_after_dummy",
                outputs="prep_data",
            ),
            node(
                func=split_data,
                inputs=["prep_data", "params:train"],
                outputs=["X_train", "X_test", "y_train", "y_test"],
                name="train_test_split",
            ),
            node(
                func=train_bag_of_words,
                inputs=["X_train", "params:train"],
                outputs=["X_feat_train", "model"],
                name="feature_engineering_train",
            ),
            node(
                func=apply_bag_of_words,
                inputs=["X_test", "model"],
                outputs="X_feat_test",
                name="feature_engineering_test",
            ),
            node(
                func=training,
                inputs=["X_feat_train", "X_feat_test", "y_train", "y_test", "model", "params:train"],
                outputs="training_model",
                name="training",
            ), 
        ]
    )

