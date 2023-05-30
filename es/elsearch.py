from elasticsearch import Elasticsearch
#import asyncio


class ElasticsearchClient_SSLConnction(object):
    def __init__(self):
        url = "https://elasticsearch-124023-0.cloudclusters.net"
        port = 10105
        conn = Elasticsearch(
            ['{}:{}'.format(url, port)],
            verify_certs=True,
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

    def insert_get_doc(self, elk_data):
        query_body = {
            "query": {
                "match": {
                    "definition": elk_data['definition']
                }
            }
        }
        try:
            #asyncio.create_task(self.conn.index(index="products", body=elk_data))
            #data = await self.conn.search(index="products", body={"query": query_body['query']})
            self.conn.index(index="products", body=elk_data)
            data = self.conn.search(index="products", body={"query": query_body['query']})
            return {
                "data": data,
                "success": True
            }
        except:
            return {
                "success": False,
                "message": "elastic operation error"
            }
