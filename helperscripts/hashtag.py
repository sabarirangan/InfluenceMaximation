import time
import tweepy
import psycopg2
import json



consumer_key = 'lYvRP6UfNbVuFhIPjqKp4ls1a'
consumer_secret = 'fhpbADrqSkHZweGSQQ6XrcoddYe0dpHQnT0lmZqSTvFk7gbY63'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
access_token = '92757725-gqkFLxJo2t1elxkI5dXTcc0MWddtWAuScYb0qig8G'
access_token_secret = '6trocZx4RvuO3XL9fG5ldPa18wWTBzaweKZSXnYuVOiH2'
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)







conn = psycopg2.connect("dbname='twitterdb1' user='postgres' host='localhost' password='zxasqw12'")
cur=conn.cursor()

ret=None
def limit_handled(cursor):
    global api
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            print('sleep start')
            time.sleep(15 * 60)
            print('sleep complete')
        except tweepy.TweepError as e:
            print(e)


query=['mobilephone','mobile phone','mobilephones','smartphone','smart phones','androidphone','android phones','ios','windows phone']
def insert_entries(temp,q):
    sql='''SELECT * FROM tweets WHERE tweet_id=%s'''
    params=(temp['id'],)
    cur.execute(sql, params)
    records = cur.fetchall()
    if len(records)==0:
        sql = '''INSERT INTO tweets (user_id, tweet_id,created_at,query) VALUES (%s,%s,%s,%s)'''
        params = (temp['user']['id'],temp['id'],temp['created_at'],q)
        cur.execute(sql, params)
        conn.commit()
        sql = '''SELECT * FROM followers WHERE user_id=%s'''
        params = (temp['user']['id'],)
        cur.execute(sql, params)
        records = cur.fetchall()
        if len(records)==0:
            insert_follower(temp['user']['id'],temp['user']['followers_count'])
        insert_mentions(temp['user']['id'], temp['entities']['user_mentions'], temp['id'])


def insert_follower(user_id,count):
    sql = '''INSERT INTO followers (user_id, follower_count) VALUES (%s,%s)'''
    params = (user_id, count)
    cur.execute(sql, params)
    conn.commit()

def insert_retweet(user_id,parent_user_id,tweet_id,parent_tweet_id):
    sql='''INSERT INTO retweet (user_id, parent_user_id,tweet_id,parent_tweet_id) VALUES (%s,%s,%s,%s)'''
    params=(user_id,parent_user_id,tweet_id,parent_tweet_id)
    cur.execute(sql,params)
    conn.commit()


def insert_mentions(user_id,user_mentions,tweet_id):
    for user in user_mentions:
        params = (user_id, user['id'],tweet_id)
        sql = '''INSERT INTO mentions (user_id,metioned_user_id,tweet_id) VALUES (%s,%s,%s)'''
        cur.execute(sql, params)
    conn.commit()


def limit_handled1(param):
    global api
    while True:
        try:
            yield api.retweets(param)
        except tweepy.RateLimitError:
            print('sleep start')
            time.sleep(15 * 60)
            print('sleep complete')
        except tweepy.TweepError:
            api=tweepy.API(auth)



for q in query:
    for tweets in limit_handled(tweepy.Cursor(api.search, q=q, show_user=True).items()):
        temp=tweets._json
        if 'retweeted_status' in temp:
            insert_entries(temp['retweeted_status'],q)
            while True:
                try:
                    ret=api.retweets(temp['retweeted_status']['id'])
                    break;
                except tweepy.RateLimitError:
                    print('sleep start')
                    time.sleep(15 * 60)
                    print('sleep complete')
                except tweepy.TweepError:
                    api=tweepy.API(auth)
            for t in ret:
                t = t._json
                insert_entries(t, q)
                insert_retweet(t['user']['id'], temp['retweeted_status']['user']['id'], t['id'],
                               temp['retweeted_status']['id'])
        else:
            insert_entries(temp, q)

