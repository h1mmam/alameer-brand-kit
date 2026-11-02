# Generates music bed + SFX (synced to index.html timeline) -> music.wav, sfx.wav (44.1k stereo)
import numpy as np, wave, sys
out=sys.argv[1]
SR=44100; DUR=86.5; N=int(SR*DUR)
rs=np.random.RandomState(3)
def hz(n):return 440*2**((n-69)/12)
def reverb(x,mix=.2):
    o=x.copy()
    for d,g in [(0.029,.35),(0.047,.28),(0.071,.22),(0.113,.15),(0.17,.1)]:
        n=int(d*SR);o[n:]+=x[:-n]*g*mix*3
    return o
# ---------- music ----------
t=np.arange(N)/SR
bpm=88;beat=60/bpm;bar=beat*4
chords=[(57,[57,60,64]),(53,[53,57,60]),(48,[48,52,55]),(55,[55,59,62])]
m=np.zeros(N)
for b in range(int(DUR/bar)+2):
    root,notes=chords[b%4];t0=b*bar;a=int(t0*SR)
    if a>=N:break
    n=min(int((bar+1.6)*SR),N-a);tt=np.arange(n)/SR
    env=np.minimum(tt/1.0,1)*np.exp(-np.maximum(tt-bar,0)*2.2)
    pad=sum(np.sin(2*np.pi*hz(nt+12)*(1+dt*.01)*tt)*.35+np.sin(2*np.pi*hz(nt)*(1+dt*.01)*tt)*.5 for nt in notes for dt in (0,.15,-.15))
    bass=np.sin(2*np.pi*hz(root-12)*tt)*.9
    m[a:a+n]+=(pad*.09+bass*.24)*env
    arp=[notes[0]+24,notes[1]+24,notes[2]+24,notes[1]+24,notes[2]+24,notes[1]+24,notes[0]+36,notes[1]+24]
    for j,nt in enumerate(arp):
        s0=int((t0+j*beat/2)*SR);mm=int(1.2*SR)
        if s0+mm>=N:continue
        t2=np.arange(mm)/SR
        pl=(np.sin(2*np.pi*hz(nt)*t2)+.3*np.sin(2*np.pi*hz(nt)*2*t2))*np.exp(-t2*3.6)*np.minimum(t2/.004,1)
        m[s0:s0+mm]+=pl*.06*(1 if j%2==0 else .65)
# punchy kick + soft hat for drive
for b in range(int(DUR/beat)):
    s0=int(b*beat*SR);mm=int(.3*SR)
    if s0+mm>=N:break
    t2=np.arange(mm)/SR
    if b%2==0 and b>=2: m[s0:s0+mm]+=np.sin(2*np.pi*(52+90*np.exp(-t2*28))*t2)*np.exp(-t2*10)*.30
    if b%2==1 and b>=4:
        h=np.diff(rs.randn(mm+1))*np.exp(-t2*45)*.05;m[s0:s0+mm]+=h
m=reverb(m,.4)
env=np.minimum(t/1.5,1)*np.minimum((DUR-t)/3.0,1)
m=m*env
m*=.6/np.max(np.abs(m))
# ---------- sfx ----------
sfx=np.zeros(N)
def put(x,at,g=1.0):
    a=int(at*SR);x=x[:max(0,N-a)]
    if a<N:sfx[a:a+len(x)]+=x*g
def whoosh(dur=.7,peak=.5):
    n=int(dur*SR);tt=np.arange(n)/SR;x=rs.randn(n)
    # band-sweep via cumulative lowpass mix
    sweep=np.sin(np.pi*np.linspace(0,1,n))**1.6
    y=np.zeros(n);prev=0
    for i in range(n):
        a=.02+.55*sweep[i];prev+=a*(x[i]-prev);y[i]=prev
    y*=sweep*2.4
    return y/np.max(np.abs(y))
def pop(f0=420,dur=.18):
    n=int(dur*SR);tt=np.arange(n)/SR
    return np.sin(2*np.pi*(f0+700*np.exp(-tt*30))*tt)*np.exp(-tt*22)
def tick():
    n=int(.09*SR);tt=np.arange(n)/SR
    return (np.sin(2*np.pi*1500*tt)+.5*np.sin(2*np.pi*2300*tt))*np.exp(-tt*55)*.5
def click():
    n=int(.12*SR);tt=np.arange(n)/SR
    return (np.sin(2*np.pi*900*tt)*np.exp(-tt*50)+rs.randn(n)*np.exp(-tt*120)*.4)
def slam():
    n=int(.5*SR);tt=np.arange(n)/SR
    return np.sin(2*np.pi*(70+120*np.exp(-tt*22))*tt)*np.exp(-tt*9)+rs.randn(n)*np.exp(-tt*60)*.5
def ping():
    n=int(.5*SR);tt=np.arange(n)/SR
    return (np.sin(2*np.pi*1318*tt)+.4*np.sin(2*np.pi*1975*tt))*np.exp(-tt*9)*np.minimum(tt/.003,1)*.6
def boom():
    n=int(1.8*SR);tt=np.arange(n)/SR
    return np.sin(2*np.pi*(46+80*np.exp(-tt*6))*tt)*np.exp(-tt*2.2)+rs.randn(n)*np.exp(-tt*5)*.18
def shimmer():
    n=int(1.4*SR);tt=np.arange(n)/SR;y=np.zeros(n)
    for k,f in enumerate([1568,2093,2637,3136]):
        y+=np.sin(2*np.pi*f*tt)*np.exp(-(tt-k*.07).clip(0)*3)*(tt>=k*.07)
    return y*.25
W=whoosh(.8)
put(W,.0,.55); put(whoosh(.9),22.4-.45,.7); put(whoosh(.9),80.1-.45,.8)
put(boom(),80.45,.55); put(shimmer(),80.75,.5)
put(whoosh(.35,.4),17.7-.1,.4)                       # cut whip
for at in (.55,5.7,8.7,19.0): put(pop(),at,.5)
for at in (13.74,14.84): put(slam(),at,.55)
put(pop(500),16.3,.45)
for at in (72.2,72.9): put(slam(),at,.55)
for at in (36.1,46.2,56.4,62.3,70.3): put(click(),at,.7)
for at in (38.0,39.7,41.9): put(ping(),at,.5)
for at in (76.0,77.2,36.9,34.0,46.8,57.0,68.6): put(pop(380,.2),at,.4)
for at in (26.5,30.7,35.6,37.9,43.6,51.9,54.7,59.8,66.4,72.0,74.7): put(tick(),at,.7)
put(pop(300),82.5,.6); put(shimmer(),82.5,.3)
sfx=reverb(sfx,.1);sfx*=.9/np.max(np.abs(sfx))
def save(x,p):
    st=np.stack([x,np.roll(x,int(.0012*SR))],1)
    w=wave.open(p,'wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR)
    w.writeframes((np.clip(st,-1,1)*32767).astype(np.int16).tobytes());w.close()
save(m,out+'/music.wav');save(sfx,out+'/sfx.wav')
print('ok')
