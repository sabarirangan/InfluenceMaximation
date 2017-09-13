import time
import tweepy
import psycopg2
import json


consumer_key = 'xxxxxxx'
consumer_secret = 'xxxxxxx'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

access_token = '134097445-kIuwstknl5Q1PfP76XlHSEREnBbdJPgBUL0GTki4'
access_token_secret = 'OU6uJc1gLiie5dyaX7w1dzHORaUeQ2wurghfH4CpoPerp'
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

conn = psycopg2.connect("dbname='twitterdb1' user='postgres' host='localhost' password='zxasqw12'")
cur=conn.cursor()
ret=None


sql='''SELECT user_id FROM followers'''
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



