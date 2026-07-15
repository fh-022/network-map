# -*- coding: utf-8 -*-
"""at_ingest_v2.py — parse the three AT v2 result files, dedupe, append to workbook."""
import re, unicodedata, openpyxl
from collections import OrderedDict

UP='/mnt/user-data/uploads/'
WB='/mnt/user-data/outputs/CZ_SK_CH_Dealership_Overview_v3_merged_with_research_status.xlsx'
TODAY='2026-07-13'

def cells_of(line):
    return [c.strip().replace('\\&','&').replace('\\#','#') for c in line.strip().strip('|').split('|')]

def street_key(street):
    s=unicodedata.normalize('NFKD',street).encode('ascii','ignore').decode().lower()
    m=re.search(r'([a-z][a-z .\-]+?)\s*(\d+)',s)
    return (re.sub(r'[^a-z]','',m.group(1)),m.group(2)) if m else (re.sub(r'[^a-z]','',s)[:14],'')

rows=OrderedDict()  # street_key+psc -> row dict
def put(name,company,street,psc_city,bl,brands,tags,group,src,prio):
    m=re.match(r'(\d{4})\s+(.*)',psc_city.strip())
    psc,city=(m.group(1),m.group(2)) if m else ('',psc_city.strip())
    k=street_key(street)+(psc,)
    r=rows.get(k)
    if r is None:
        rows[k]={'name':name,'company':company,'street':street,'psc':psc,'city':city,'bl':bl,
                 'brands':OrderedDict((b,t) for b,t in zip(brands,tags)),'group':group,'src':[src],'prio':prio}
    else:
        # merge: higher prio wins name/group/company; brands union (explicit beats generic VW Group)
        if prio>r['prio']:
            r['name'],r['company'],r['group'],r['prio']=name,company,group,prio
        if brands!=['VW Group'] and 'VW Group' in r['brands'] and prio>=r['prio']:
            del r['brands']['VW Group']
        if not (brands==['VW Group'] and any(b!='VW Group' for b in r['brands'])):
            for b,t in zip(brands,tags): r['brands'].setdefault(b,t)
        if src not in r['src']: r['src'].append(src)

BRAND_MAP={'vw':'Volkswagen','škoda':'Škoda','skoda':'Škoda','seat':'SEAT/CUPRA','cupra':'SEAT/CUPRA',
 'seat/cupra':'SEAT/CUPRA','seat, cupra':'SEAT/CUPRA','fiat professional':'Fiat','abarth':'Abarth'}
def nbrand(b):
    b=re.sub(r'\(.*?\)','',b).strip()
    if not b or b.lower() in ('all brands',''):return None
    return BRAND_MAP.get(b.lower(),b)

# ---- P8b: Porsche Bank Händlerverzeichnis (prio 1) ----
t=open(UP+'GUARD_BLOCK__included_in_every_prompt__CRITICAL_RU.md',encoding='utf-8').read()
n8=0
for line in t.splitlines():
    if not line.startswith('|'):continue
    c=cells_of(line)
    if len(c)<8 or c[0] in ('#','\\#',':--') or not c[0].strip('\\# ').isdigit():continue
    ticks=re.search(r'×\s*(\d+)',c[6])
    tick_n=ticks.group(1) if ticks else '?'
    src=f'Porsche Bank Händlerverzeichnis PDF (porschebank.at, {c[7]}), {tick_n} of 5 VW-Group brands ticked, {TODAY}'
    grp='Porsche Inter Auto (Porsche Holding)' if 'Porsche Inter Auto' in c[2] else c[2]
    mcity=re.match(r'\d{4}\s+(.*)',c[4].strip())
    dispname=c[1]+(' – '+mcity.group(1) if mcity else '')
    put(dispname,c[2],c[3],c[4],c[5],['VW Group'],['S,SV'],grp,src,1)
    n8+=1
print('P8b rows:',n8)

# ---- P10b: group Standorte (prio 3, explicit brands) ----
t=open(UP+'Importer-owned_retail__amp__dealer-group_networks.md',encoding='utf-8').read()
sections=re.split(r'\n## ',t)
GRPNAME={'Denzel':'Denzel Gruppe','Pappas':'Pappas Gruppe','Wiesenthal':'Merbag (ex-Wiesenthal)',
 'Porsche Inter Auto':'Porsche Inter Auto (Porsche Holding)','Eisner':'Eisner Auto','AutoFrey':'AutoFrey'}
n10=0
for sec in sections[1:]:
    title=sec.split('\n')[0]
    grp=next((v for k,v in GRPNAME.items() if k in title),None)
    if grp is None:continue
    dom=re.search(r'—\s*(\S+)',title)
    dom=dom.group(1) if dom else 'group website'
    for line in sec.splitlines():
        if not line.startswith('|'):continue
        c=cells_of(line)
        if len(c)<7 or c[0].startswith(':--') or c[0]=='Location name':continue
        svc=c[5].lower()
        s='S' in ('S' if 'verkauf' in svc else '')+('' if 'only' in svc else '')
        sales=('verkauf' in svc) and ('only' not in svc)
        tag='S,SV' if sales else 'SV'
        brands=[];tags=[]
        for braw in re.split(r'[,;](?![^(]*\))',c[4]):
            svnote='service' in braw.lower() and '(' in braw
            b=nbrand(braw)
            if b is None:continue
            brands.append(b);tags.append('SV' if (svnote or not sales) else tag)
        if not brands:continue
        src=f'{grp} Standorte ({dom}), {TODAY}'
        put(c[0],grp,c[1],c[2],c[3],brands,tags,grp,src,3)
        n10+=1
