import struct, csv, os, json, math, collections
from pathlib import Path
P=Path('/mnt/data/final_work')
MASK=0xffffffff
def sign(x,b):return x-(1<<b) if x&(1<<(b-1)) else x
def signed(x):return sign(x&MASK,32)
class CPU:
 def __init__(self,elf,pc,source):
  self.reg=[0]*32; self.reg[2]=0x7ffffff0; self.reg[1]=0xffffffff if source=='O1' else 0
  self.pc=pc; self.mem={}; self.trace=[]; self.source=source
  dat=Path(elf).read_bytes(); e_phoff=struct.unpack_from('<I',dat,28)[0]; phentsize,phnum=struct.unpack_from('<HH',dat,42)
  for i in range(phnum):
   off=e_phoff+i*phentsize; typ,fo,va,pa,fs,ms,flags,align=struct.unpack_from('<IIIIIIII',dat,off)
   if typ==1:
    for j,b in enumerate(dat[fo:fo+fs]):self.mem[(va+j)&MASK]=b
    # bss zero implicit
 def read(self,ad,n=4):return sum(self.mem.get((ad+i)&MASK,0)<<(8*i) for i in range(n))
 def write(self,ad,val,n=4):
  for i in range(n):self.mem[(ad+i)&MASK]=(val>>(8*i))&0xff
 def run(self,maxsteps=300000):
  R=self.reg; tr=self.trace
  for st in range(maxsteps):
   pc=self.pc
   if pc in (0xffffffff,0xfffffffe):break
   ins=self.read(pc)
   op=ins&127; rd=(ins>>7)&31; f3=(ins>>12)&7; rs1=(ins>>15)&31; rs2=(ins>>20)&31; f7=(ins>>25)&127; a=R[rs1]; b=R[rs2]; pcnew=(pc+4)&MASK; res=None; da=None; rw=None; cat='ALU'; mnemonic=''
   if op==0x37:res=ins&0xfffff000;mnemonic='lui'
   elif op==0x17:res=(pc+(ins&0xfffff000))&MASK;mnemonic='auipc'
   elif op==0x13:
    imm=sign(ins>>20,12)
    if f3==0:res=a+imm;mnemonic='addi'
    elif f3==7:res=a&imm;mnemonic='andi'
    elif f3==6:res=a|imm;mnemonic='ori'
    elif f3==4:res=a^imm;mnemonic='xori'
    elif f3==1:res=a<<((ins>>20)&31);mnemonic='slli'
    elif f3==5:
     sh=(ins>>20)&31
     res=(signed(a)>>sh) if f7==0x20 else a>>sh;mnemonic='srai' if f7==0x20 else 'srli'
    elif f3==2:res=int(signed(a)<imm);mnemonic='slti'
    elif f3==3:res=int(a<(imm&MASK));mnemonic='sltiu'
    else:raise Exception(('op13',hex(pc),hex(ins)))
   elif op==0x33:
    if f7==1:
     cat='Multiply'
     if f3==0:res=a*b;mnemonic='mul'
     elif f3==1:res=(signed(a)*signed(b))>>32;mnemonic='mulh'
     elif f3==3:res=(a*b)>>32;mnemonic='mulhu'
     else:raise Exception(('mult',hex(pc),hex(ins)))
    elif f3==0:res=a-b if f7==0x20 else a+b;mnemonic='sub' if f7==0x20 else 'add'
    elif f3==2:res=int(signed(a)<signed(b));mnemonic='slt'
    elif f3==3:res=int(a<b);mnemonic='sltu'
    elif f3==4:res=a^b;mnemonic='xor'
    elif f3==6:res=a|b;mnemonic='or'
    elif f3==7:res=a&b;mnemonic='and'
    elif f3==1:res=a<<(b&31);mnemonic='sll'
    elif f3==5:res=signed(a)>>(b&31) if f7==0x20 else a>>(b&31);mnemonic='sra' if f7==0x20 else 'srl'
    else:raise Exception(('op33',hex(pc),hex(ins)))
   elif op==0x03:
    imm=sign(ins>>20,12);da=(a+imm)&MASK; rw='R';cat='Load';mnemonic={2:'lw',0:'lb',4:'lbu',1:'lh',5:'lhu'}[f3];n={0:1,4:1,1:2,5:2,2:4}[f3];res=self.read(da,n)
    if f3 in (0,1):res=sign(res,n*8)
   elif op==0x23:
    imm=((ins>>25)<<5)|((ins>>7)&31);imm=sign(imm,12);da=(a+imm)&MASK;rw='W';cat='Store';n={0:1,1:2,2:4}[f3];self.write(da,b,n);mnemonic={0:'sb',1:'sh',2:'sw'}[f3]
   elif op==0x63:
    imm=((ins>>31)&1)<<12|((ins>>7)&1)<<11|((ins>>25)&63)<<5|((ins>>8)&15)<<1;imm=sign(imm,13)
    cond={0:a==b,1:a!=b,4:signed(a)<signed(b),5:signed(a)>=signed(b),6:a<b,7:a>=b}[f3]
    if cond:pcnew=(pc+imm)&MASK
    cat='Branch/jump';mnemonic={0:'beq',1:'bne',4:'blt',5:'bge',6:'bltu',7:'bgeu'}[f3]
   elif op==0x6f:
    imm=((ins>>31)&1)<<20|((ins>>12)&255)<<12|((ins>>20)&1)<<11|((ins>>21)&1023)<<1;imm=sign(imm,21)
    res=(pc+4)&MASK;pcnew=(pc+imm)&MASK;cat='Branch/jump';mnemonic='jal'
   elif op==0x67:
    imm=sign(ins>>20,12);res=(pc+4)&MASK;pcnew=(a+imm)&0xfffffffe;cat='Branch/jump';mnemonic='jalr'
   elif op==0x73:
    cat='Branch/jump';mnemonic='ecall';tr.append({'i':st+1,'pc':pc,'next_pc':pcnew,'ins':ins,'opcode':mnemonic,'type':cat,'rw':rw,'addr':da,'size':0,'value':None,'stack':None});break
   else:raise Exception(('invalid',hex(pc),hex(ins),op))
   if res is not None and rd!=0:R[rd]=res&MASK
   R[0]=0
   n=4 if rw else 0
   val=(self.read(da,n) if rw else None)
   tr.append({'i':st+1,'pc':pc,'next_pc':pcnew,'ins':ins,'opcode':mnemonic,'type':cat,'rw':rw,'addr':da,'size':n,'value':val,'stack':(da>=0x70000000) if rw else None})
   self.pc=pcnew
  else:raise Exception('maxsteps')
  return self

