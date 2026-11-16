from analyze import CPU,P,stats
from collections import OrderedDict
import csv, json
class Cache:
 def __init__(self,size=64,line=16,ways=1,policy='WB'):
  self.policy=policy;self.size=size;self.line=line;self.ways=ways;self.sets=max(1,size//line//ways);self.lines=[OrderedDict() for _ in range(self.sets)];self.h=0;self.m=0;self.writes=0;self.steps=[];self.seen=set()
 def access(self,rw,addr):
  block=addr//self.line;setno=block%self.sets;tag=block//self.sets;bank=self.lines[setno];prior=block in self.seen;ev=None
  if tag in bank:
   hit=True;old=bank.pop(tag);dirty=old['dirty']
   self.h+=1
  else:
   hit=False;self.m+=1;dirty=False
   if len(bank)==self.ways:
    t,info=bank.popitem(last=False);ev=f'0x{((t*self.sets+setno)*self.line):08X}'
    if self.policy=='WB' and info['dirty']:self.writes+=1
  if rw=='W':
   if self.policy=='WT':self.writes+=1
   else:dirty=True
  bank[tag]={'dirty':dirty,'block':block};self.seen.add(block)
  x=dict(i=self.h+self.m,rw=rw,addr=f'0x{addr:08X}',tag=f'0x{tag:X}',line=setno,offset=addr%self.line,hit='Hit' if hit else 'Miss',evict=ev or '-',previous='Evet' if prior else 'Hayır')
  self.steps.append(x)
  return x
 def consume(self,refs):
  for x in refs:self.access(x['rw'],x['addr'])
  return self
 def snapshot(self):
  out=[]
  for i,bank in enumerate(self.lines):
   for tag,e in bank.items():out.append(dict(line=i,tag=f'0x{tag:X}',dirty=int(e['dirty']),valid=1,LRU=list(bank).index(tag)))
   if not bank:out.append(dict(line=i,tag='-',dirty=0,valid=0,LRU='-'))
  return out
 def result(self):return dict(refs=self.h+self.m,hit=self.h,miss=self.m,H=self.h/(self.h+self.m),writes=self.writes,dirty_resident=sum(v['dirty'] for bank in self.lines for v in bank.values()))

def getrefs(cpu):return [x for x in cpu.trace if x['rw']]
def make():
 a=CPU(P/'o0.elf',0,'O0').run(); b=CPU(P/'o1.elf',0x3c,'O1').run();refs=getrefs(a); refs1=getrefs(b)
 model=Cache().consume(refs);baseline=model.result();first=Cache().consume(refs[:30]);print('BASE',baseline,'first30',first.result(),first.snapshot());
 with open(P/'cache_first30.csv','w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=first.steps[0]);w.writeheader();w.writerows(first.steps)
 with open(P/'cache_first30_state.csv','w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=first.snapshot()[0]);w.writeheader();w.writerows(first.snapshot())
 results=[]
 for way in [1,2,4]:
  c=Cache(64,16,way).consume(refs);results.append(dict(kind='mapping',config=f'{way}-way',**c.result()))
 c=Cache(64,16,4).consume(refs);results.append(dict(kind='mapping',config='fully associative',**c.result()))
 for line in [8,16,32,64]:
  c=Cache(64,line,1).consume(refs);results.append(dict(kind='line_size',config=f'{line} B',**c.result()))
 with open(P/'cache_design_space.csv','w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=results[0]);w.writeheader();w.writerows(results)
 print('DESIGN',results)
 print('FIRST5',[(hex(x),format(x,'032b'),hex((x//16)//4),(x//16)%4,x%16) for x in dict.fromkeys([x['addr'] for x in refs[:100]])][:5])
 (P/'cache_summary.json').write_text(json.dumps(dict(base=baseline,first30=first.result(),first30_state=first.snapshot(),space=results),indent=2))
 return a,b,refs,refs1,baseline,results
if __name__=='__main__':make()
