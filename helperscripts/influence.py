import psycopg2
conn = psycopg2.connect("dbname='twitterdb' user='postgres' host='localhost' password='zxasqw12'")
cur=conn.cursor()

Smax=None
Mmax=None
Tmax=None
V=[]
W=[]
def assignConstants():
    global Smax,Mmax,Tmax,V
    # sql = '''SELECT COUNT(*) as a FROM followers GROUP BY user_id ORDER BY a DESC '''
    # cur.execute(sql)
    # records = cur.fetchall()
    # Smax=records[0][0]
    sql = '''SELECT COUNT(*) as a FROM mentions GROUP BY user_id ORDER BY a DESC '''
    cur.execute(sql)
    records = cur.fetchall()
    Mmax = records[0][0]
    sql = '''SELECT COUNT(*) as a FROM retweet GROUP BY parent_user_id ORDER BY a DESC '''
    cur.execute(sql)
    records = cur.fetchall()
    Tmax = records[0][0]
    sql = '''SELECT DISTINCT user_id FROM tweets'''
    cur.execute(sql)
    records=cur.fetchall()
    for v in records:
        V.append(v[0])


def S(u):
    sql = '''SELECT follower_user_id FROM followers WHERE user_id=%s'''
    params = (u,)
    cur.execute(sql, params)
    records = cur.fetchall()
    return records

def P(v):
    sql = '''SELECT user_id FROM followers WHERE follower_user_id=%s'''
    params = (v,)
    cur.execute(sql, params)
    records = cur.fetchall()
    return records

def R(u,v):
    sql = '''SELECT tweet_id FROM retweet WHERE user_id=%s AND parent_tweet_id=%s'''
    params = (v,u)
    cur.execute(sql, params)
    records = cur.fetchall()
    return records

def M(u,v):
    sql = '''SELECT tweet_id FROM mentions WHERE user_id=%s AND metioned_user_id=%s'''
    params = (u,v)
    cur.execute(sql, params)
    records = cur.fetchall()
    return records

def Wf(u,v):
    temp=len(set(S(u)) & set(S(v)))+1
    return temp/Smax

def Wm(u,v):
    temp=len(M(u,v))
    return temp/Mmax

def Wr(u,v):
    temp=len(R(u,v))
    return temp/Tmax

def Wx(u,v):
    return Wr(u,v)+Wm(u,v)

assignConstants()
Nmin=None
Nmax=None
fl=open('hello.txt',"w")
for u in V:
    for v in V:
        if u!=v:
            t=Wx(u,v)
            fl.write(str(u)+' '+str(v)+' '+str(t)+'\n')

