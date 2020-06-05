import json
import logging
import traceback

from kafka import KafkaConsumer
import os


log = logging.getLogger('file')
cluster_details = os.environ.get('KAFKA_CLUSTER_DETAILS', 'localhost:9092')
consumer_poll_interval = os.environ.get('CONSUMER_POLL_INTERVAL', 10)
anu_etl_wfm_topic = "anu-etl-wfm"
#anu_etl_wfm_topic = os.environ.get('ANU_ETL_WF_TOPIC', 'laser-align-job-register')
anu_etl_wfm_consumer_grp = os.environ.get('ANU_ETL_WF_CONSUMER_GRP', 'anu-etl-wfm-consumer-group')

# Method to instantiate the kafka consumer
def instantiate():
    consumer = KafkaConsumer(anu_etl_wfm_topic,
                             bootstrap_servers=[cluster_details],
                             api_version=(1, 0, 0),
                             group_id=anu_etl_wfm_consumer_grp,
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             max_poll_records=1,
                             value_deserializer=lambda x: handle_json(x))
    consumer.poll(consumer_poll_interval)
    return consumer

# Method to read and process the requests from the kafka queue
def consume():
    consumer = instantiate()
    log.info("Consumer running.......")
    try:
        data = {}
        for msg in consumer:
            log.info("Consuming from the Kafka Queue......")
            data = msg.value
            break
    except Exception as e:
        log.error("Exception while consuming: " + str(e))
        traceback.print_exc()
    finally:
        consumer.close()

# Method that provides a deserialiser for the kafka record.
def handle_json(x):
    try:
        return json.loads(x.decode('utf-8'))
    except Exception as e:
        log.error("Exception while deserialising: " + str(e))
        traceback.print_exc()
        return {}