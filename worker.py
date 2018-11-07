import os
import redis
from rq import Worker, Queue, Connection
from config import load_dotenv

conn = redis.from_url(os.environ['REDIS_URL'])
listen = ['default']

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
