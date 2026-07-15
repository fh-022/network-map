# -*- coding: utf-8 -*-
"""rebuild_completeness.py — regenerate the Completeness sheet + normalize tag spacing."""
import openpyxl, re
from openpyxl.styles import Font, PatternFill
from openpyxl.chart import BarChart, Reference
from collections import Counter

p='/mnt/user-data/outputs/CZ_SK_CH_Dealership_Overview_v3_merged_with_research_status.xlsx'
wb=openpyxl.load_workbook(p)
ws=wb['Locations']
hdr=[r for r in range(1,15) if str(ws.cell(r,2).value).strip()=='#'][0]

# normalize tag spacing
for r in range(hdr+1,ws.max_row+1):
    v=ws.cell(r,7).value
    if v and '[' in str(v):
        nv=re.sub(r'\[\s*S\s*,\s*SV\s*\]','[S,SV]',str(v))
        if nv!=v: ws.cell(r,7).value=nv

ALIAS={'vw group (all brands)':'VW Group','vw group':'VW Group','vw':'Volkswagen','vw lcv':'VW Commercial Vehicles','volkswagen lcv':'VW Commercial Vehicles',
 'vw nutzfahrzeuge':'VW Commercial Vehicles','vw commercial vehicles':'VW Commercial Vehicles',
 'seat':'SEAT/CUPRA','cupra':'SEAT/CUPRA','seat/cupra':'SEAT/CUPRA','skoda':'Škoda'}
def parse_brands(s):
    s=str(s or '')
    out=[]
    for pRaw in re.split(r',(?![^\[]*\])',s):
        pRaw=pRaw.strip()
        m=re.search(r'\[([^\]]*)\]',pRaw)
        tag=m.group(1) if m else None
        b=re.sub(r'\[[^\]]*\]','',pRaw)
        b=re.sub(r'\(.*?\)','',b).strip();b=re.sub(r'\s+',' ',b)
        if b and b.lower()!='nan':
            out.append((ALIAS.get(b.lower(),b),tag))
    return out
capAll={};capVer={}
for r in range(hdr+1,ws.max_row+1):
    mk=str(ws.cell(r,4).value or '').strip()
    if mk not in ('CZ','SK','CH','AT'):continue
    seen=set()
    for b,tag in parse_brands(ws.cell(r,7).value):
        if b in seen:continue
        seen.add(b)
        capAll.setdefault(mk,Counter())[b]+=1
        if tag and 'S' in [t.strip() for t in tag.split(',')]:
            capVer.setdefault(mk,Counter())[b]+=1
rs=wb['Research Status']
off={}
for r in range(2,rs.max_row+1):
    mk=str(rs.cell(r,1).value or '');b=str(rs.cell(r,2).value or '')
    b=ALIAS.get(b.lower(),b)
    tot=rs.cell(r,3).value;st=str(rs.cell(r,6).value or '')
    if mk and b and isinstance(tot,(int,float)) and tot:
        off[(mk,b)]=(int(tot),st)
if 'Completeness' in wb.sheetnames: del wb['Completeness']
cs=wb.create_sheet('Completeness',index=2)
HDRF=PatternFill('solid',fgColor='023F40');HF=Font(color='FFFFFF',bold=True)
GREEN=PatternFill('solid',fgColor='C6EFCE');AMBER=PatternFill('solid',fgColor='FFEB9C')
RED=PatternFill('solid',fgColor='FFC7CE');GREY=PatternFill('solid',fgColor='EDEDED')
cs['A1']='Data completeness — verified sales outlets vs official network size'
cs['A1'].font=Font(bold=True,size=14,color='023F40')
cs['A2']='Coverage & bar = locations with verified [S] sales tag / official total. "DB any" also counts legacy/untagged and service-only mentions. Denominators: verified officials or estimates (see Research Status).'
cs['A2'].font=Font(size=9,color='808080')
row=4;chart_anchors=[]
for mk,label in [('CZ','Czech Republic'),('SK','Slovakia'),('CH','Switzerland'),('AT','Austria')]:
    cs.cell(row,1).value=label;cs.cell(row,1).font=Font(bold=True,size=12,color='023F40')
    row+=1
    for j,h in enumerate(['Brand','Verified sales [S]','Official / est.','DB any mention','Coverage (verified)','Status','Progress']):
        c=cs.cell(row,1+j);c.value=h;c.fill=HDRF;c.font=HF
    row+=1
    table_start=row
    items=[]
    for (m,b),(tot,st) in off.items():
        if m!=mk:continue
        items.append((b,capVer.get(mk,{}).get(b,0),capAll.get(mk,{}).get(b,0),tot,st))
    items.sort(key=lambda x:-x[3])
    for b,cv,ca,tot,st in items:
        cov=cv/tot*100
        bar_n=min(20,round(min(cov,100)/5))
        cs.cell(row,1).value=b;cs.cell(row,2).value=cv;cs.cell(row,3).value=tot;cs.cell(row,4).value=ca
        cs.cell(row,5).value=f'{cov:.0f}%'
        cs.cell(row,6).value=('verified' if 'verified' in st else ('partial' if 'partial' in st else 'estimate'))
        bar=cs.cell(row,7);bar.value='▓'*bar_n+'░'*(20-bar_n)
        bar.font=Font(name='Consolas',size=9,color=('2C7A4B' if cov>=80 else ('B8860B' if cov>=50 else 'C00000')))
        cs.cell(row,5).fill=GREEN if cov>=80 else (AMBER if cov>=50 else RED)
        if 'verified' not in st: cs.cell(row,6).fill=GREY
        row+=1
    n=min(12,len(items))
    if n>=3:
        ch=BarChart();ch.type='col';ch.title=f'{label} — verified sales outlets vs official (top {n})'
        ch.height=7;ch.width=22;ch.gapWidth=60;ch.overlap=-10
        data=Reference(cs,min_col=2,max_col=3,min_row=table_start-1,max_row=table_start-1+n)
        cats=Reference(cs,min_col=1,min_row=table_start,max_row=table_start-1+n)
        ch.add_data(data,titles_from_data=True);ch.set_categories(cats)
        ch.series[0].graphicalProperties.solidFill='00CD55'
        ch.series[1].graphicalProperties.solidFill='B9C3CA'
        ch.y_axis.title='outlets';ch.legend.position='b'
        chart_anchors.append((ch,f'I{table_start-1}'))
    row+=2
for ch,a in chart_anchors:cs.add_chart(ch,a)
for col,w in [('A',22),('B',16),('C',13),('D',14),('E',16),('F',10),('G',24)]:
    cs.column_dimensions[col].width=w
wb.save(p)
# snapshot
tot=0
for mk in ('CZ','SK','CH','AT'):
    items=[(b,capVer.get(mk,{}).get(b,0),t) for (m,b),(t,st) in off.items() if m==mk]
    ge80=sum(1 for b,c0,t in items if c0/t>=0.8)
    print(mk,f'{ge80}/{len(items)} brands >=80% verified')
cnt=sum(1 for r in range(hdr+1,ws.max_row+1) if str(ws.cell(r,4).value) in ('CZ','SK','CH','AT'))
print('total locations:',cnt)
