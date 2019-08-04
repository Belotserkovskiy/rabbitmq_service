import pika
import json
import saver
import time

class RabbitmqService:
    def __init__(self, connection, db_connection):
        self.__host = connection['host']
        self.__vhost = connection['vhost']
        self.__port = connection['port']
        self.__exchange = connection['exchange']
        self.__queue = connection['queue']
        self.__user = connection['user']
        self.__password = connection['password']
        self.__db_saver = saver.DatabaseSaver(db_connection)
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(
                                                  host=self.__host, virtual_host=self.__vhost,
                                                  port=self.__port, credentials=pika.PlainCredentials(self.__user,
                                                                                                      self.__password)))

    def __del__(self):
        self.__connection.close()

    def run(self):   
        self.__channel = self.__connection.channel()
        self.__channel.basic_consume(queue=self.__queue, on_message_callback=self.__callback, auto_ack=True)
        self.__channel.start_consuming()

    def __callback(self, ch, method, properties, body):
        d = json.loads(body.decode('utf-8').replace('\'', '\"'))

        exchange_point = d['reply_to']['exchange']
        queue = d['reply_to']['queue']
        del d['reply_to']

        result = {"error_msg": ""}
        try:
            result["id"] = self.__db_saver.push_to_database(d)
            result["error_code"] = 0
        except Exception as e:
            result["id"] = None
            result["error_code"] = 1
            result["error_msg"] = str(e)

        print(result)
        self.__channel.basic_publish(exchange=exchange_point,
                              routing_key=queue,
                              body=json.dumps(result))


def try_start_service():
    while True:
        print("try")
        try:
            f = open("cfg/rabbitmq.cfg")
            rabbitmq_connection = json.load(f)
            f.close()

            f = open("cfg/postgresql.cfg")
            postgresql_connection = json.load(f)
            f.close()

            service = RabbitmqService(rabbitmq_connection, postgresql_connection)
            service.run()
        except pika.exceptions.AMQPConnectionError:
            print("Something went wrong with RabbitMq connection, retrying...")
        except Exception as e:
            print(e)
        print("Retrying...")
        time.sleep(5)


try_start_service()
