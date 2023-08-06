import socket
import json

from confluent_kafka import Producer


def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))


def send_messages(producer, data):
    if 'topics' in data and len(data['topics']) > 0 :
        all_topic = data['topics']
        available_topics = list(producer.list_topics().topics)
        for topic in all_topic:
            if topic in available_topics:
                print(f'sending message topic : {topic}, data :{data}')
                byte_data = json.dumps(data).encode('utf-8')
                producer.produce(topic, value=byte_data, callback=acked)
            else :
                pass # write log


def create_producer(broker):
    conf = {
        'bootstrap.servers': broker,
        'client.id': socket.gethostname()
        }

    producer = Producer(conf)
    return producer


def topic_add_or_create(result, topics):
    if result.get('topics', None) in [ None, [], 'None' ] :
        result['topics'] = topics
    else :
        result['topics'] += topics
    
    return result