print('P10b rows:',n10)

# ---- P9b: Mazda association 2019 (prio 2) ----
t=open(UP+'Brand_dealer_association_member_lists__Toyota__Kia.md',encoding='utf-8').read()
n9=0
for line in t.splitlines():
    if not line.startswith('|'):continue
    c=cells_of(line)
    if len(c)<6 or c[0].startswith(':--') or c[0] in ('Dealer name','Association'):continue
    if 'PDF p.' not in c[5]:continue
    svp='servicepartner' in c[0].lower()
    tag='SV' if svp else 'S,SV'
    src=f'Mazda Händlerverband Mitgliederliste 2019 PDF (mazdahaendlerverband.at, {c[5]}) — dated 2019, {TODAY}'
    put(c[0],c[1],c[2],c[3],c[4],['Mazda'],[tag],c[1],src,2)
    n9+=1
print('P9b rows:',n9)

# ---- P12b: automobile.at brand index (prio 1, secondary source) ----
t=open(UP+'remaining_brands_via_automobile_at_brand_index__se.md',encoding='utf-8').read()
n12=0
for sec in re.split(r'\n## ',t)[1:]:
    title=sec.split('\n')[0]
    brand=title.split('—')[0].strip()
    b=nbrand(brand)
    if b is None or 'TOTAL' in brand:continue
    for line in sec.splitlines():
        if not line.startswith('|'):continue
        c=cells_of(line)
        if len(c)<5 or c[0].startswith(':--') or c[0] in ('Dealer name','Brand'):continue
        if not re.match(r'\d{4}\s',c[2].strip()):continue
        name=re.sub(r'\s*\(secondary source\)','',c[0]).strip()
        src=f'automobile.at brand index (secondary source), {TODAY}'
        put(name,name,c[1],c[2],c[3],[b],['S'],name,src,1)
        n12+=1
print('P12b rows:',n12)
print('unique locations after dedupe:',len(rows))

# ---- canonical group assignment ----
from collections import Counter
comp_count=Counter(d['company'] for d in rows.values())
GROUP_SET=set(GRPNAME.values())
auto_groups={}
for k,d in rows.items():
    if d['group'] in GROUP_SET:continue
    if comp_count[d['company']]>=3 and len(d['company'])>6:
        d['group']=d['company']
        auto_groups.setdefault(d['company'],0)
        auto_groups[d['company']]+=1
print('auto-derived AT groups (>=3 locations):',len(auto_groups))

# ---- append to workbook ----
wb=openpyxl.load_workbook(WB)
ws=wb['Locations']
hdr=[r for r in range(1,15) if str(ws.cell(r,2).value).strip()=='#'][0]
# next number
mx=0
for r in range(hdr+1,ws.max_row+1):
    v=ws.cell(r,2).value
    if isinstance(v,(int,float)):mx=max(mx,int(v))
# drop pre-existing AT rows (idempotent re-run)
del_rows=[r for r in range(hdr+1,ws.max_row+1) if str(ws.cell(r,4).value).strip()=='AT']
for r in reversed(del_rows):ws.delete_rows(r)
r=ws.max_row+1
for k,d in rows.items():
    mx+=1
    bstr=', '.join(f'{b} [{t}]' for b,t in d['brands'].items())
    ws.cell(r,2).value=mx
    ws.cell(r,3).value=d['group']
    ws.cell(r,4).value='AT'
    ws.cell(r,5).value=d['name']
    ws.cell(r,6).value=f"{d['street']}, {d['psc']} {d['city']}".strip(', ')
    ws.cell(r,7).value=bstr
    ws.cell(r,8).value='Group' if (d['group'] in GRPNAME.values() or comp_count[d['company']]>=3 and d['group']==d['company']) else 'Independent'
    ws.cell(r,9).value=TODAY
    ws.cell(r,10).value=' + '.join(d['src'][:2])+' (NEW)'
    r+=1
print('appended',len(rows),'AT rows')

