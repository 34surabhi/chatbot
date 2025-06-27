from google.cloud import bigquery
import pandas as pd
import os

# Set your credentials if not set in terminal
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.expanduser("~/Downloads/avid-relic-463708-h6-4524d09725d8.json")

def get_training_data():
    client = bigquery.Client()

    query = """
        SELECT *
        FROM `avid-relic-463708-h6.chatbot_data.it_support_tickets`

    """

    df = client.query(query).to_dataframe()
    return df
