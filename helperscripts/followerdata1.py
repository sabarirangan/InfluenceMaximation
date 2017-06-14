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


sql='''SELECT user_id FROM followers WHERE id>1000 AND id<=2000'''
cur.execute(sql)
records = cur.fetchall()
V=[]
for i in records:
    V.append(i[0])
count=0
for uid in V:
    print(uid)
    while True:
        print(count)
        try:
            ret = api.followers_ids(uid)
            count+=1
            break;
        except tweepy.RateLimitError:
            print('sleep start')
            time.sleep(15 * 60)
            print('sleep complete')
        except tweepy.TweepError:
            api = tweepy.API(auth)
    for i in list(set(ret) & set(V)):
        sql = '''INSERT INTO userfollower (user_id, follower_id) VALUES (%s,%s);'''
        params = (i,uid)
        cur.execute(sql, params)
        conn.commit()



