from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient
from elasticsearch import AsyncElasticsearch
from aiohttp_prometheus import metrics_middleware, MetricsView
import logging

logger = logging.getLogger(__name__)


async def index(request):
    
    # Connect to MongoDB
    logger.info("in get")
    mongo_client = AsyncIOMotorClient('mongodb://root:example@mongodb:27017')
    db = mongo_client['mydatabase']
    collection = db['mycollection']

    logger.info("in get 2")
    # Insert a document
    doc = {'name': 'John', 'age': 25}
    await collection.insert_one(doc)
    logger.info("in get 3")
    # Connect to Elasticsearch
    es = AsyncElasticsearch(
        [{'host': 'elasticsearch', 'port': 9200, "scheme": "http"}], 
    )
    # check if the index already exists
    index_name = 'myindex'
    if not await es.indices.exists(index=index_name):
        # define the mapping for the index
        mapping = {
            "mappings": {
                "properties": {
                    "name": {"type": "text"},
                    "age": {"type": "text"}
                }
            }
        }
        # create the index with the specified mapping
        await es.indices.create(index=index_name, body=mapping)
    logger.info("in get 4")
    # Search for documents
    query = {'query': {'match': {'name': 'John'}}}
    result = await es.search(index='myindex', body=query)

    response = web.Response(text=str(result))

    return response

app = web.Application()
app.middlewares.append(metrics_middleware)
app.add_routes([web.get('/', index), web.get('/metrics', MetricsView)])

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8080)