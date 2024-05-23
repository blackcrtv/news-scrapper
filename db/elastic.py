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
            data['@timestamp'] = int(datetime.now().timestamp() * 1000)
            bulk_data.append({"index": {"_index": self.index_name, "_id": _id}})
            bulk_data.append({key: value for key, value in data.items()})
        
        return self.es.bulk(body=bulk_data)

    def select_data(self,index: str = "index_news", query: Dict = None, size: int = 1) -> List[Dict[str, str]]:
        if query is None:
            query = {
                "query": {
                    "match_all": {}
                }
            }
        response = self.es.search(index=index, body=query, size=size)
        hits = response['hits']['hits']
        return [hit['_source'] for hit in hits]