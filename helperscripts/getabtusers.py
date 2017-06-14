import time
import tweepy
import psycopg2
import json


consumer_key = 'Fs61elRfHr00yM1dYf9ZQQWC6'
consumer_secret = 'lzZGfGdzDVLkOZL3ayNAEpQKjVaEgiucY4Ud88CMZ7KQvKJ19Z'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

access_token = '2986939003-C49fviOIzjTBp4cnLIMCatJuWQhyV2009NZG1PO'
access_token_secret = 'tVdgH1TDeO0iGnqN10fnf2H6Ew2eqQcL0bIhwyMUAu2L2'
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

conn = psycopg2.connect("dbname='twitterdb1' user='postgres' host='localhost' password='zxasqw12'")
cur=conn.cursor()
ret=None


sql='''SELECT user_id FROM followers'''
cur.execute(sql)
records = cur.fetchall()
count=0
for uid in records:
    flag=0
    uid=uid[0]
    print(uid)
    while True:
        print(count)
        try:
            ret = api.get_user(uid)
            count+=1
            break;
        except tweepy.RateLimitError:
            print('sleep start')
            time.sleep(15 * 60)
            print('sleep complete')
        except tweepy.TweepError:
            flag=1
            break;
    if flag==1:
        continue
    sql = '''UPDATE followers SET following_count = %s,tweets_count=%s WHERE user_id = %s;'''
    params = (ret._json['friends_count'],ret._json['statuses_count'],uid)
    cur.execute(sql, params)
    conn.commit()


