import psycopg2
import random

conn = psycopg2.connect("dbname='twitterdb1' user='postgres' host='localhost' password='zxasqw12'")
cur=conn.cursor()


def fun():
    sql = '''SELECT user_id,follower_count FROM followers ORDER BY follower_count DESC LIMIT 1000'''
    cur.execute(sql)
    records = cur.fetchall()
    V = []
    for t in records:
        V.append(t[0])

    maxf = records[0][1]
    for t in records:
        temp = t[1] * 100 / maxf
        print(t[1], temp)
        if int(temp)==0:
            temp=random.randrange(0,5)
        templ = random.sample(V, int(temp))
        for s in templ:
            if s != t[0]:
                sql = '''INSERT INTO followerstable (user_id, follower_user_id) VALUES (%s,%s)'''
                params = (t[0], s)
                cur.execute(sql, params)
                conn.commit()


def fun2():
    sql = '''SELECT user_id,follower_user_id FROM followerstable'''
    cur.execute(sql)
    records = cur.fetchall()
    for r in records:
        sql = '''SELECT created_at FROM tweets WHERE user_id=%s ORDER BY created_at DESC LIMIT 1'''
        params=(r[0],)
        cur.execute(sql,params)
        rr1 = cur.fetchall()
        sql = '''SELECT created_at FROM tweets WHERE user_id=%s ORDER BY created_at DESC LIMIT 1'''
        params = (r[1],)
        cur.execute(sql,params)
        rr2 = cur.fetchall()
        temp=abs(rr1[0][0]-rr2[0][0])
        temp=temp.days*60*24*60+temp.seconds
        sql = '''UPDATE followerstable SET timeweight=%s WHERE user_id=%s AND follower_user_id=%s'''
        params = (temp,r[0],r[1])
        cur.execute(sql, params)
        conn.commit()


fun2()






