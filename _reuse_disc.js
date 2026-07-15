# -*- coding: utf-8 -*-
"""prep_v5.py: parse merged Excel -> locations_v5.json / groups already done separately or here."""
import pandas as pd, json, re, math, sys

f=sys.argv[1] if len(sys.argv)>1 else '/mnt/user-data/uploads/CZ_SK_CH_Dealership_Overview_v3_merged.xlsx'
def S(v):
    v='' if pd.isna(v) else str(v).strip()
    return '' if v.lower()=='nan' else v
g=pd.read_excel(f,sheet_name='Dealership Groups',header=6).dropna(subset=['Name'])
def own_class(o):
    o=o.lower()
    if 'oem-captive' in o or 'oem captive' in o: return 'OEM-captive'
    if 'family' in o or 'private' in o: return 'Private / Family'
    if 'subsidiary' in o or 'public' in o or 'international' in o or 'plc' in o: return 'International group'
    return 'Other'
groups=[{'name':S(r['Name']),'market':S(r['Market']),'hq':S(r.get('HQ')),
  'own':own_class(S(r['Ownership type'])),'ownRaw':S(r['Ownership type']),
  'access':S(r.get('Access / Existing Relationship')),'comment':S(r.get('Comment / Remark')),
  'outlets':S(r.get('No. Outlets')),'rev':S(r.get('Revenue (est)')),'sales':S(r.get('Sales Volume (estimates 2025)')),
  'brands':S(r.get('Brand portfolio')),
  'cn':S(r['Chinese brands?']).lower().startswith('yes'),'cnDetail':S(r['Chinese brands?'])} for _,r in g.iterrows()]
gmeta={x['name']:x for x in groups}
gkeys=list(gmeta)
def match_group(n):
    n=n.strip()
    if n in gmeta: return n
    for k in gkeys:
        if n in k or k in n: return k
    nf=n.split()[0].lower()
    for k in gkeys:
        if nf==k.split()[0].lower(): return k
    return None

GAZ=json.load(open('gazetteer_v5.json'))
GAZL={k.lower():v for k,v in GAZ.items()}
GAZ_BY_LEN=sorted([k for k in GAZ if len(k)>=4],key=len,reverse=True)
DG=json.load(open('district_gazetteer.json')); DIST=DG['districts']; PSC=DG['psc_praha']
DASH=r'\s*[-\u2013/]\s*'
CANT=r'(ZH|BE|LU|UR|SZ|OW|NW|GL|ZG|FR|SO|BS|BL|SH|AR|AI|SG|GR|AG|TG|TI|VD|VS|NE|GE|JU|FL)'
def clean(c):
    c=re.sub(r'\s+'+CANT+r'$','',c)
    c=re.sub(r'\s+a\.\s?[AdMR]\..*$','',c)
    c=re.sub(r'\s+u\s+\S+$','',c)
    c=re.sub(r'\s+(am|an der|bei|b\.|im|ob|nad|pod|pri|v)\s.*$','',c,flags=re.I)
    return c.strip()
WPLZ=DG.get('plz_wien',{})
GAZM=json.load(open('gazetteer_mkt.json'))
BBOX={'CZ':(48.5,12.0,51.1,18.9),'SK':(47.7,16.8,49.7,22.6),'CH':(45.7,5.9,47.9,10.6),'AT':(46.3,9.4,49.1,17.2)}
def inbox(mk,la,lo):
    s,w,n,e=BBOX[mk];return s<=la<=n and w<=lo<=e
ATREF={'1':(48.21,16.37),'2':(48.2,16.4),'3':(48.2,15.6),'4':(48.2,14.3),'5':(47.7,13.1),
 '6':(47.25,10.9),'7':(47.6,16.4),'8':(47.1,15.4),'9':(46.7,14.0)}
