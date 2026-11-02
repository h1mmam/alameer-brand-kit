import numpy as np, subprocess, wave, os
SR=44100; DUR=56.0
# (start, max_end, text)
LINES=[
(0.4,4.2,"تطبيق الأمير. قطع الهيدروليك والمعدات الثقيلة، بين يديك."),
(4.95,9.8,"حمّل التطبيق، وسجّل دخولك بجوجل أو آبل أو واتساب."),
(10.1,15.9,"في الرئيسية: الآليات، والأخبار، وأحدث المنتجات."),
(16.4,22.5,"تصفّح حسب النوع: قطع غيار، فلاتر، شحمة، وزيوت. أو ابحث بكود المنتج."),
(23.0,28.8,"أسعار واضحة بالشيكل، وعروض وخصومات. والسعر الخاص؟ اطلب السعر."),
(29.2,31.1,"أولًا: أضف للسلة."),
(31.5,33.3,"ثانيًا: توصيل أو استلام."),
(33.7,35.5,"ثالثًا: بيانات المستلم."),
(35.9,37.7,"رابعًا: كود الخصم."),
(38.1,41.0,"خامسًا: أكّد الطلب."),
(41.5,46.2,"تابع طلبك خطوة بخطوة، وقيّم منتجاتك."),
(46.6,50.9,"وآليات للبيع، ودردشة ودعم مباشر."),
(51.3,55.8,"حمّل تطبيق الأمير الآن."),
]
def read(p):
    w=wave.open(p);d=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768;return d
voice=np.zeros(int(SR*DUR))
dm=np.zeros(len(voice))  # duck mask
for i,(s,e,t) in enumerate(LINES):
    rate=190
    while True:
        subprocess.run(["say","-v","Majed","-r",str(rate),"-o",f"l{i}.wav","--data-format=LEI16@44100",t],check=True)
        d=read(f"l{i}.wav")
        # trim silence
        nz=np.where(np.abs(d)>0.01)[0]; d=d[nz[0]:nz[-1]+1]
        if len(d)/SR<=e-s or rate>=250: break
        rate+=8
    print(i,rate,round(len(d)/SR,2),'/',round(e-s,2))
    d=d/np.max(np.abs(d))*0.9
    f=int(0.02*SR);d[:f]*=np.linspace(0,1,f);d[-f:]*=np.linspace(1,0,f)
    a=int(s*SR);voice[a:a+len(d)]+=d[:len(voice)-a]
    dm[max(0,a-int(.25*SR)):a+len(d)+int(.4*SR)]=1
# warm voice: gentle lowpass-ish + short reverb
def reverb(x,mix=.12):
    out=x.copy()
    for dly,g in [(0.029,.35),(0.047,.28),(0.071,.22),(0.113,.15),(0.17,.1)]:
        n=int(dly*SR);out[n:]+=x[:-n]*g*mix*3
    return out
voice=reverb(voice)
k=np.ones(3)/3;voice=np.convolve(voice,k,'same')*0.6+voice*0.4
voice=np.tanh(voice*1.6)/1.0
voice*=0.95/np.max(np.abs(voice))
# ---- music ----
t=np.arange(len(voice))/SR
bpm=76;beat=60/bpm;bar=beat*4
def hz(n):return 440*2**((n-69)/12)
chords=[(57,[57,60,64]),(53,[53,57,60]),(48,[48,52,55]),(55,[55,59,62])]  # Am F C G
music=np.zeros(len(t))
for b in range(int(DUR/bar)+2):
    root,notes=chords[b%4]
    t0=b*bar;a=int(t0*SR);n=int((bar+1.6)*SR)
    if a>=len(t):break
    n=min(n,len(t)-a);tt=np.arange(n)/SR
    env=np.minimum(tt/1.1,1)*np.exp(-np.maximum(tt-bar,0)*2.2)
    pad=np.zeros(n)
    for nt in notes:
        for dt,ch in [(0,12),(0.15,12),(-0.15,12),(0,24)]:
            f=hz(nt+ch*0)*(1+dt*0.01); pad+=np.sin(2*np.pi*f*tt)*(.5 if ch==12 else .0)
            pad+=np.sin(2*np.pi*hz(nt+12)*(1+dt*0.01)*tt)*0.35
    bass=np.sin(2*np.pi*hz(root-12)*tt)*0.9
    music[a:a+n]+=(pad*0.12+bass*0.22)*env
    # arpeggio plucks
    arp=[notes[0]+24,notes[1]+24,notes[2]+24,notes[1]+24,notes[2]+24,notes[1]+24,notes[0]+36,notes[1]+24]
    for j,nt in enumerate(arp):
        s0=int((t0+j*beat/2)*SR)
        m=int(1.4*SR)
        if s0+m>=len(t):continue
        tt2=np.arange(m)/SR
        pl=(np.sin(2*np.pi*hz(nt)*tt2)+0.3*np.sin(2*np.pi*hz(nt)*2*tt2))*np.exp(-tt2*3.2)*np.minimum(tt2/0.004,1)
        music[s0:s0+m]+=pl*0.07*(1 if j%2==0 else .7)
# soft kick/ pulse feel: very subtle low heartbeat on beats 1 & 3
for b in range(int(DUR/beat)):
    if b%2==0:
        s0=int(b*beat*SR);m=int(.35*SR)
        if s0+m>=len(t):break
        tt2=np.arange(m)/SR
        music[s0:s0+m]+=np.sin(2*np.pi*(55+60*np.exp(-tt2*25))*tt2)*np.exp(-tt2*9)*0.10
music=reverb(music,.5)
# fades + ducking
env=np.minimum(t/2.5,1)*np.minimum((DUR-t)/2.5,1)
duck=1-0.62*np.convolve(dm,np.ones(int(.3*SR))/int(.3*SR),'same')
music=music*env*duck
music*=0.5/np.max(np.abs(music))
mix=voice*0.95+music*0.55
mix*=0.92/np.max(np.abs(mix))
pcm=(mix*32767).astype(np.int16)
with wave.open('mix.wav','wb') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes())
