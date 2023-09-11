import sys
from demo_sentiment_analysis.api_serving.wrapper import DemoSentimentAnalysis
import logging

PAYLOAD = None

if len(sys.argv) > 1:
    PAYLOAD = sys.argv[1]

logging.getLogger().info('[Run API Pipeline]')
api_pipeline = DemoSentimentAnalysis()
api_pipeline.predict(X = PAYLOAD)
logging.getLogger().info('[End API Pipeline]')

