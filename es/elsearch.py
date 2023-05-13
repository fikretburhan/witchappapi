import datetime
from elasticsearch import Elasticsearch
import pem
from datetime import datetime, date


class ElasticsearchClient_SSLConnction(object):
    def __init__(self):
        url = "https://elasticsearch-124023-0.cloudclusters.net"
        port = 10105
        ca_cert = pem.parse_file("es/ca_certificate.pem")
        conn = Elasticsearch(
            ['{}:{}'.format(url, port)],
            verify_certs=True,
            #     # provide a path to CA certs on local
            ca_certs='es/ca_certificate.pem',
            http_auth=("elastic", "dJhwA7pE")
        )
        self.conn = conn

    def create_index(self):
        mappings = {
            "mappings": {
                "properties": {
                    "definition": {"type": "text"},
                    "price": {"type": "double"},
                    "createdate": {"type": "date"}
                }
            }
        }

        return self.conn.indices.create(index='products', body=mappings)

    def insert_doc(self, elkdata):
        res = self.conn.index(index="products", body=elkdata)
        if res['result'] == 'created':
            return {
                'success': True,
                'term': elkdata['definition']
            }
        else:
            return {
                'success': False
            }
