# import pika
# import psycopg2
# import time
# import tweepy
#
# connection = pika.BlockingConnection(pika.ConnectionParameters(
#         host='localhost'))
# channel = connection.channel()
#
# channel.queue_declare(queue='sabarirangan1996',durable=True)
#
# conn = psycopg2.connect("dbname='twitterdb' user='postgres' host='localhost' password='zxasqw12'")
# cur=conn.cursor()
#
# consumer_key = 'lYvRP6UfNbVuFhIPjqKp4ls1a'
# consumer_secret = 'fhpbADrqSkHZweGSQQ6XrcoddYe0dpHQnT0lmZqSTvFk7gbY63'
#
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#
# access_token = '92757725-gqkFLxJo2t1elxkI5dXTcc0MWddtWAuScYb0qig8G'
# access_token_secret = '6trocZx4RvuO3XL9fG5ldPa18wWTBzaweKZSXnYuVOiH2'
# auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth)
#
# connection = pika.BlockingConnection(pika.ConnectionParameters(
#         host='localhost'))
# channel = connection.channel()
#
# channel.queue_declare(queue='sabarirangan1996',durable=True)
#
# channel.basic_qos(prefetch_count=1)
#
#
#
#
# def limit_handled(cursor):
#     while True:
#         try:
#             yield cursor.next()
#         except tweepy.RateLimitError:
#             print('sleep start')
#             time.sleep(15 * 60)
#             print('sleep complete')
#             global connection, channel
#             # connection.close()
#             try:
#                 connection = pika.BlockingConnection(pika.ConnectionParameters(
#                     host='localhost'))
#                 channel = connection.channel()
#
#                 channel.queue_declare(queue='sabarirangan1996', durable=True)
#                 channel.basic_qos(prefetch_count=1)
#
#                 channel.basic_consume(callback,
#                                       queue='sabarirangan1996',
#                                       no_ack=True)
#
#                 print(' [*] Waiting for messages. To exit press CTRL+C')
#                 channel.start_consuming()
#             except Exception as e:
#                 print(e)
#
# def callback(ch, method, properties, body):
#     sql = '''SELECT * FROM followers WHERE user_id=%s'''
#     body=body.decode("utf-8")
#     params = (body,)
#     cur.execute(sql, params)
#     records = cur.fetchall()
#     if len(records) == 0:
#
#     ch.basic_ack(delivery_tag=method.delivery_tag)
# try:
#     channel.basic_consume(callback,
#                           queue='sabarirangan1996',
#                           no_ack=True)
#
#     print(' [*] Waiting for messages. To exit press CTRL+C')
#     channel.start_consuming()
# except Exception as e:
#     print(e)
