from fastapi import FastAPI
from fastapi.requests import Request
import json
import pika

credentials = pika.PlainCredentials(username='admin', password='strongpassword')

app = FastAPI()

@app.get('/test')
def test():
    return { 'message': 'Succeed' }

@app.post('/mula-imbasan')
async def mula_imbasan(request: Request):
    body = await request.json()
    tugasan_id = body['tugasan_id']

    with open('scanned_data.json', 'r') as cbom:
        cbom_data = json.load(cbom)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='178.128.116.198',
            port=5672,
            credentials=credentials
        )
    )

    channel = connection.channel()

    channel.queue_declare(queue='tugasan_queue')

    data = {
        'tugasan_id': tugasan_id,
        'cbom_data': cbom_data
    }

    channel.basic_publish(
        exchange='',
        routing_key='tugasan_queue',
        body=json.dumps(data)
    )

    connection.close()
    
    return {
        'message': 'Imbasan bermula'
    }