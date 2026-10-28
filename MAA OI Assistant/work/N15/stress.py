from pathlib import Path
import subprocess, time, random, json, threading
import ctypes
from ctypes import wintypes

class Memory(ctypes.Structure):
    _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)]+[(x,ctypes.c_size_t) for x in ['PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage']]
get_memory=ctypes.WinDLL('psapi').GetProcessMemoryInfo
get_memory.argtypes=[wintypes.HANDLE,ctypes.POINTER(Memory),wintypes.DWORD]
get_memory.restype=wintypes.BOOL

ROOT=Path(__file__).resolve().parents[2]
TMP=ROOT/'work/N15'
BIN=TMP/'bin'
rows=[]

def run(name,path,expected=None):
    with path.open('rb') as inp:
        begin=time.perf_counter()
        proc=subprocess.Popen([str(BIN/(name+'.exe'))],stdin=inp,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        peak=[0]
        def watch():
            while proc.poll() is None:
                info=Memory();info.cb=ctypes.sizeof(info)
                if get_memory(int(proc._handle),ctypes.byref(info),info.cb):peak[0]=max(peak[0],info.PeakWorkingSetSize)
                time.sleep(0.01)
        t=threading.Thread(target=watch);t.start()
        out,err=proc.communicate(timeout=120);t.join()
        elapsed=time.perf_counter()-begin
    if proc.returncode:raise RuntimeError((name,proc.returncode,err))
    if expected is not None:assert out.decode().split()==list(map(str,expected)),(name,out[:200],expected[:200])
    row={'program':name,'input':path.name,'seconds':round(elapsed,3),'peak_working_set_MiB':round(peak[0]/1024**2,2),'checked_expected':expected is not None,'output_preview':out.decode()[:80]}
    rows.append(row);print(row,flush=True)

rng=random.Random(20261013)
p=TMP/'cookoff_million_random.in'
with p.open('w') as f:
    n=m=1000000;f.write(f'{n} {m}\n')
    for z in range(n+m):f.write(f'1 {rng.randint(1,n+m)} {rng.randint(-10**9,10**9)}\n')
run('G123910_std',p)
p=TMP/'cookoff_million_all_early.in'
with p.open('w') as f:
    n=m=1000000;f.write(f'{n} {m}\n')
    for z in range(n+m):f.write('1000000000 2000000000000000 -1000000000\n')
run('G123910_std',p,[-2000000000000000])
p=TMP/'subseq_max_random.in'
with p.open('w') as f:
    n=50000;k=20;q=200000
    f.write(f'{n} {k}\n'+' '.join(str(rng.randint(1,k)) for _ in range(n))+f'\n{q}\n')
    for _ in range(q):
        l=rng.randint(1,n);r=rng.randint(l,n);f.write(f'{l} {r}\n')
run('G123909_std',p)
p=TMP/'subseq_max_same.in'
with p.open('w') as f:
    n=50000;k=20;q=200000
    f.write(f'{n} {k}\n'+' '.join(['20']*n)+f'\n{q}\n')
    for _ in range(q):f.write(f'1 {n}\n')
run('G123909_std',p,[pow(2,50000,1000000007)]*200000)
p=TMP/'upkeep_max_cycle.in'
with p.open('w') as f:
    n=m=2000;f.write(f'{n} {m}\n')
    for i in range(1,n+1):f.write(f'{i} {i%n+1} 1000000000 1000000000\n')
run('G123908_std',p,[2000000000000])
p=TMP/'erase_max.in';p.write_text('ABC'*100000+'\n')
run('G123907_std',p,[100000])
(TMP/'stress.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