# ---- Research Status AT rows ----
rs=wb['Research Status']
at_status=[
 ('AT','VW Group (all brands)',258,'Porsche Bank Händlerverzeichnis PDF — full enumeration; per-brand split not decodable from PDF ticks',TODAY,'verified (as group)','P8b'),
 ('AT','Mazda',47,'Mazda Händlerverband Mitgliederliste 2019 (35 full + 7 sub + 5 service) — DATED 2019',TODAY,'partial (2019)','P9b'),
 ('AT','Mercedes-Benz',None,'Pappas 21 + Merbag/ex-Wiesenthal 6 locations captured; AVB association has no public list','','partial (groups only)','P9b/P10b'),
 ('AT','Toyota',None,'toyota-hv.at 403; importer statement ~110 Toyota/Lexus partners (earlier session, credible total, no enumeration)','','open (total only)','P9b'),
 ('AT','Kia',None,'kia-hv.at offline; member list was login-only','','open','P9b'),
 ('AT','Nissan',None,'No public association site','','open','P9b'),
 ('AT','Hyundai',None,'Denzel importer; Denzel retail locations captured; full dealer network pending','','partial (Denzel retail)','P10b'),
 ('AT','BMW',None,'Denzel BMW/MINI retail locations captured; full network pending','','partial (Denzel retail)','P10b'),
]
have={(str(rs.cell(rr,1).value),str(rs.cell(rr,2).value)):rr for rr in range(2,rs.max_row+1)}
for mk,b,tot,srcs,dt,st,pr in at_status:
    rr=have.get((mk,b)) or rs.max_row+1
    rs.cell(rr,1).value=mk;rs.cell(rr,2).value=b
    if tot:rs.cell(rr,3).value=tot
    rs.cell(rr,4).value=srcs;rs.cell(rr,5).value=dt;rs.cell(rr,6).value=st
    rs.cell(rr,10).value=pr;rs.cell(rr,11).value=f'yes ({TODAY})';rs.cell(rr,12).value='yes'
# ---- Dealership Groups sheet: AT rows ----
gs=wb['Dealership Groups']
GHDR=7
# find column letters by header names
heads={str(gs.cell(GHDR,c).value):c for c in range(1,20)}
def gc(name):return heads.get(name)
# delete existing AT group rows (idempotent)
delg=[r for r in range(GHDR+1,gs.max_row+1) if str(gs.cell(r,gc('Market')).value).strip()=='AT']
for r in reversed(delg):gs.delete_rows(r)
loc_count=Counter()
for d in rows.values():
    if d['group']:loc_count[d['group']]+=1
CURATED={
 'Porsche Inter Auto (Porsche Holding)':dict(hq='Salzburg, Austria',own='OEM-captive / Subsidiary (Porsche Holding Salzburg / VW Group)',
   brands='VW, Audi, SEAT, CUPRA, Škoda, Porsche',cn='no',rev='part of Porsche Holding Salzburg (€30B+ group)',
   com='Largest AT retail group; VW-Group brands only'),
 'Denzel Gruppe':dict(hq='Wien, Austria',own='Private/Family (Wolfgang Denzel Auto AG)',
   brands='BMW, MINI, Hyundai, Mitsubishi, MG, BYD, Maxus, Fiat, Alfa Romeo, Jeep, Land Rover, Volvo',
   cn='Yes (MG, BYD, Maxus — Denzel is AT importer for these)',rev='~€1.3B (2023)',
   com='Importer for Hyundai, Mitsubishi, MG, BYD, Maxus + multi-brand retail'),
 'Pappas Gruppe':dict(hq='Salzburg, Austria',own='Private/Family',brands='Mercedes-Benz (PW + Vans/Trucks)',
   cn='no',rev='~€1.9B (2023)',com='Dominant Mercedes-Benz retail network in AT'),
 'Merbag (ex-Wiesenthal)':dict(hq='Wien, Austria',own='International group (Merbag Holding, CH)',
   brands='Mercedes-Benz',cn='no',rev='',com='Took over Wiesenthal Vienna MB retail'),
 'Eisner Auto':dict(hq='Klagenfurt, Austria',own='Private/Family',brands='Opel, Mazda, MG, Ford, Fiat, Hyundai (multi-brand)',
   cn='Yes (MG)',rev='~€0.4B',com='Kärnten/Steiermark multi-brand group'),
 'AutoFrey':dict(hq='Salzburg, Austria',own='Private/Family',brands='VW Group + multi-brand',cn='no',rev='',com='Salzburg region'),
}
gr=gs.max_row+1
for gname,cnt in sorted(loc_count.items(),key=lambda x:-x[1]):
    if cnt<3 and gname not in CURATED:continue
    meta=CURATED.get(gname,dict(hq='Austria',own='Private/Family',brands='',cn='no',rev='',
        com=f'Auto-derived from AT dealer research ({cnt} locations)'))
    gs.cell(gr,gc('Name')).value=gname
    gs.cell(gr,gc('Market')).value='AT'
    gs.cell(gr,gc('HQ')).value=meta['hq']
    gs.cell(gr,gc('Ownership type')).value=meta['own']
    gs.cell(gr,gc('No. Outlets')).value=cnt
    if gc('Revenue (est)') and meta['rev']:gs.cell(gr,gc('Revenue (est)')).value=meta['rev']
    if gc('Brand portfolio'):gs.cell(gr,gc('Brand portfolio')).value=meta['brands']
    if gc('Chinese brands?'):gs.cell(gr,gc('Chinese brands?')).value=meta['cn']
    if gc('Comment / Remark'):gs.cell(gr,gc('Comment / Remark')).value=meta['com']
    gr+=1
print('AT groups written:',gr-(gs.max_row+1-(gr-gs.max_row-1)) if False else 'ok')

wb.save(WB)
print('workbook saved')
