import boto3
import json

def lambda_handler(event, context):
    print("Event recibido:", json.dumps(event))
    
    # Obtener parámetros del body
    body = json.loads(event.get('body', '{}'))
    tenant_id = body.get('tenant_id')
    alumno_id = body.get('alumno_id')
    
    # Validar parámetros requeridos
    if not tenant_id or not alumno_id:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'tenant_id y alumno_id son requeridos'})
        }
    
    # Buscar en DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    
    try:
        response = table.get_item(
            Key={
                'tenant_id': tenant_id,
                'alumno_id': alumno_id
            }
        )
        
        # Verificar si se encontró el alumno
        if 'Item' in response:
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(response['Item'])
            }
        else:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Alumno no encontrado'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }