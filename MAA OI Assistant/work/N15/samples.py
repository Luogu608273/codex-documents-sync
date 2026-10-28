from pathlib import Path
import subprocess, concurrent.futures, json
ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'outputs/N15';TMP=ROOT/'work/N15';BIN=TMP/'bin'
CXX='C:/TDM-GCC-64/bin/g++.exe'

samples={
'G123907': [('ABCBA\n','2'),('ABCBBACBABB\n','5')],
'G123908': [('5 7\n1 2 15 1\n2 4 9 9\n5 2 5 6\n4 5 4 4\n4 3 3 7\n1 3 2 7\n1 4 2 1\n','25')],
'G123909': [('5 2\n1 2 1 1 2\n3\n2 3\n4 5\n1 5\n','3 4 20')],
'G123910': [('4 3\n2 1 1\n3 8 1\n2 13 1\n1 13 1\n3 6 1\n2 11 1\n2 15 1\n','6'),('5 7\n16 73 16\n17 73 10\n20 73 1\n14 73 16\n18 73 10\n3 73 2\n10 73 7\n16 73 19\n12 73 4\n15 73 15\n20 73 14\n15 73 8\n','63'),('9 11\n86 565 58\n41 469 -95\n73 679 28\n91 585 -78\n17 513 -63\n48 878 -66\n66 901 59\n72 983 -70\n68 1432 11\n42 386 -87\n36 895 57\n100 164 10\n96 812 -6\n23 961 -66\n54 193 51\n37 709 82\n62 148 -36\n28 853 22\n15 44 53\n77 660 -19\n','99')]
}
io={'G123907':'erase','G123908':'upkeep','G123909':'subseq','G123910':'cookoff'}
def build(p):
 out=BIN/(p.stem+'_fileio.exe')
 r=subprocess.run([CXX,'-std=c++17','-O2','-Wall','-Wextra',str(p),'-o',str(out)],capture_output=True,text=True)
 assert r.returncode==0 and not r.stderr,(p.name,r.stderr)
 return p.stem
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: print('File-IO builds:',list(pool.map(build,SRC.glob('*.cpp'))),flush=True)
rows=[]
for key,tests in samples.items():
 for z,(inp,ans) in enumerate(tests,1):
  path=TMP/'fileio'/f'{key}_{z}';path.mkdir(parents=True,exist_ok=True)
  (path/(io[key]+'.in')).write_text(inp,encoding='utf-8')
  r=subprocess.run([str(BIN/(key+'_std_fileio.exe'))],cwd=path,capture_output=True,text=True,timeout=10)
  got=(path/(io[key]+'.out')).read_text().split()
  assert r.returncode==0 and got==ans.split(),(key,z,r.returncode,got,ans,r.stderr)
  rows.append({'program':key+'_std','sample':z,'result':'PASS','mode':'default file IO'})
print('Official PDF samples PASS:',len(rows),flush=True)
special=[('G123907_partial_5','AABB\n','2'),('G123907_partial_57',samples['G123907'][0][0],'2'),('G123908_partial_20','4 4\n1 2 0 7\n1 2 0 3\n2 3 0 4\n1 3 0 20\n','7'),('G123909_partial_24',samples['G123909'][0][0],'3 4 20'),('G123910_partial_5',samples['G123910'][1][0],'63'),('G123910_partial_10',samples['G123910'][2][0],'99')]
for name,inp,ans in special:
 key=name.split('_')[0];path=TMP/'fileio'/name;path.mkdir(parents=True,exist_ok=True)
 (path/(io[key]+'.in')).write_text(inp,encoding='utf-8')
 r=subprocess.run([str(BIN/(name+'_fileio.exe'))],cwd=path,capture_output=True,text=True,timeout=10)
 got=(path/(io[key]+'.out')).read_text().split()
 assert r.returncode==0 and got==ans.split(),(name,got,ans)
 rows.append({'program':name,'case':'sample or valid subtask edge case','result':'PASS','mode':'default file IO'})
(TMP/'samples.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('Partial file-IO checks PASS:',len(special),flush=True)
