import boto3
import json

def lambda_handler(event, context):
    print("Event recibido:", json.dumps(event))
    
    # ✅ CORREGIDO para Lambda Proxy Integration
    # En Proxy Integration, event['body'] ya es un string JSON
    if isinstance(event.get('body'), dict):
        body = event['body']
    else:
        # Si viene como string, hacer parsing
        body = json.loads(event.get('body', '{}'))
    
    tenant_id = body.get('tenant_id')
    alumno_id = body.get('alumno_id')
    alumno_datos = body.get('alumno_datos')
    
    # Validar parámetros requeridos
    if not tenant_id or not alumno_id or not alumno_datos:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'tenant_id, alumno_id y alumno_datos son requeridos'})
        }
    
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    alumno = {
        'tenant_id': tenant_id,
        'alumno_id': alumno_id,
        'alumno_datos': alumno_datos
    }
    
    try:
        response = table.put_item(Item=alumno)
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'mensaje': 'Alumno creado exitosamente',
                'alumno': alumno
            })
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