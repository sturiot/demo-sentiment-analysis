import pandas as pd
import numpy as np
import logging.config
from sklearn import metrics

logger = logging.getLogger(__name__)

def calculate_metrics(true_labels: pd.core.series.Series, predicted_labels: np.ndarray):
    # TP / SUM(Y)
    accuracy = np.round(metrics.accuracy_score(true_labels, predicted_labels), 4)
    # TP / (TP + FP)
    precision = np.round(metrics.precision_score(true_labels, predicted_labels, average='weighted'), 4)
    # TP / (TP + FN)
    recall = np.round(metrics.recall_score(true_labels, predicted_labels, average='weighted'), 4)
    # 2 * (preicision * recall) / (precision + recall)
    F1_score = np.round(metrics.f1_score(true_labels, predicted_labels, average='weighted'), 4)

    return accuracy, precision, recall, F1_score

def confusion_matrix_as_pandas(true_labels: pd.core.series.Series, predicted_labels: pd.core.series.Series, classes=[1, 0]):
    total_classes = len(classes)
    level_labels = [total_classes] * [0], list(range(total_classes))

    cm = metrics.confusion_matrix(y_true=true_labels, y_pred=predicted_labels, labels=classes)
    
    return pd.DataFrame(
        data=cm,
        columns=pd.MultiIndex(levels=[['Predicted:'], classes], codes=level_labels),
        index=pd.MultiIndex(levels=[['Actual:'], classes], codes=level_labels)
    )

def confusion_matrix_as_figure(true_labels: pd.core.series.Series, predicted_labels: pd.core.series.Series, classes=[1, 0]):

    cm = metrics.confusion_matrix(y_true=true_labels, y_pred=predicted_labels, labels=classes)
    
    return metrics.ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=classes)

def classification_metrix (true_labels, predicted_labels, classes=[1, 0]):
    return metrics.classification_report(y_true=true_labels, y_pred=predicted_labels, labels=classes)

def print_performance_metrics(true_labels, predicted_labels, classes=[1, 0]):
    logger.info('Model performance metrics:')
    logger.info('-' * 30)
    accuracy, precision, recall, F1_score = calculate_metrics(true_labels=true_labels, predicted_labels=predicted_labels)

    logger.info('Accuracy: ', accuracy)
    logger.info('Precision: ', precision)
    logger.info('Recall: ', recall)
    logger.info('F1 Score: ', F1_score)

    logger.info('\nPrediction Confusion Matrix:')
    logger.info('-' * 30)
    cm_frame = confusion_matrix_as_pandas(true_labels=true_labels, predicted_labels=predicted_labels, classes=classes)
    logger.info(cm_frame)

    logger.info('\Model Classification report:')
    logger.info('-' * 30)
    report = classification_metrix(true_labels=true_labels, predicted_labels=predicted_labels, classes=classes)
    logger.info(report)
