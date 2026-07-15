// ================ travel-time engine (JS port of Phase 1 engine.py) ================
const ENG=(()=>{
 const ids=Object.values(GRAPH.nodes);
 const NN=ids.length;
 const NLAT=new Float64Array(NN),NLON=new Float64Array(NN);
 const NPOP=new Float64Array(NN);const NKEY=new Array(NN);
 for(const k in GRAPH.nodes){const v=GRAPH.nodes[k];NLAT[v.id]=v.lat;NLON[v.id]=v.lon;NPOP[v.id]=v.pop||0;NKEY[v.id]=k;}
 const ADJ=Array.from({length:NN},()=>[]);
 for(const[a,b,w]of GRAPH.edges){ADJ[a].push([b,w]);ADJ[b].push([a,w]);}
 function havKm(la1,lo1,la2,lo2){const dy=(la2-la1)*111.32,dx=(lo2-lo1)*111.32*Math.cos((la1+la2)/2*Math.PI/180);return Math.hypot(dx,dy);}
 const QS=52,QW=1.35,QCAP=45;
 function links(lat,lon){
  const c=[];for(let i=0;i<NN;i++)c.push([havKm(lat,lon,NLAT[i],NLON[i]),i]);
  c.sort((a,b)=>a[0]-b[0]);const out=[];
  for(let k=0;k<4;k++){const[d,i]=c[k];if(d>QCAP&&out.length)break;out.push([i,d*QW/QS*60]);}
  return out.length?out:[[c[0][1],c[0][0]*QW/QS*60]];}
 // binary-heap multi-source dijkstra
 function dijkstra(sources){
  const dist=new Float64Array(NN).fill(Infinity);
  const hN=new Int32Array(NN+8),hD=new Float64Array(NN+8);let hs=0;
  function push(n,d){let i=hs++;hN[i]=n;hD[i]=d;
   while(i>0){const p=(i-1)>>1;if(hD[p]<=hD[i])break;
    [hN[p],hN[i]]=[hN[i],hN[p]];[hD[p],hD[i]]=[hD[i],hD[p]];i=p;}}
  function pop(){const n=hN[0],d=hD[0];hs--;hN[0]=hN[hs];hD[0]=hD[hs];let i=0;
   for(;;){const l=2*i+1,r=l+1;let m=i;
    if(l<hs&&hD[l]<hD[m])m=l;if(r<hs&&hD[r]<hD[m])m=r;if(m===i)break;
    [hN[m],hN[i]]=[hN[i],hN[m]];[hD[m],hD[i]]=[hD[i],hD[m]];i=m;}
   return[n,d];}
  for(const[n,d]of sources)if(d<dist[n]){dist[n]=d;push(n,d);}
  while(hs){const[u,d]=pop();if(d>dist[u])continue;
   for(const[v,w]of ADJ[u]){const nd=d+w;if(nd<dist[v]){dist[v]=nd;push(v,nd);}}}
  return dist;}
 // demand municipalities: map to graph node ids + region weight
 const REGC=[
  ['CH','ZH',47.41,8.66],['CH','BE',46.83,7.60],['CH','LU',47.07,8.20],['CH','UR',46.77,8.63],
  ['CH','SZ',47.06,8.75],['CH','OW',46.85,8.20],['CH','NW',46.93,8.40],['CH','GL',47.00,9.07],
  ['CH','ZG',47.16,8.53],['CH','FR',46.72,7.05],['CH','SO',47.30,7.60],['CH','BS',47.56,7.59],
  ['CH','BL',47.45,7.70],['CH','SH',47.72,8.62],['CH','AR',47.37,9.30],['CH','AI',47.32,9.42],
  ['CH','SG',47.30,9.30],['CH','GR',46.70,9.60],['CH','AG',47.40,8.15],['CH','TG',47.57,9.05],
  ['CH','TI',46.20,8.90],['CH','VD',46.60,6.55],['CH','VS',46.20,7.50],['CH','NE',47.00,6.85],
  ['CH','GE',46.22,6.13],['CH','JU',47.35,7.15],
  ['CZ','Prague',50.08,14.44],['CZ','Central Bohemian',49.95,14.60],['CZ','South Bohemian',49.00,14.50],
  ['CZ','Plzeň',49.60,13.30],['CZ','Karlovy Vary',50.15,12.80],['CZ','Ústí nad Labem',50.55,13.90],
  ['CZ','Liberec',50.75,15.05],['CZ','Hradec Králové',50.30,15.90],['CZ','Pardubice',49.95,16.10],
  ['CZ','Vysočina',49.40,15.70],['CZ','South Moravian',49.00,16.70],['CZ','Olomouc',49.70,17.20],
  ['CZ','Zlín',49.20,17.80],['CZ','Moravian-Silesian',49.85,18.20],
  ['SK','Bratislava Region',48.20,17.15],['SK','Trnava Region',48.40,17.60],['SK','Trenčín Region',48.90,18.10],
  ['SK','Nitra Region',48.20,18.20],['SK','Žilina Region',49.20,19.00],['SK','Banská Bystrica Region',48.60,19.30],
  ['SK','Prešov Region',49.10,21.30],['SK','Košice Region',48.70,21.30],
  ['AT','Wien',48.21,16.37],['AT','Niederösterreich',48.30,15.80],['AT','Oberösterreich',48.20,14.00],
  ['AT','Steiermark',47.20,15.30],['AT','Kärnten',46.70,14.10],['AT','Salzburg',47.60,13.10],
  ['AT','Tirol',47.25,11.40],['AT','Vorarlberg',47.30,9.70],['AT','Burgenland',47.60,16.50]];
 const SCALE={CZ:1/0.605,SK:1/0.518,CH:1/0.475,AT:1/0.621};
 const DM=MUNIS.map(m=>{
  const key=m.name+'|'+m.c;const node=GRAPH.nodes[key];
  let best=1e9,reg=1;
  for(const[cc,r,la,lo]of REGC){if(cc!==m.c)continue;
   const d=havKm(m.lat,m.lon,la,lo);if(d<best){best=d;reg=(WEIGHTS[cc]&&WEIGHTS[cc][r])||1;}}
  return{...m,node:node?node.id:null,w:m.pop*SCALE[m.c],rw:reg};});
 return{links,dijkstra,DM,havKm,NLAT,NLON,NN};})();