def stats(cpu):
 c=collections.Counter(x['type'] for x in cpu.trace); reads=[x for x in cpu.trace if x['rw']=='R'];writes=[x for x in cpu.trace if x['rw']=='W']; refs=reads+writes
 cycles=sum(c.get(k,0)*v for k,v in {'ALU':1,'Multiply':3,'Load':1,'Store':1,'Branch/jump':2}.items())
 return dict(instructions=len(cpu.trace),classes=dict(c),loads=len(reads),stores=len(writes),cycles=cycles,cpi=cycles/len(cpu.trace),refs=len(refs),registers=cpu.reg)
if __name__=='__main__':
 a=CPU(P/'o0.elf',0,'O0').run();b=CPU(P/'o1.elf',0x3c,'O1').run()
 for cpu in [a,b]:
  s=stats(cpu)
  print(cpu.source, {k:v for k,v in s.items() if k!='registers'})
  addrmap={'O0':{'bucket':0x100000a4,'mean':0x100000b8,'below':0x100000bc,'pass':0x100000c0},'O1':{'bucket':0x100000a8,'mean':0x100000bc,'below':0x100000c0,'pass':0x100000a4}}[cpu.source]
  print('outputs', {k:cpu.read(v) for k,v in addrmap.items()},'bucket',[cpu.read(addrmap['bucket']+4*i) for i in range(5)])
  with open(P/f'trace_instruction_{cpu.source}.csv','w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(cpu.trace[0]));w.writeheader();w.writerows(cpu.trace)
  with open(P/f'trace_data_{cpu.source}.csv','w',newline='') as f:
   w=csv.writer(f);w.writerow(['sira','RW','adres_hex','boyut','c_satiri','stack_mi','pc_hex','data_hex']);j=0
   for x in cpu.trace:
    if x['rw']:
     j+=1;w.writerow([j,x['rw'],f'0x{x["addr"]:08X}',x['size'],'(PC mapping in map_pc.csv)',int(x['stack']),f'0x{x["pc"]:08X}',f'0x{x["value"]:08X}'])
  (P/f'stats_{cpu.source}.json').write_text(json.dumps({k:v for k,v in s.items() if k!='registers'},indent=2))
