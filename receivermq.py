import pika
import json


def callback(ch, method, properties, body):
    data = json.loads(body)
    landmarks = data
    print(landmarks)  # Replace this with your own processing code


cred = pika.PlainCredentials('anish', 'dotmail123')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='172.19.0.1', port=5672, virtual_host='/', credentials=cred))
channel = connection.channel()

channel.queue_declare(queue='hand_gesture_data')

channel.basic_consume(queue='hand_gesture_data',
                      on_message_callback=callback, auto_ack=True)

print('Waiting for hand gesture data. To exit press CTRL+C')
channel.start_consuming()
