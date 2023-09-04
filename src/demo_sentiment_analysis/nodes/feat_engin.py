import logging.config
from sklearn.feature_extraction.text import TfidfVectorizer # CountVectorizer
from sklearn.pipeline import Pipeline

logger = logging.getLogger(__name__)


def train_bag_of_words(X_train: list, params):
    logger.info("\n(node:feat_engin.build_bag_of_words): Building B.O.W ==================================\n")
    min_df = params["vectorizer"]["min_df"]
    max_df = params["vectorizer"]["max_df"]
    bow_model = TfidfVectorizer(min_df=min_df, max_df=max_df, ngram_range=(1, 2))
    #bow_model = CountVectorizer(min_df=min_df, max_df=max_df, ngram_range=(1, 2))
    X_feat_train = bow_model.fit_transform(X_train)
    model_pipe = Pipeline([("bow_model", bow_model)])

    return X_feat_train, model_pipe

def apply_bag_of_words(X_test: list, model):
    logger.info("\n(node:feat_engin.build_bag_of_words): Apply B.O.W ==================================\n")
    return model["bow_model"].transform(X_test)

