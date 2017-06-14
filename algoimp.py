import psycopg2
import random
import heapq

conn = psycopg2.connect("dbname='twitterdb1' user='postgres' host='localhost' password='zxasqw12'")
cur=conn.cursor()
S=[]


V=[]

MG=[]

W=None

lmin=None
lmax=None
delta=None
Tmax=None


class Node:
    def __init__(self, id, ferc,fingc,tc):
        self.id = id
        self.index=None
        self.follower_count = ferc
        self.following_count = fingc
        self.tweets_count = tc
        self.weight = None

    def __lt__(self, other):
         return self.weight-other.weight


def findWx(u,v):
    global lmin,lmax,W
    sql = '''SELECT * FROM followerstable WHERE user_id=%s AND follower_user_id=%s'''
    params = (V[u].id, V[v].id)
    cur.execute(sql, params)
    records = cur.fetchall()
    if len(records) != 0:
        if V[v].following_count!=0:
            W[u][v] =(1 / V[v].following_count) * (V[u].tweets_count / Tmax)
        W[u][v]+=(records[0][2]-3)/103489289
        if lmin==None or lmin>W[u][v]:
            lmin=W[u][v]
        if lmax==None or lmax<W[u][v]:
            lmax=W[u][v]
        print(W[u][v])
    else:
        W[u][v]=0

def inf(x,v):
    if W[x][v]==0:
        return 0
    return (W[x][v]-lmin)/(lmax-lmin)

def calculateMG(x):
    res=0
    for v in MG:
        if v not in S:
            res+=inf(x,v.index)
    return res





sql = '''SELECT user_id,follower_count,following_count,tweets_count FROM followers ORDER BY follower_count DESC LIMIT 1000'''
cur.execute(sql)
records = cur.fetchall()
i=0
for t in records:
    if Tmax==None or Tmax<t[3]:
        Tmax=t[3]
    temp=Node(t[0],t[1],t[2],t[3])
    temp.index=i
    i+=1
    V.append(temp)
W=[[0 for x in range(len(V))] for y in range(len(V))]
for u in range(len(V)):
    for v in range(len(V)):
        findWx(u,v)

for v in V:
    v.weight=1+calculateMG(v.index)
    # v.weight = 1+random.random()
    heapq.heappush(MG,v)

nodeMax=heapq.heappop(MG)
S.append(nodeMax)

while len(S)<10:
    nodeMax = heapq.heappop(MG)
    for v in MG:
        MG.remove(v)
        v.weight = 1 + calculateMG(v.index)
        MG.append(v)
    heapq.heapify(MG)
    temp=heapq.heappop(MG)
    if nodeMax.weight>=temp.weight:
        S.append(nodeMax)
        print(len(S))
    else:
        heapq.heappush(MG, temp)
        heapq.heappush(MG, nodeMax)

for s in S:
    print(s.id)

