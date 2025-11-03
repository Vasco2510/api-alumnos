import boto3
import json
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    print("Event recibido:", json.dumps(event))
    
    # Obtener tenant_id del body
    body = json.loads(event.get('body', '{}'))
    tenant_id = body.get('tenant_id')
    
    if not tenant_id:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json', 
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'tenant_id es requerido'})
        }
    
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    response = table.query(
        KeyConditionExpression=Key('tenant_id').eq(tenant_id)
    )
    items = response['Items']
    num_reg = response['Count']
    
    # Salida (json)
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'tenant_id': tenant_id,
            'num_reg': num_reg,
            'alumnos': items
        })
    }