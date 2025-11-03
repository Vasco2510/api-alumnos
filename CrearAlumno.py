import boto3
import json

def lambda_handler(event, context):
    print("Event recibido:", json.dumps(event))
    
    # Obtener parámetros del body (CORREGIDO para Serverless)
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
    response = table.put_item(Item=alumno)
    
    # Salida (json)
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