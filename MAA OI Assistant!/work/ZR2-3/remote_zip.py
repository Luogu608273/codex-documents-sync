import urllib.request, struct, io, zipfile, zlib
from pathlib import Path
U='https://jag-icpc.org/files/summer-camp-2026-day2-data.zip'
def get(a,b):
    r=urllib.request.urlopen(urllib.request.Request(U,headers={'Range':f'bytes={a}-{b}'}))
    data=r.read()
    if r.status!=206: raise RuntimeError((r.status,len(data)))
    return data
r=urllib.request.urlopen(urllib.request.Request(U,method='HEAD'))
n=int(r.headers['Content-Length'])
d=get(n-65536,n-1)
p=d.rfind(b'PK\x05\x06')
e=struct.unpack_from('<4s4H2LH',d,p)
size,off=e[5:7]
central=get(off,off+size-1)
z=zipfile.ZipFile(io.BytesIO(central+d[p:]))
files=z.infolist()
for f in files:
    if f.filename.endswith('.pdf'): print(f.filename,f.file_size)
for f in files:
    if f.filename.endswith('.pdf') and ('solution' in f.filename.lower() or 'editorial' in f.filename.lower()):
        q=off+f.header_offset
        h=get(q,q+29)
        v=struct.unpack('<4s5H3L2H',h)
        start=q+30+v[-2]+v[-1]
        raw=get(start,start+f.compress_size-1)
        raw=zlib.decompress(raw,-15) if f.compress_type==8 else raw
        name=f.filename.rsplit('/',1)[-1]
        open('work/ZR2-3/'+name,'wb').write(raw)
        print('saved',name)
for f in files:
    if f.filename.endswith('/C.zip'):
        q=off+f.header_offset
        v=struct.unpack('<4s5H3L2H',get(q,q+29))
        start=q+30+v[-2]+v[-1]
        raw=get(start,start+f.compress_size-1)
        raw=zlib.decompress(raw,-15) if f.compress_type==8 else raw
        zz=zipfile.ZipFile(io.BytesIO(raw))
        target=Path('work/ZR2-3/official_C')
        target.mkdir(exist_ok=True)
        for x in zz.infolist():
            if x.filename.endswith(('.in','.ans')):
                (target/x.filename.rsplit('/',1)[-1]).write_bytes(zz.read(x))
        print([(x.filename,x.file_size) for x in zz.infolist() if not x.is_dir()][:60])
        for x in zz.infolist():
            if x.filename.lower().endswith(('.pdf','.cpp','.html','.md')):
                name='C_'+x.filename.rsplit('/',1)[-1]
                open('work/ZR2-3/'+name,'wb').write(zz.read(x))
                print('saved',name)
