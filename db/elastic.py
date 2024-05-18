from elasticsearch import Elasticsearch
from datetime import datetime
from typing import List, Dict
import configparser

class ElasticSearch:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.host = self.config['elasticsearch']['host']
        self.port = self.config['elasticsearch']['port']
        self.user = self.config['elasticsearch']['user']
        self.password = self.config['elasticsearch']['password']
        self.index_name = self.config['elasticsearch']['index']    

        self.es = Elasticsearch(self.host)

    def insert_data(self, data: Dict[str, str]):
        _id = self.generate_id(data['link'])
        self.es.index(index=self.index_name, body=data, id=_id)

    def insert_multiple_data(self, data_list: List[Dict[str, str]]):
        bulk_data = []
        for data in data_list:
            _id = data['link']
            data['@timestamp'] = datetime.now().isoformat()
            bulk_data.append({"index": {"_index": self.index_name, "_id": _id}})
            bulk_data.append({
                "link": data['link'],
                "text": data['text'], 
                "site": data['site'],
                "@timestamp": data['@timestamp'],
            })
        self.es.bulk(body=bulk_data)