# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 10:46:51 2023

@author: Friedrich.Schmidt
"""

import asyncio
from datetime import datetime
from funke_enrichment_core.helper import save_dict_to_bq, publish_data_to_pubsub_topic
from google.cloud import bigquery


class InitPayload():
    """
    dummy class to get init input data
    """
    def __init__(self, payload):
        self.payload = payload

    async def process(self, inp_data):
        return self.payload


class WriteToBigQuery():
    """
    Class to write to BQ
    """
    def __init__(self, table_path, table_schema, write_disposition):
        self.table = table_path
        self.job_config = bigquery.LoadJobConfig(schema=table_schema, write_disposition=write_disposition)

    async def process(self, inp_data):
        job_future = save_dict_to_bq(inp_data, self.table, self.job_config)
        await asyncio.sleep(0.1)
        for _ in range(600):
            if job_future.done():
                return {self.table: True}
            else:
                await asyncio.sleep(0.5)
                
        job_future.cancel()
        raise TimeoutError('Failed finishing write to BigQuery job within 5 minutes')
        
        

class PublishOnPubSubTopic():
    """
    Class to publish to a pubsub topic
    """
    def __init__(self, topic_path):
        self.topic_path = topic_path


    def _make_dict_json_serializable(self, json_dict):
        for key, value in json_dict.items():
            if isinstance(value, datetime):
                json_dict[key] = value.strftime("%Y-%m-%dT%H:%M:%S")
            elif isinstance(value, dict):
                json_dict[key] = self._make_dict_json_serializable(value)
            else:
                json_dict[key] = value

        return json_dict

    async def process(self, inp_data):
        pubsub_dict = self._make_dict_json_serializable(inp_data)
        job_future = publish_data_to_pubsub_topic(self.topic_path, pubsub_dict)
        await asyncio.sleep(0.1)
        for _ in range(600):
            if job_future.done():
                return {self.topic_path: True}
            else:
                await asyncio.sleep(0.5)
                
        job_future.cancel()
        raise TimeoutError('Failed finishing to publish to Pub/Sub topic within 5 minutes')