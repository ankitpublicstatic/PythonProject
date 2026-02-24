from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
import os
import json

app = FastAPI()
db = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION', 'us-east-1'))
TABLE = os.getenv('TABLE_NAME', 'items')


def table():
    return db.Table(TABLE)


class Item(BaseModel):
    id: str
    name: str


@app.post('/items')
async def create_item(item: Item):
    t = table()
    t.put_item(Item=item.model_dump())
    # t.put_item(Item=item.dict())

    return {'status': 'ok', 'item': item}


@app.get('/items/{item_id}')
async def get_item(item_id: str):
    r = table().get_item(Key={'id': item_id})
    if 'Item' not in r:
        raise HTTPException(status_code=404, detail='Not found')
    return r['Item']

@app.put('/items/{item_id}')
async def update_item(item_id: str, item: Item):
    t = table()
    t.put_item(Item=item.model_dump())
    return {'status': 'ok', 'item': item}

@app.delete('/items/{item_id}')
async def delete_item(item_id: str):
    t = table()
    t.delete_item(Key={'id': item_id})
    return {'status': 'ok'}

@app.get('/items')
async def read_items(skip: int = 0, limit: int = 100):
    t = table()
    items = t.scan()
    items = items[skip:skip+limit]
    return {'items': items}

"""
Deployment options:

Containerize with Docker and run on ECS/Fargate, EKS, or App Service.

For serverless, wrap the FastAPI app with AWS Lambda + API Gateway using AWS Lambda Function URLs or AWS Lambda POWertools + container image.

Use ALB + EC2/ECS for blue/green.

"""

def get_secret(name, region='us-east-1'):
    client = boto3.client('secretsmanager', region_name=region)
    resp = client.get_secret_value(SecretId=name)
    if 'SecretString' in resp:
        return json.loads(resp['SecretString'])
    else:
        # binary secrets
        import base64
        return json.loads(base64.b64decode(resp['SecretBinary']))