def resolve(city,address,mk=None):
    a=str(address)
    _plzref=None
    if mk=='AT':
        _m=re.search(r'\b([1-9])\d{3}\s',a)
        if _m:_plzref=ATREF[_m.group(1)]
    if 'Wien' in a or 'Wien' in str(city):
        mw=re.search(r'\b(1[0-2]\d0)\b',a)
        if mw and WPLZ.get(mw.group(1)): return WPLZ[mw.group(1)][0],WPLZ[mw.group(1)][1],'district'
    m=re.search(r'\b1(\d)0\s?\d\d\s',a)
    if m and PSC.get(m.group(1)): return PSC[m.group(1)][0],PSC[m.group(1)][1],'district'
    for txt in (a,str(city)):
        for k,v in DIST.items():
            base=k.split('(')[0].strip()
            if base and base in txt: return v[0],v[1],'district'
    cands=[]
    m=re.search(r'\d{3}\s?\d{2}\s+([^,]+?)\s*$',a) or re.search(r'\b\d{4}\s+([^,]+?)\s*$',a)
    if m:
        raw=m.group(1).strip(); c=clean(raw)
        cands+= [raw,c]+re.split(DASH,c)[:1]+[re.sub(r'\s*\d+\s*$','',re.split(DASH,c)[0]).strip()]
        if re.match(r'^Praha\b',c): cands.append('Praha')
        if re.match(r'^Bratislava\b',c): cands.append('Bratislava')
        if re.match(r'^Brno\b',c): cands.append('Brno')
    m2=re.search(r',\s*([^,\d][^,]*?)\s*$',a)
    if m2:
        c2=clean(m2.group(1)); cands+=[c2]+re.split(DASH,c2)[:1]
    c3=str(city).strip(); cands+=[c3]+re.split(DASH,c3)[:1]+[clean(c3)]
    # expansion passes
    ext=[]
    for c in list(cands):
        c=(c or '').replace('\xa0',' ').strip()
        if not c:continue
        ext.append(c)
        ext.append(re.sub(r'\s*n[./]\s*',' nad ',c))
        ext.append(c.replace(' ','-'))
        ext.append(re.sub(r'St\.\s*',u'St. ',c))
        ext.append(re.sub(r'\s+[IVX]+$','',c))                       # Klatovy III
        ext.append(re.sub(r'\s*\d+\s*$','',c))
        for part in re.split(DASH,c): ext.append(part.strip())
        ext.append(clean(c))
    # also every comma segment of the address
    for seg in str(address).replace('\xa0',' ').split(','):
        seg=clean(re.sub(r'^[\s\d/.]+|[\s\d/.]+$','',seg.strip()))
        if seg and not re.search(r'\d',seg): ext.append(seg)
    def ok(v):
        if v is None: return None
        if mk is not None and not inbox(mk,v[0],v[1]): return None
        if _plzref is not None:
            if math.hypot((v[0]-_plzref[0])*111,(v[1]-_plzref[1])*78)>190: return None
        return v
    for c in ext:
        c=c.strip()
        if not c:continue
        if mk=='AT' and _plzref is not None:
            _m2=re.search(r'\b([1-9])\d{3}\s',a)
            if _m2 and (c+'|AT'+_m2.group(1)) in GAZM:
                v=GAZM[c+'|AT'+_m2.group(1)];return v[0],v[1],'city'
        if mk and (c+'|'+mk) in GAZM:
            v=GAZM[c+'|'+mk];return v[0],v[1],'city'
        v=ok(GAZ.get(c)) or ok(GAZL.get(c.lower())) or ok(GAZ.get(c.title()))
        if v is None:
            u=c.lower().replace('ae','ä').replace('oe','ö').replace('ue','ü')
            v=ok(GAZL.get(u))
        if v is not None: return v[0],v[1],'city'
    # last resort: any gazetteer town named inside the location name / address
    hay=str(address).replace('\xa0',' ')
    for k in GAZ_BY_LEN:
        if re.search(r'(?<![\wäöüÄÖÜ])'+re.escape(k)+r'(?![\wäöüÄÖÜ])',hay,flags=re.I):
            v=GAZ[k]
            if (mk is None or inbox(mk,v[0],v[1])) and (_plzref is None or math.hypot((v[0]-_plzref[0])*111,(v[1]-_plzref[1])*78)<=190):
                return v[0],v[1],'city'
    return None,None,None

