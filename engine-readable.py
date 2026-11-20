import json,os,sys,urllib.request
U=os.environ['MAKEFUN_ENV_URL']
V={'P':100,'N':320,'B':330,'R':500,'Q':900,'K':0,'p':-100,'n':-320,'b':-330,'r':-500,'q':-900,'k':0}
D=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
N=[(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]
def pos(f):
 b=[]
 for r in f.split()[0].split('/')[::-1]:
  for c in r:b += ['.']*int(c) if c.isdigit() else [c]
 return b,f.split()[1],f.split()[2],f.split()[3]
def xy(i):return i&7,i>>3
def sq(x,y):return y*8+x
def attacked(b,i,by):
 x,y=xy(i)
 for dx,dy in N:
  q=sq(x+dx,y+dy) if 0<=x+dx<8 and 0<=y+dy<8 else -1
  if q>=0 and b[q]==('N' if by=='w' else 'n'):return 1
 for dx,dy in D:
  xx,yy=x+dx,y+dy;n=1
  while 0<=xx<8 and 0<=yy<8:
   p=b[sq(xx,yy)]
   if p!='.':
    if (p in (('B','Q') if abs(dx)==abs(dy) else ('R','Q'))) if by=='w' else (p in (('b','q') if abs(dx)==abs(dy) else ('r','q'))):return 1
    break
   xx+=dx;yy+=dy;n+=1
 for dx,dy in D:
  if max(abs(dx),abs(dy))==1:
   q=sq(x+dx,y+dy) if 0<=x+dx<8 and 0<=y+dy<8 else -1
   if q>=0 and b[q]==('K' if by=='w' else 'k'):return 1
 py=y-1 if by=='w' else y+1
 for xx in (x-1,x+1):
  if 0<=xx<8 and 0<=py<8 and b[sq(xx,py)]==('P' if by=='w' else 'p'):return 1
 return 0
def check(b,c):
 k=b.index('K' if c=='w' else 'k');return attacked(b,k,'b' if c=='w' else 'w')
def moves(b,c,cr,ep):
 out=[];W=c=='w'
 for i,p in enumerate(b):
  if p=='.' or p.isupper()!=W:continue
  x,y=xy(i); u=p.upper()
  z=[]
  if u=='N':z=[(x+dx,y+dy) for dx,dy in N]
  elif u=='K':
   z=[(x+dx,y+dy) for dx,dy in D if max(abs(dx),abs(dy))==1]
   if W and i==4 and 'K' in cr and b[5]==b[6]=='.' and b[7]=='R' and not check(b,c) and not attacked(b,5,'b') and not attacked(b,6,'b'):z += [(6,0)]
   if W and i==4 and 'Q' in cr and b[1]==b[2]==b[3]=='.' and b[0]=='R' and not check(b,c) and not attacked(b,3,'b') and not attacked(b,2,'b'):z += [(2,0)]
   if not W and i==60 and 'k' in cr and b[61]==b[62]=='.' and b[63]=='r' and not check(b,c) and not attacked(b,61,'w') and not attacked(b,62,'w'):z += [(62,7)]
   if not W and i==60 and 'q' in cr and b[57]==b[58]==b[59]=='.' and b[56]=='r' and not check(b,c) and not attacked(b,59,'w') and not attacked(b,58,'w'):z += [(58,7)]
  elif u=='P':
   dy=1 if W else -1
   if 0<=y+dy<8:
    if b[sq(x,y+dy)]=='.':z += [(x,y+dy)]+([(x,y+2*dy)] if y==(1 if W else 6) and b[sq(x,y+2*dy)]=='.' else [])
    for xx in (x-1,x+1):
     if 0<=xx<8 and (b[sq(xx,y+dy)]!='.' and b[sq(xx,y+dy)].isupper()!=W or sq(xx,y+dy)==ep):z += [(xx,y+dy)]
  else:
   z=[];ds=D if u in 'RQ' else [(1,1),(1,-1),(-1,1),(-1,-1)]
   for dx,dy in ds:
    xx,yy=x+dx,y+dy
    while 0<=xx<8 and 0<=yy<8:
     z.append((xx,yy))
     if u=='N':break
     if b[sq(xx,yy)]!='.':break
     xx+=dx;yy+=dy
  for xx,yy in z:
   if not(0<=xx<8 and 0<=yy<8):continue
   j=sq(xx,yy);q=b[j]
   if q!='.' and (q.isupper()==W or q.upper()=='K'):continue
   if u=='K' and abs(xx-x)==2 and check(b,c):continue
   nb=b[:];nb[j]=p;nb[i]='.'
   if u=='P' and j==ep and q=='.':nb[j+( -8 if W else 8)]='.'
   if u=='K' and abs(xx-x)==2:
    r=7 if xx>x else 0;nb[sq(5 if xx>x else 3,r)]=nb[sq(7 if xx>x else 0,r)];nb[sq(7 if xx>x else 0,r)]='.'
   if u=='P' and yy in (0,7):
    for pp in 'QRBN':
     t=pp if W else pp.lower();n2=nb[:];n2[j]=t
     if not check(n2,'b' if W else 'w'):out.append((i,j,n2,t))
    continue
   if not check(nb,'b' if W else 'w'):out.append((i,j,nb,''))
 return out
def um(i,j,p):return 'abcdefgh'[i&7]+str(i//8+1)+'abcdefgh'[j&7]+str(j//8+1)+(p.lower() if p else '')
def apply(b,c,cr,ep,m):
 i,j,nb,p=m; nc='b' if c=='w' else 'w';nr=cr
 if b[i].upper()=='K':nr=nr.replace('K' if c=='w' else 'k','').replace('Q' if c=='w' else 'q','')
 if i in (0,7,56,63):nr=nr.replace(('Q','K','q','k')[(i in (7,0,56,63)) and 0 or 0],'') if False else nr
 ne=-1
 if b[i].upper()=='P' and abs(j-i)==16:ne=(i+j)//2
 return nb,nc,nr,ne
def ev(b):return sum(V.get(x,0) for x in b)
def search(b,c,cr,ep,d,a=-99999,z=99999):
 ms=moves(b,c,cr,ep)
 if not ms:return (-99999 if check(b,c) else 0,None)
 if d==0:return ((ev(b) if c=='w' else -ev(b)),None)
 best=-999999;bm=None
 for m in sorted(ms,key=lambda x:(V.get(b[x[1]],0),b[x[0]].upper()!='R',-abs((x[1]&7)-3.5)-abs((x[1]>>3)-3.5)),reverse=True):
  x,_,_,_=apply(b,c,cr,ep,m);v=-search(x,'b' if c=='w' else 'w',cr,-1,d-1,-z,-a)[0]
  if v>best:best,bm=v,m
  a=max(a,v)
  if a>=z:break
 return best,bm
def post(p,x):
 q=urllib.request.Request(U+p,data=json.dumps(x).encode(),headers={'content-type':'application/json'})
 return json.load(urllib.request.urlopen(q))
while 1:
 g=post('/game',{})
 if g['status']=='done':break
 while g['status']=='your_move':
  b,c,cr,ep=pos(g['fen']);ep=-1 if ep=='-' else sq(ord(ep[0])-97,int(ep[1])-1)
  legal=g['legal_moves'];_,m=search(b,c,cr,ep,3)
  move=um(m[0],m[1],m[3]) if m else legal[0]
  if move not in legal:move=legal[0]
  g=post('/move',{'game':g['game'],'move':move})
print(g.get('wins'),g.get('draws'),g.get('losses'),file=sys.stderr)
