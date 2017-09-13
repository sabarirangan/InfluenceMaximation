import pika
import psycopg2
import time
import tweepy

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='sabarirangan1996',durable=True)

conn = psycopg2.connect("dbname='twitterdb' user='postgres' host='localhost' password='zxasqw12'")
cur=conn.cursor()

consumer_key = 'xxxxxxxxx'
consumer_secret = 'xxxxxxxxxxx'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

access_token = 'xxxxxxxxxO'
access_token_secret = 'xxxxxxxxxxxxxxxx'
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='sabarirangan1996',durable=True)

channel.basic_qos(prefetch_count=1)




def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            print('sleep start')
            time.sleep(15 * 60)
            print('sleep complete')
            global connection, channel
            # connection.close()
            try:
                connection = pika.BlockingConnection(pika.ConnectionParameters(
                    host='localhost'))
                channel = connection.channel()

                channel.queue_declare(queue='sabarirangan1996', durable=True)
                channel.basic_qos(prefetch_count=1)

                channel.basic_consume(callback,
                                      queue='sabarirangan1996',
                                      no_ack=True)

                print(' [*] Waiting for messages. To exit press CTRL+C')
                channel.start_consuming()
            except Exception as e:
                print(e)

def callback(ch, method, properties, body):
    sql = '''SELECT * FROM followers WHERE user_id=%s'''
    body=body.decode("utf-8")
    print(body)
    params = (body,)
    cur.execute(sql, params)
    records = cur.fetchall()
    if len(records) == 0:
        for followers in limit_handled(tweepy.Cursor(api.followers_ids, id=body).items()):
            sql = '''INSERT INTO followers (user_id, follower_user_id) VALUES (%s,%s)'''
            params = (body, followers)
            cur.execute(sql, params)
        conn.commit()
    ch.basic_ack(delivery_tag=method.delivery_tag)
try:
    channel.basic_consume(callback,
                          queue='sabarirangan1996',
                          no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
except Exception as e:
    print(e)