loc=pd.read_excel(f,sheet_name='Locations',header=None)
hdr=loc.index[loc[1].astype(str).str.strip()=='#'][0]
loc=loc.iloc[hdr+1:,1:8]; loc.columns=['num','group','market','city','address','brands','dtype']
loc=loc[loc['market'].astype(str).str.strip().isin(['CZ','SK','CH','AT'])]
BRAND_MAP={'vw':'Volkswagen','škoda':'Škoda','skoda':'Škoda','vw commercial vehicles':'VW Commercial Vehicles',
 'vw lcv':'VW Commercial Vehicles','vw commercial':'VW Commercial Vehicles','vw nutzfahrzeuge':'VW Commercial Vehicles',
 'mercedes':'Mercedes-Benz','citroen':'Citroën','van':'Mercedes-Benz Vans','cupra':'CUPRA','seat/cupra':'SEAT/CUPRA'}
CN_BRANDS={'byd','mg','omoda','jaecoo','gwm','ora','wey','leapmotor','xpeng','nio','aiways','dfsk','maxus',
 'lynk & co','lynk&co','zeekr','hongqi','chery','dongfeng','jac','seres','voyah','skywell','swm','baic','forthing','exeed','geely','kgm'}
def nb(sv):
    out=[];tags={}
    for b in re.split(r',(?![^\[]*\])',str(sv)):   # commas outside [..] only
        b=b.strip()
        mt=re.search(r'\[([^\]]*)\]',b)
        tag=mt.group(1).replace(' ','') if mt else None
        b=re.sub(r'\[[^\]]*\]','',b)
        b=re.sub(r'\(.*?\)','',b.strip()).strip(); b=re.sub(r'\s+',' ',b)
        if not b:continue
        b=BRAND_MAP.get(b.lower(),b)
        if b not in out:out.append(b)
        if tag:tags[b]=tag
    return out,tags
out=[];seen={};miss=[];prec={'district':0,'city':0};stats={'group':0,'independent':0}
for i,(_,l) in enumerate(loc.iterrows()):
    dtype='independent' if 'ndependent' in str(l['dtype']) else 'group'
    la,lo,p=resolve(l['city'],l['address'],str(l['market']).strip())
    if la is None: miss.append((str(l['market']),str(l['city']),str(l['address']))); continue
    key=f'{la:.4f},{lo:.4f}';n=seen.get(key,0);seen[key]=n+1
    if n>0:
        ang=n*2.399963;r=0.0032*math.sqrt(n)
        la+=r*math.cos(ang);lo+=r*math.sin(ang)/math.cos(math.radians(la))
    brands,vtags=nb(l['brands'])
    gname=match_group(str(l['group'])) if dtype=='group' else None
    if dtype=='group' and gname:
        gm=gmeta[gname]
        rec_own,rec_cn,rec_cnd,rec_acc,rec_com=gm['own'],gm['cn'],gm['cnDetail'],gm['access'],gm['comment']
    else:
        gname=str(l['group']).strip();dtype='independent'
        rec_own='Independent'
        rec_cn=any(b.lower() in CN_BRANDS for b in brands)
        rec_cnd='Yes ('+', '.join(b for b in brands if b.lower() in CN_BRANDS)+')' if rec_cn else 'No'
        rec_acc,rec_com='',''
    prec[p]+=1;stats[dtype]+=1
    out.append({'id':i+1,'group':gname,'market':str(l['market']).strip(),'city':str(l['city']).strip(),
      'address':str(l['address']).strip(),'brands':brands,'lat':round(la,5),'lon':round(lo,5),
      'precision':p,'own':rec_own,'cn':rec_cn,'cnDetail':rec_cnd,
      'access':rec_acc,'comment':rec_com,'dtype':dtype,'vtags':vtags})
print(len(out),'located |',prec,'|',stats,'| missing:',len(miss))
from collections import Counter
print('miss by market:',Counter(m[0] for m in miss))
for m in miss[:40]:print('  !',m)
json.dump(out,open('locations_v5.json','w'),ensure_ascii=False)
json.dump(groups,open('groups_v5.json','w'),ensure_ascii=False)
