import logging.config
import pandas as pd

from typing import Dict

logger = logging.getLogger(__name__)

def drop_missing_data(data=pd.DataFrame):
    return data.dropna()

def preprocess_data(data=pd.DataFrame):
    prepro_train_df = drop_missing_data(data)
    return prepro_train_df


def format_data_to_score(data: pd.DataFrame):
    try:
        return data['review'].tolist()
    except BaseException:
        logger.error('The dataset to score is either not a pandas Dataframe or does not contain "review" column')

