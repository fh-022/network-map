// ================ PPT EXPORT (Colmobil master geometry) ================
const CI={petrol:'023F40',green:'00CD55',grey:'5F7382',light:'E7E6E6',warn:'C07A1E'};
const EX_DEFAULTS=[
 {id:'x1',name:'Current view',o:{base:true,dealers:'auto',places:true,areas:'off',gaps:false,cities:false,legend:true,kpi:true,title:''}},
 {id:'x2',name:'Places & coverage gaps',o:{base:true,dealers:'off',places:true,areas:'off',gaps:true,cities:true,legend:true,kpi:true,title:''}},
 {id:'x3',name:'Proposed network (schematic)',o:{base:true,dealers:'off',places:true,areas:'schematic',gaps:false,cities:true,legend:true,kpi:true,title:''}}];
WS.pptPresets=WS.pptPresets&&WS.pptPresets.length?WS.pptPresets:JSON.parse(JSON.stringify(EX_DEFAULTS));
WS.pptPresets.forEach(p=>p.o=Object.assign({heat:false,pop:false,frame:null,labStyle:'chip',labSize:'M'},p.o));
WS.pptChecked=WS.pptChecked||['x1'];
let exSel=WS.pptPresets[0].id;
function exP(){return WS.pptPresets.find(p=>p.id===exSel)||WS.pptPresets[0];}
const REGION_BOUNDS={CZ:[[48.55,12.05],[51.06,18.87]],SK:[[47.72,16.83],[49.62,22.58]],CH:[[45.81,5.95],[47.81,10.50]],AT:[[46.35,9.45],[49.05,17.20]]};
function caseBounds(){let s=90,w=180,n=-90,e=-180;
 C().markets.forEach(m=>{const b=REGION_BOUNDS[m];s=Math.min(s,b[0][0]);w=Math.min(w,b[0][1]);n=Math.max(n,b[1][0]);e=Math.max(e,b[1][1]);});
 return[[s,w],[n,e]];}
function frameLabel(f){if(!f)return'Current view';
 for(const k in REGION_BOUNDS){const b=REGION_BOUNDS[k];
  if(Math.abs(b[0][0]-f[0][0])<1e-6&&Math.abs(b[1][1]-f[1][1])<1e-6)return k;}
 return'Custom frame';}
function frameRectPx(f){ // container-px rect of geo frame in CURRENT view
 const p1=map.latLngToContainerPoint([f[1][0],f[0][1]]),p2=map.latLngToContainerPoint([f[0][0],f[1][1]]);
 return{x:Math.min(p1.x,p2.x),y:Math.min(p1.y,p2.y),w:Math.abs(p2.x-p1.x),h:Math.abs(p2.y-p1.y)};}
function fullRect(){const s=map.getSize();return{x:0,y:0,w:s.x,h:s.y};}
function tilesIdle(ms){return new Promise(res=>{
 const tl=BASES[baseName];let done=false;
 const fin=()=>{if(!done){done=true;tl.off('load',fin);res();}};
 tl.on('load',fin);setTimeout(fin,ms);});}
async function withFrame(f,fn){ // fit map to frame, run fn, restore
 if(!f)return fn(fullRect());
 const c0=map.getCenter(),z0=map.getZoom();
 map.fitBounds(f,{animate:false,padding:[6,6]});
 await tilesIdle(1800);
 const r=frameRectPx(f);
 const out=fn(r);
 map.setView(c0,z0,{animate:false});
 return out;}
function cropUrl(canvas,rect,scale){
 const full=fullRect();
 if(rect.x===0&&rect.y===0&&rect.w===full.w&&rect.h===full.h)return canvas.toDataURL('image/png');
 const c=document.createElement('canvas');c.width=rect.w*scale;c.height=rect.h*scale;
 c.getContext('2d').drawImage(canvas,rect.x*scale,rect.y*scale,rect.w*scale,rect.h*scale,0,0,rect.w*scale,rect.h*scale);
 return c.toDataURL('image/png');}
// ---- crop editor ----
const crop={r:null,asp:0};
function cropShow(){
 const s=map.getSize();
 let r=crop.r;
 if(!r){const f=exP().o.frame; r=f?frameRectPx(f):{x:s.x*.18,y:s.y*.2,w:s.x*.64,h:s.y*.6};}
 crop.r={x:Math.max(0,r.x),y:Math.max(0,r.y),w:Math.min(s.x,r.w),h:Math.min(s.y,r.h)};
 cropSync();$('cropOv').classList.add('on');$('cropBar').classList.add('on');}
function cropSync(){const r=crop.r,el=$('cropOv');
 el.style.left=r.x+'px';el.style.top=r.y+'px';el.style.width=r.w+'px';el.style.height=r.h+'px';}
function cropAspect(){if(!crop.asp)return;crop.r.h=crop.r.w/crop.asp;cropSync();}
(function(){
 const ov=$('cropOv');let drag=null;
 ov.addEventListener('pointerdown',e=>{
  e.preventDefault();e.stopPropagation();
  const h=e.target.classList.contains('hnd')?[...e.target.classList].find(c=>c.length===2):null;
  drag={h,sx:e.clientX,sy:e.clientY,r:{...crop.r}};ov.setPointerCapture(e.pointerId);});
 ov.addEventListener('pointermove',e=>{
  if(!drag)return;const dx=e.clientX-drag.sx,dy=e.clientY-drag.sy,r=drag.r,s=map.getSize();
  let nr={...r};
  if(!drag.h){nr.x=Math.min(Math.max(0,r.x+dx),s.x-r.w);nr.y=Math.min(Math.max(0,r.y+dy),s.y-r.h);}
  else{
   if(drag.h.includes('e'))nr.w=Math.max(60,r.w+dx);
   if(drag.h.includes('s'))nr.h=Math.max(40,r.h+dy);
   if(drag.h.includes('w')){nr.x=r.x+dx;nr.w=Math.max(60,r.w-dx);}
   if(drag.h.includes('n')){nr.y=r.y+dy;nr.h=Math.max(40,r.h-dy);}
   if(crop.asp)nr.h=nr.w/crop.asp;}
  crop.r=nr;cropSync();});
 ov.addEventListener('pointerup',()=>{drag=null;});
})();
$('cropAsp').onchange=e=>{crop.asp=+e.target.value;cropAspect();};
$('cropApply').onclick=()=>{
 const r=crop.r;
 const nw=map.containerPointToLatLng([r.x,r.y]),se=map.containerPointToLatLng([r.x+r.w,r.y+r.h]);
 exP().o.frame=[[se.lat,nw.lng],[nw.lat,se.lng]];save();
 $('cropOv').classList.remove('on');$('cropBar').classList.remove('on');
 exRender();$('exDlg').showModal();};
$('cropCancel').onclick=()=>{
 $('cropOv').classList.remove('on');$('cropBar').classList.remove('on');exRender();$('exDlg').showModal();};
// ---- capture helpers ----
function captureRegion(draw,scale){
 const size=map.getSize();
 const c=document.createElement('canvas');c.width=size.x*scale;c.height=size.y*scale;
 const ctx=c.getContext('2d');ctx.scale(scale,scale);
 draw(ctx,size);return c;}
function drawDomLayerOnto(ctx,el){
 const cr=map.getContainer().getBoundingClientRect();
 const r=el.getBoundingClientRect();
 try{ctx.drawImage(el,r.left-cr.left,r.top-cr.top,r.width,r.height);}catch(e){}}
function captureBasemap(scale,rect){
 let ok=false;
 const c=captureRegion((ctx,size)=>{
  ctx.fillStyle='#e8edf1';ctx.fillRect(0,0,size.x,size.y);
  const tl=BASES[baseName];
  if(tl&&tl._tiles)for(const k in tl._tiles){const t=tl._tiles[k];
   if(!t.el||!t.el.complete||!t.el.naturalWidth)continue;
   drawDomLayerOnto(ctx,t.el);ok=true;}
  const dim=WS.ui.dim||0;
  if(dim>0){ctx.fillStyle=`rgba(0,0,0,${dim/100})`;ctx.fillRect(0,0,size.x,size.y);}},scale);
 try{return{data:cropUrl(c,arguments[1]||fullRect(),scale),ok};}
 catch(e){return{data:null,ok:false};}}
function captureCanvasLayer(layer){ // DiscLayer instance currently on map
 if(!layer||!layer._c)return null;
 const c=captureRegion((ctx)=>drawDomLayerOnto(ctx,layer._c),2);
 return c.toDataURL('image/png');}
function renderVeilOffscreen(sites,T,rect){ // gaps veil independent of layer state
 const size=map.getSize();
 const c=document.createElement('canvas');c.width=size.x*2;c.height=size.y*2;
 const ctx=c.getContext('2d');ctx.scale(2,2);
 ctx.fillStyle='rgba(35,48,60,.42)';ctx.fillRect(0,0,size.x,size.y);
 if(sites.length){
  let src=[];for(const[la,lo]of sites)src=src.concat(ENG.links(la,lo));
  const dist=ENG.dijkstra(src);
  const mPP=40075016.686*Math.cos(map.getCenter().lat*Math.PI/180)/(256*Math.pow(2,map.getZoom()));
  const pxPerKm=1000/mPP;
  ctx.globalCompositeOperation='destination-out';ctx.fillStyle='#000';
  const disc=(la,lo,rkm)=>{const p=map.latLngToContainerPoint([la,lo]);
   ctx.beginPath();ctx.arc(p.x,p.y,Math.max(2,rkm*pxPerKm),0,6.2832);ctx.fill();};
  for(let i=0;i<ENG.NN;i++){const t=dist[i];if(t<=T)disc(ENG.NLAT[i],ENG.NLON[i],(T-t)/60*46);}
  for(const[la,lo]of sites)disc(la,lo,Math.min(T,22)*0.5);
  ctx.globalCompositeOperation='source-over';}
 return cropUrl(c,rect||fullRect(),2);}
function renderAreasOffscreen(places,T,rect){
 const size=map.getSize();
 const c=document.createElement('canvas');c.width=size.x*2;c.height=size.y*2;
 const ctx=c.getContext('2d');ctx.scale(2,2);
 const buf=document.createElement('canvas');buf.width=size.x;buf.height=size.y;
 const bctx=buf.getContext('2d');bctx.fillStyle='#'+CI.petrol;
 const mPP=40075016.686*Math.cos(map.getCenter().lat*Math.PI/180)/(256*Math.pow(2,map.getZoom()));
 const pxPerKm=1000/mPP;
 for(const p of places){
  const dist=ENG.dijkstra(ENG.links(p.lat,p.lon));
  for(let i=0;i<ENG.NN;i++){const t=dist[i];if(t<=T){
   const pt=map.latLngToContainerPoint([ENG.NLAT[i],ENG.NLON[i]]);
   bctx.beginPath();bctx.arc(pt.x,pt.y,Math.max(2,(T-t)/60*46*pxPerKm),0,6.2832);bctx.fill();}}
  const pt=map.latLngToContainerPoint([p.lat,p.lon]);
  bctx.beginPath();bctx.arc(pt.x,pt.y,Math.min(T,20)*0.5*pxPerKm,0,6.2832);bctx.fill();}
 ctx.globalAlpha=.22;ctx.drawImage(buf,0,0);
 return cropUrl(c,rect||fullRect(),2);}
function captureDensity(kind,rect){
 const layer=kind==='heat'?dealerHeat:popHeat;
 const wasOn=map.hasLayer(layer);
 if(kind==='heat'){layer.o.bwKm=state.hBw;layer.o.opacity=state.hOp;
  layer.setData(filtered.map(l=>[l.lat,l.lon,1]));}
 else{layer.o.bwKm=state.pBw;layer.o.opacity=state.pOp;layer.o.gamma=.42;
  layer.setData(ENG.DM.filter(m=>C().markets.includes(m.c)).map(m=>[m.lat,m.lon,m.w*(state.weight?m.rw:1)]));}
 if(!wasOn)layer.addTo(map);
 layer.redraw();
 const c=captureRegion((ctx)=>drawDomLayerOnto(ctx,layer._c),2);
 const url=cropUrl(c,rect||fullRect(),2);
 if(!wasOn)map.removeLayer(layer);
 return url;}
function dotsImage(rect){
 const c=captureRegion((ctx)=>{
  for(const l of filtered){const p=map.latLngToContainerPoint([l.lat,l.lon]);
   ctx.beginPath();ctx.arc(p.x,p.y,3.4,0,6.2832);
   ctx.fillStyle=colorFor(l);ctx.fill();ctx.lineWidth=1;ctx.strokeStyle='#fff';ctx.stroke();}},2);
 return cropUrl(c,rect||fullRect(),2);}
// ---- geometry mapping ----
function slideGeom(rect){
 const MAPY=1.62,MAPH=5.15,MAXW=12.19,X0=0.57;
 let w=MAPH*rect.w/rect.h,h=MAPH;
 if(w>MAXW){w=MAXW;h=w*rect.h/rect.w;}
 return{X:X0,Y:MAPY,W:w,H:h,rect};}
function ll2in(g,lat,lon){
 const p=map.latLngToContainerPoint([lat,lon]);
 const rx=p.x-g.rect.x,ry=p.y-g.rect.y;
 return{x:g.X+rx/g.rect.w*g.W,y:g.Y+ry/g.rect.h*g.H,
  vis:rx>=0&&ry>=0&&rx<=g.rect.w&&ry<=g.rect.h};}
function kmToIn(g,km){
 const mPP=40075016.686*Math.cos(map.getCenter().lat*Math.PI/180)/(256*Math.pow(2,map.getZoom()));
 return km*1000/mPP/g.rect.w*g.W;}
// ---- slide builder ----
function autoTitle(o){
 const sc=activeSc(),T=state.T;
 const r=computeCoverage(kpiSites(),T);
 if(o.places&&sc.places.length){
  const as=sc.places.filter(p=>p.state==='assigned').length;
  return`${sc.places.length} places (${as} assigned) cover ${r.pct==null?'–':r.pct.toFixed(0)+'%'} of demand within ${T} min`;}
 return`${filtered.length} dealer locations cover ${r.pct==null?'–':r.pct.toFixed(0)+'%'} of demand within ${T} min`;}
function initials(l){return l.group.replace(/[^A-ZÀ-Ž]/g,'').slice(0,2)||l.group.slice(0,2).toUpperCase();}
function buildSlide(pptx,preset,rect){
 const o=preset.o,g=slideGeom(rect),T=state.T,sl=pptx.addSlide();
 const F='Assistant';
 // title + subtitle (Folienmaster geometry)
 sl.addText(o.title||autoTitle(o),{x:0.57,y:0.35,w:11.81,h:0.85,fontFace:F,fontSize:20,bold:true,color:CI.petrol,valign:'top'});
 sl.addText(`${C().name} · ${activeSc().name} · drive-time threshold ${T} min · ${new Date().toISOString().slice(0,10)}`,
  {x:0.57,y:1.16,w:11.81,h:0.32,fontFace:F,fontSize:11,color:CI.grey});
 // basemap
 let baseWarn=false;
 if(o.base){const b=captureBasemap(2,rect);
  if(b.data&&b.ok)sl.addImage({data:b.data,x:g.X,y:g.Y,w:g.W,h:g.H});
  else{baseWarn=true;
   sl.addShape(pptx.ShapeType.rect,{x:g.X,y:g.Y,w:g.W,h:g.H,fill:{color:'EFF3F6'},line:{color:'D5DDE3',width:0.75}});}}
 else sl.addShape(pptx.ShapeType.rect,{x:g.X,y:g.Y,w:g.W,h:g.H,fill:{color:'F6F8FA'},line:{color:'D5DDE3',width:0.75}});
 // density layers
 if(o.pop)sl.addImage({data:captureDensity('pop',rect),x:g.X,y:g.Y,w:g.W,h:g.H});
 if(o.heat)sl.addImage({data:captureDensity('heat',rect),x:g.X,y:g.Y,w:g.W,h:g.H});
 // gaps veil
 if(o.gaps)sl.addImage({data:renderVeilOffscreen(kpiSites(),T,rect),x:g.X,y:g.Y,w:g.W,h:g.H});
 // model areas
 const places=activeSc().places;
 if(o.areas==='model'&&places.length)
  sl.addImage({data:renderAreasOffscreen(places,T,rect),x:g.X,y:g.Y,w:g.W,h:g.H});
 // dealers
 const mode=o.dealers==='auto'?(filtered.length>450?'image':'shapes'):o.dealers;
 if(mode==='image'&&filtered.length)
  sl.addImage({data:dotsImage(rect),x:g.X,y:g.Y,w:g.W,h:g.H});
 if(mode==='shapes'){let di=0,bb=null;
  for(const l of filtered){
   const p=ll2in(g,l.lat,l.lon);if(!p.vis)continue;
   const x=p.x-0.045,y=p.y-0.045;
   sl.addShape(pptx.ShapeType.ellipse,{x,y,w:0.09,h:0.09,objectName:'dnpdot_'+(di++),
    fill:{color:colorFor(l).slice(1)},line:{color:'FFFFFF',width:0.75}});
   if(!bb)bb={x0:x,y0:y,x1:x+0.09,y1:y+0.09};
   else{bb.x0=Math.min(bb.x0,x);bb.y0=Math.min(bb.y0,y);bb.x1=Math.max(bb.x1,x+0.09);bb.y1=Math.max(bb.y1,y+0.09);}}
  if(di>1)GROUP_JOBS.push({slide:pptx.slides?pptx.slides.length:GROUP_JOBS.length+1,bb});}
 // cities
 if(o.cities)CITIES.filter(c=>C().markets.includes(c.c)).forEach(c=>{
  const p=ll2in(g,c.lat,c.lon);if(!p.vis)return;
  sl.addShape(pptx.ShapeType.ellipse,{x:p.x-0.03,y:p.y-0.03,w:0.06,h:0.06,fill:{color:'FFFFFF'},line:{color:'44546A',width:1}});
  sl.addText(c.name,{x:p.x+0.04,y:p.y-0.11,w:1.4,h:0.2,fontFace:F,fontSize:7.5,color:'44546A'});});
 // schematic areas + places
 if(o.places){
  if(o.areas==='schematic'){const r=kmToIn(g,T*0.55);
   for(const p of places){const q=ll2in(g,p.lat,p.lon);if(!q.vis)continue;
    sl.addShape(pptx.ShapeType.ellipse,{x:q.x-r,y:q.y-r,w:2*r,h:2*r,
     fill:{color:CI.petrol,transparency:88},line:{color:CI.petrol,width:1,dashType:'dash'}});}}
  for(const p of places){const q=ll2in(g,p.lat,p.lon);if(!q.vis)continue;
   const D=0.30,a=p.assigned&&p.assigned!=='GF'?locById[p.assigned]:null;
   if(p.state==='assigned'&&p.greenfield)
    sl.addText('G',{shape:pptx.ShapeType.ellipse,x:q.x-D/2,y:q.y-D/2,w:D,h:D,align:'center',valign:'middle',margin:0,
     fill:{color:CI.green},line:{color:'FFFFFF',width:1.5},fontFace:F,fontSize:9,bold:true,color:CI.petrol});
   else if(p.state==='assigned'&&a)
    sl.addText(initials(a),{shape:pptx.ShapeType.ellipse,x:q.x-D/2,y:q.y-D/2,w:D,h:D,align:'center',valign:'middle',margin:0,
     fill:{color:CI.petrol},line:{color:'FFFFFF',width:1.5},fontFace:F,fontSize:8,bold:true,color:'FFFFFF'});
   else if(p.state==='short')
    sl.addText('?',{shape:pptx.ShapeType.ellipse,x:q.x-D/2,y:q.y-D/2,w:D,h:D,align:'center',valign:'middle',margin:0,
     fill:{color:'FFFFFF'},line:{color:CI.warn,width:1.75},fontFace:F,fontSize:9,bold:true,color:CI.warn});
   else
    sl.addShape(pptx.ShapeType.ellipse,{x:q.x-D/2,y:q.y-D/2,w:D,h:D,
     fill:{color:CI.petrol,transparency:90},line:{color:CI.petrol,width:1.5,dashType:'dash'}});
   const SZ={S:[8.5,7.5],M:[9.5,8.5],L:[11,9.5]}[o.labSize||'M'];
   const lines=[{text:p.name,options:{fontSize:SZ[0],bold:true,color:CI.petrol,breakLine:true}}];
   let line2=null;
   if(a)line2=a.city;else if(p.greenfield)line2='greenfield';
   if(line2)lines.push({text:line2,options:{fontSize:SZ[1],color:'333F49',italic:!a}});
   const chars=Math.max(p.name.length,(line2||'').length);
   const w=Math.max(0.55,chars*SZ[0]*0.0088+0.12);
   const h=(line2?SZ[0]+SZ[1]:SZ[0])*1.32/72+0.05;
   const st=o.labStyle||'chip';
   const opt={x:q.x-w/2,y:q.y+D/2+0.02,w,h,align:'center',margin:0.015,fontFace:F,
    fit:'resize',line:{type:'none'}};
   if(st==='chip')opt.fill={color:'FFFFFF',transparency:28};
   if(st==='shadow')opt.shadow={type:'outer',color:'FFFFFF',blur:4,offset:0,opacity:.95,angle:90};
   if(st==='outline')opt.outline={size:0.55,color:'FFFFFF'};
   sl.addText(lines,opt);}}
 // legend (native)
 if(o.legend){
  const rows=[];
  if(mode!=='off'&&filtered.length){const cset=CFG.colors[state.colorBy];
   for(const k in cset)rows.push({c:cset[k].slice(1),t:(CFG.labels[state.colorBy]||{})[k]||k,shape:'dot'});}
  if(o.places&&places.length){
   if(places.some(p=>p.state==='assigned'&&!p.greenfield))rows.push({c:CI.petrol,t:'Place — assigned',shape:'dot'});
   if(places.some(p=>p.state==='short'))rows.push({c:CI.warn,t:'Place — suggested',shape:'ring'});
   if(places.some(p=>p.state==='open'))rows.push({c:CI.petrol,t:'Place — open',shape:'ring'});
   if(places.some(p=>p.greenfield))rows.push({c:CI.green,t:'Place — greenfield',shape:'dot'});}
  if(o.heat)rows.push({c:'008CC8',t:'Dealer density',shape:'sq'});
  if(o.pop)rows.push({c:'D95F2B',t:'Population density'+(state.weight?' (weighted)':''),shape:'sq'});
  if(o.gaps)rows.push({c:'54606C',t:`Not covered ≤${T} min`,shape:'sq'});
  if(o.areas!=='off')rows.push({c:CI.petrol,t:`Market area ≤${T} min`,shape:'ring'});
  if(rows.length){
   const LH=0.21,LW=2.05,lx=g.X+g.W-LW-0.12,ly=g.Y+0.12,lh=rows.length*LH+0.16;
   sl.addShape(pptx.ShapeType.roundRect,{x:lx,y:ly,w:LW,h:lh,rectRadius:0.05,
    fill:{color:'FFFFFF',transparency:8},line:{color:'D5DDE3',width:0.75}});
   rows.forEach((r,i)=>{const y=ly+0.09+i*LH;
    if(r.shape==='sq')sl.addShape(pptx.ShapeType.rect,{x:lx+0.09,y:y+0.02,w:0.12,h:0.12,fill:{color:r.c,transparency:40}});
    else sl.addShape(pptx.ShapeType.ellipse,{x:lx+0.09,y:y+0.02,w:0.12,h:0.12,
     fill:r.shape==='ring'?{color:'FFFFFF'}:{color:r.c},line:{color:r.c,width:1.25}});
    sl.addText(r.t,{x:lx+0.26,y:y-0.02,w:LW-0.3,h:LH,fontFace:F,fontSize:8.5,color:'333F49'});});}}
 // KPI box (native)
 if(o.kpi){const r=computeCoverage(kpiSites(),T);
  const kw=1.95,kh=0.86,kx=g.X+g.W-kw-0.12,ky=g.Y+g.H-kh-0.12;
  sl.addShape(pptx.ShapeType.roundRect,{x:kx,y:ky,w:kw,h:kh,rectRadius:0.05,
   fill:{color:'FFFFFF',transparency:8},line:{color:'D5DDE3',width:0.75}});
  sl.addText(r.pct==null?'–':r.pct.toFixed(0)+'%',{x:kx+0.08,y:ky+0.04,w:kw-0.16,h:0.42,fontFace:F,fontSize:22,bold:true,color:CI.petrol});
  sl.addText(`of demand ≤${T} min${state.weight?' (weighted)':''}\n${C().markets.map(m=>m+' '+((computeCoverage(kpiSites(),T).per[m]||0)).toFixed(0)+'%').join(' · ')}`,
   {x:kx+0.08,y:ky+0.44,w:kw-0.16,h:0.4,fontFace:F,fontSize:7.5,color:CI.grey});}
 // source line
 sl.addText('Source: dealer database (v3 merged); drive-time model estimates (±20–30%, synthetic road graph); demand: official census municipalities, scaled'+
  (state.weight?', × regional motorization':'')+`. Generated by Dealer Network Platform, ${new Date().toISOString().slice(0,10)}.`+
  (baseWarn?' Basemap could not be captured (offline?).':''),
  {x:0.57,y:6.98,w:11.81,h:0.3,fontFace:F,fontSize:7.5,color:'8A97A3',italic:true});
 return baseWarn;}
let GROUP_JOBS=[];
const EMU=v=>Math.round(v*914400);
async function groupDots(b64){
 if(!GROUP_JOBS.length)return b64;
 const zip=await JSZip.loadAsync(b64,{base64:true});
 const names=Object.keys(zip.files).filter(n=>/^ppt\/slides\/slide\d+\.xml$/.test(n))
  .sort((a,b)=>+a.match(/\d+/)[0]-+b.match(/\d+/)[0]);
 let ji=0;
 for(const n of names){
  let xml=await zip.file(n).async('string');
  if(!xml.includes('name="dnpdot_'))continue;
  const job=GROUP_JOBS[ji++]||GROUP_JOBS[GROUP_JOBS.length-1];
  const sps=[];
  xml=xml.replace(/<p:sp>(?:(?!<\/p:sp>)[\s\S])*?<\/p:sp>/g,m=>{
   if(m.includes('name="dnpdot_')){sps.push(m);return'';}return m;});
  if(sps.length>1){
   const b2=job.bb;
   const off=`x="${EMU(b2.x0)}" y="${EMU(b2.y0)}"`,ext=`cx="${EMU(b2.x1-b2.x0)}" cy="${EMU(b2.y1-b2.y0)}"`;
   const grp=`<p:grpSp><p:nvGrpSpPr><p:cNvPr id="90001" name="Existing dealers"/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>`+
    `<p:grpSpPr><a:xfrm><a:off ${off}/><a:ext ${ext}/><a:chOff ${off}/><a:chExt ${ext}/></a:xfrm></p:grpSpPr>`+
    sps.join('')+`</p:grpSp>`;
   xml=xml.replace('</p:spTree>',grp+'</p:spTree>');}
  else if(sps.length===1)xml=xml.replace('</p:spTree>',sps[0]+'</p:spTree>');
  zip.file(n,xml);}
 return zip.generateAsync({type:'base64',compression:'DEFLATE'});}
async function buildPptx(presets){
 GROUP_JOBS=[];
 const pptx=new PptxGenJS();
 pptx.defineLayout({name:'CM169',width:13.333,height:7.5});
 pptx.layout='CM169';
 pptx.author='Dealer Network Platform';pptx.company='Horváth';
 let warn=false;let i=0;
 for(const p of presets){i++;
  const st=$('exStatus');if(st)st.textContent=`Rendering slide ${i}/${presets.length} — ${p.name}…`;
  await new Promise(r=>setTimeout(r,30));
  warn=await withFrame(p.o.frame||null,rect=>buildSlide(pptx,p,rect))||warn;}
 let b64=await pptx.write('base64');
 b64=await groupDots(b64);
 return{b64,warn};}
window.__buildPptx=ids=>buildPptx(WS.pptPresets.filter(p=>ids.includes(p.id)));
// ---- flat PNG ----
function flatPng(o){return withFrame(o.frame||null,rect=>flatPngRect(o,rect));}
function flatPngRect(o,rect){
 const T=state.T;
 const size=map.getSize();
 const c=document.createElement('canvas');c.width=size.x*2;c.height=size.y*2;
 const ctx=c.getContext('2d');
 const put=d=>{if(!d)return;const im=new Image();im.src=d;
  return new Promise(res=>{im.onload=()=>{ctx.drawImage(im,0,0,c.width,c.height);res();};im.onerror=res;});};
 const jobs=[];
 if(o.base){const b=captureBasemap(2,rect);jobs.push(put(b.data));}
 if(o.gaps)jobs.push(put(renderVeilOffscreen(kpiSites(),T)));
 if(o.areas==='model'&&activeSc().places.length)jobs.push(put(renderAreasOffscreen(activeSc().places,T)));
 if(o.dealers!=='off'&&filtered.length)jobs.push(put(dotsImage()));
 return Promise.all(jobs).then(()=>{
  const x2=ctx;x2.scale(2,2);x2.translate(-rect.x,-rect.y);
  if(o.places)for(const p of activeSc().places){
   const q=map.latLngToContainerPoint([p.lat,p.lon]);
   x2.beginPath();x2.arc(q.x,q.y,10,0,6.2832);
   const a=p.assigned&&p.assigned!=='GF'?locById[p.assigned]:null;
   x2.fillStyle=p.greenfield?'#00CD55':(p.state==='assigned'?'#023F40':'rgba(2,63,64,.12)');
   x2.fill();x2.lineWidth=2;x2.strokeStyle=p.state==='assigned'||p.greenfield?'#fff':'#023F40';
   if(p.state==='open')x2.setLineDash([4,3]);x2.stroke();x2.setLineDash([]);
   x2.fillStyle=p.state==='assigned'&&!p.greenfield?'#fff':'#023F40';
   x2.font='bold 9px Assistant,Segoe UI';x2.textAlign='center';
   x2.fillText(p.greenfield?'G':(a?initials(a):p.state==='short'?'?':'+'),q.x,q.y+3);
   x2.fillText(p.name,q.x,q.y+22);}
  return c.toDataURL('image/png');});}
// ---- market fragmentation PPT slide ----
async function buildFragPptx(N){
 const d=fragData(N);
 const pptx=new PptxGenJS();
 pptx.defineLayout({name:'CM169',width:13.333,height:7.5});pptx.layout='CM169';
 pptx.author='Dealer Network Platform';pptx.company='Horváth';
 const sl=pptx.addSlide();const F='Assistant';
 const top10=d.rows[Math.min(9,d.rows.length-1)],top25=d.rows[Math.min(24,d.rows.length-1)],topAll=d.rows[d.rows.length-1];
 sl.addText(`Covering the top ${d.rows.length} municipalities as quickly as possible`,
  {x:0.57,y:0.35,w:11.81,h:0.6,fontFace:F,fontSize:22,bold:true,color:CI.petrol});
 sl.addText(`… is crucial in order to reach a significant share of the addressable population — ${C().markets.join(' + ')}`,
  {x:0.57,y:0.95,w:11.81,h:0.35,fontFace:F,fontSize:13,color:CI.grey});
 const PX=0.75,PY=1.85,PW=9.4,PH=4.55; // plot area (in)
 sl.addShape(pptx.ShapeType.rect,{x:PX,y:PY,w:PW,h:PH,fill:{color:'FFFFFF'},line:{color:'D5DDE3',width:0.75}});
 sl.addText('[population reach, cumulative %]',{x:PX,y:PY-0.28,w:4,h:0.24,fontFace:F,fontSize:9.5,color:CI.grey});
 // bands (native rects, editable) + avg labels
 const bands=fragBands(d.rows);const bandCols=['E8F6EE','F1FAF4','F4F6F7'];
 const xf=i=>PX+PW*(d.rows.length<=1?0:i/(d.rows.length-1));
 const maxY=Math.min(100,Math.ceil(Math.max(10,d.rows[d.rows.length-1].cumPct)/10)*10);
 const yf=v=>PY+PH*(1-v/maxY);
 bands.forEach((b,i)=>{const x0=xf(b.from),x1=xf(Math.min(b.to,d.rows.length-1));
  sl.addShape(pptx.ShapeType.rect,{x:x0,y:PY,w:Math.max(0.02,x1-x0),h:PH,fill:{color:bandCols[i%3]},line:{type:'none'}});
  sl.addText(`ø ~${b.avg.toFixed(1)}% increase per city`,{x:x0,y:PY-0.02,w:Math.max(0.3,x1-x0),h:0.24,
   align:'center',fontFace:F,fontSize:8.5,bold:true,color:'2C7A4B'});});
 // gridlines native
 for(let v=0;v<=maxY;v+=Math.max(10,Math.round(maxY/5/10)*10)){const yy=yf(v);
  sl.addShape(pptx.ShapeType.line,{x:PX,y:yy,w:PW,h:0,line:{color:'E3E8EC',width:0.75}});
  sl.addText(v+'%',{x:PX-0.55,y:yy-0.1,w:0.48,h:0.2,align:'right',fontFace:F,fontSize:8,color:CI.grey});}
 // curve as freeform + points
 const pts2=d.rows.map((r,i)=>({x:xf(i),y:yf(r.cumPct)}));
 sl.addShape(pptx.ShapeType.line,{x:0,y:0,w:0,h:0}); // no-op keep pptxgen shape cache warm
 // freeform curve via custGeom points using addShape 'line' segments (robust, always renders)
 for(let i=1;i<pts2.length;i++){
  sl.addShape(pptx.ShapeType.line,{x:Math.min(pts2[i-1].x,pts2[i].x),y:Math.min(pts2[i-1].y,pts2[i].y),
   w:Math.abs(pts2[i].x-pts2[i-1].x)||0.001,h:Math.abs(pts2[i].y-pts2[i-1].y)||0.001,
   flipH:pts2[i].x<pts2[i-1].x,flipV:pts2[i].y<pts2[i-1].y,
   line:{color:CI.green,width:2.25}});}
 pts2.forEach(p=>sl.addShape(pptx.ShapeType.ellipse,{x:p.x-0.045,y:p.y-0.045,w:0.09,h:0.09,
  fill:{color:CI.petrol},line:{color:'FFFFFF',width:1}}));
 // draggable label textboxes — pre-placed near each point, alternating above/below to reduce overlap
 const F2=F,dense=d.rows.length>22,step=Math.ceil(d.rows.length/22);
 const shown=[];
 d.rows.forEach((r,i)=>{if(!dense||i<12||i%step===0||i===d.rows.length-1)shown.push(i);});
 shown.forEach((idx,j)=>{
  const r=d.rows[idx],p=pts2[idx],above=j%2===0;
  const ly=above?p.y-0.32:p.y+0.10;
  sl.addText(`${r.name} +${r.incPct.toFixed(1)}%`,
   {x:p.x-0.02,y:ly,w:1.7,h:0.22,fontFace:F2,fontSize:8,color:'33424A',
    fill:{color:'FFFFFF',transparency:15},line:{type:'none'},margin:0.01,align:'left'});});
 // axis footer
 sl.addText('0',{x:PX-0.05,y:PY+PH+0.02,w:0.3,h:0.2,fontFace:F,fontSize:8.5,color:CI.grey});
 sl.addText(d.rows.length+' municipalities',{x:PX+PW-1.6,y:PY+PH+0.02,w:1.6,h:0.2,align:'right',fontFace:F,fontSize:8.5,color:CI.grey});
 // summary table (native, editable)
 const tx=PX+PW+0.35,tw=13.333-tx-0.4;
 const tRows=[['Addressable market',`Top ${Math.min(10,d.rows.length)}`,`Top ${Math.min(25,d.rows.length)}`,`Top ${d.rows.length}`],
  ['% of total population covered',top10.cumPct.toFixed(1)+'%',top25.cumPct.toFixed(1)+'%',topAll.cumPct.toFixed(1)+'%']];
 sl.addTable(tRows,{x:tx,y:PY,w:tw,fontFace:F,fontSize:9,color:'333F49',border:{type:'solid',color:'D5DDE3',pt:0.5},
  fill:{color:'F6F8FA'},autoPage:false,rowH:0.5,
  colW:[tw*0.4,tw*0.2,tw*0.2,tw*0.2]});
 sl.addText([{text:`The top ${Math.min(10,d.rows.length)} municipalities `,options:{bold:true}},
  {text:`need to be covered right away for a significant effect of the market entry.`,options:{}}],
  {x:tx,y:PY+1.7,w:tw,h:0.9,fontFace:F,fontSize:10.5,color:'333F49',
   fill:{color:'E8F6EE'},line:{type:'none'},valign:'middle',margin:0.1});
 sl.addText([{text:`The top ${d.rows.length} municipalities `,options:{bold:true}},
  {text:`reach ~${topAll.cumPct.toFixed(0)}% of the addressable population.`,options:{}}],
  {x:tx,y:PY+2.75,w:tw,h:0.9,fontFace:F,fontSize:10.5,color:'333F49',
   fill:{color:'E8F6EE'},line:{type:'none'},valign:'middle',margin:0.1});
 sl.addText('Source: dealer database population model (census municipalities). Generated by Dealer Network Platform, '+new Date().toISOString().slice(0,10)+'.',
  {x:0.57,y:6.98,w:11.81,h:0.3,fontFace:F,fontSize:7.5,color:'8A97A3',italic:true});
 return pptx.write('base64');}
async function buildCovPptx(){
 const curves=covCurves();
 const pptx=new PptxGenJS();
 pptx.defineLayout({name:'CM169',width:13.333,height:7.5});pptx.layout='CM169';
 pptx.author='Dealer Network Platform';pptx.company='Horváth';
 const sl=pptx.addSlide();const F='Assistant';
 const single=curves.length===1;
 sl.addText(single
   ?`${curves[0].rows.length} places cover ${curves[0].rows[curves[0].rows.length-1].cumPct.toFixed(0)}% of demand within ${state.T} min`
   :`Scenario comparison — coverage build-up within ${state.T} min`,
  {x:0.57,y:0.35,w:11.81,h:0.6,fontFace:F,fontSize:22,bold:true,color:CI.petrol});
 sl.addText(`Places ordered by marginal coverage gain · drive-time model (est.)${state.weight?' · demand weighted':''} · ${new Date().toISOString().slice(0,10)}`,
  {x:0.57,y:0.95,w:11.81,h:0.35,fontFace:F,fontSize:12,color:CI.grey});
 const PX=0.75,PY=1.85,PW=9.4,PH=4.55;
 sl.addShape(pptx.ShapeType.rect,{x:PX,y:PY,w:PW,h:PH,fill:{color:'FFFFFF'},line:{color:'D5DDE3',width:0.75}});
 const maxN=Math.max(...curves.map(d=>d.rows.length));
 const maxY=Math.min(100,Math.ceil(Math.max(20,...curves.map(d=>d.rows[d.rows.length-1].cumPct))/10)*10);
 const xf=i=>PX+PW*(maxN<=1?0:i/(maxN-1));
 const yf=v=>PY+PH*(1-v/maxY);
 for(let v=0;v<=maxY;v+=Math.max(10,Math.round(maxY/5/10)*10)){const yy=yf(v);
  sl.addShape(pptx.ShapeType.line,{x:PX,y:yy,w:PW,h:0,line:{color:'E3E8EC',width:0.75}});
  sl.addText(v+'%',{x:PX-0.55,y:yy-0.1,w:0.48,h:0.2,align:'right',fontFace:F,fontSize:8,color:CI.grey});}
 const cuts=single?covBandCuts(curves[0]):null;
 if(cuts){
  const rows0=curves[0].rows,n=rows0.length;
  const segs=[{from:0,to:cuts.a},{from:cuts.a,to:cuts.b},{from:cuts.b,to:n}];
  const bandCols=['E8F6EE','F1FAF4','F4F6F7'];
  const bx=idx=>idx<=0?xf(0):idx>=n?xf(n-1):(xf(idx-1)+xf(idx))/2;
  segs.forEach((sg,i)=>{const x0=bx(sg.from),x1=bx(sg.to);
   const avg=sg.to>sg.from?rows0.slice(sg.from,sg.to).reduce((s2,r)=>s2+r.gainPP,0)/(sg.to-sg.from):0;
   sl.addShape(pptx.ShapeType.rect,{x:x0,y:PY,w:Math.max(0.02,x1-x0),h:PH,fill:{color:bandCols[i%3]},line:{type:'none'}});
   sl.addText(`ø +${avg.toFixed(1)}% per place (Top ${sg.to})`,{x:x0,y:PY-0.26,w:Math.max(0.3,x1-x0),h:0.22,align:'center',fontFace:F,fontSize:8.5,bold:true,color:'2C7A4B'});});}
 const cols=['00CD55','008CC8','C07A1E','7A5AA3','D9534F'];
 curves.forEach((d,ci)=>{const col=cols[ci%cols.length];
  const pts=d.rows.map((r,i)=>({x:xf(i),y:yf(r.cumPct)}));
  for(let i=1;i<pts.length;i++)
   sl.addShape(pptx.ShapeType.line,{x:Math.min(pts[i-1].x,pts[i].x),y:Math.min(pts[i-1].y,pts[i].y),
    w:Math.abs(pts[i].x-pts[i-1].x)||0.001,h:Math.abs(pts[i].y-pts[i-1].y)||0.001,
    flipH:pts[i].x<pts[i-1].x,flipV:pts[i].y<pts[i-1].y,line:{color:col,width:2.25}});
  pts.forEach(p=>sl.addShape(pptx.ShapeType.ellipse,{x:p.x-0.045,y:p.y-0.045,w:0.09,h:0.09,
   fill:{color:CI.petrol},line:{color:'FFFFFF',width:1}}));
  if(single){
   d.rows.forEach((r,i)=>{const above=i%2===0;
    sl.addText(`${r.name} +${r.gainPP.toFixed(1)}%`,
     {x:pts[i].x-0.02,y:above?pts[i].y-0.32:pts[i].y+0.10,w:1.7,h:0.22,fontFace:F,fontSize:8,color:'33424A',
      fill:{color:'FFFFFF',transparency:15},line:{type:'none'},margin:0.01});});}
  else{const last=d.rows[d.rows.length-1];
   sl.addText(`${d.label} — ${last.cumPct.toFixed(0)}%`,
    {x:Math.min(PX+PW-2.2,xf(d.rows.length-1)+0.08),y:yf(last.cumPct)-0.1,w:2.2,h:0.2,
     fontFace:F,fontSize:8.5,bold:true,color:col,fill:{color:'FFFFFF',transparency:20},line:{type:'none'},margin:0.01});}});
 // summary table
 const tx=PX+PW+0.35,tw=13.333-tx-0.4;
 let tRows;
 if(single){const d=curves[0],pick=n=>d.rows[Math.min(n-1,d.rows.length-1)];
  const cu=covBandCuts(d)||{a:Math.min(3,d.rows.length),b:Math.min(5,d.rows.length)};
  tRows=[['Places','Top '+cu.a,'Top '+cu.b,'Top '+d.rows.length],
   ['Coverage',pick(cu.a).cumPct.toFixed(1)+'%',pick(cu.b).cumPct.toFixed(1)+'%',d.rows[d.rows.length-1].cumPct.toFixed(1)+'%']];}
 else tRows=[['Scenario','Places','Coverage'],
  ...curves.map(d=>[d.label,String(d.rows.length),d.rows[d.rows.length-1].cumPct.toFixed(0)+'%'])];
 sl.addTable(tRows,{x:tx,y:PY,w:tw,fontFace:F,fontSize:9,color:'333F49',
  border:{type:'solid',color:'D5DDE3',pt:0.5},fill:{color:'F6F8FA'},rowH:0.42,autoPage:false});
 sl.addText('Source: dealer database; drive-time model estimates (±20–30%); demand: census municipalities'+(state.weight?' × regional motorization':'')+'. Generated by Dealer Network Platform, '+new Date().toISOString().slice(0,10)+'.',
  {x:0.57,y:6.98,w:11.81,h:0.3,fontFace:F,fontSize:7.5,color:'8A97A3',italic:true});
 return pptx.write('base64');}
$('fragPpt').onclick=async()=>{
 if(fragMode==='cov'&&!covCurves().length){ui.alert('No places in the selected scenario(s).');return;}
 $('fragPpt').textContent='Rendering…';
 const b64=fragMode==='cov'?await buildCovPptx():await buildFragPptx(+$('fragN').value);
 const a=document.createElement('a');
 a.href='data:application/vnd.openxmlformats-officedocument.presentationml.presentation;base64,'+b64;
 a.download=fragMode==='cov'?'coverage_buildup.pptx':'market_fragmentation.pptx';a.click();
 $('fragPpt').textContent='Export PPT slide';};
// ---- dialog wiring ----
function exRender(){
 const el=$('exPresets');el.innerHTML='';
 WS.pptPresets.forEach(p=>{
  const d=document.createElement('div');d.className='exP'+(p.id===exSel?' sel':'');
  const cb=document.createElement('input');cb.type='checkbox';cb.checked=WS.pptChecked.includes(p.id);
  cb.onclick=e=>{e.stopPropagation();
   WS.pptChecked=cb.checked?[...WS.pptChecked,p.id]:WS.pptChecked.filter(x=>x!==p.id);save();};
  d.appendChild(cb);
  const nm=document.createElement('span');nm.className='nm';nm.textContent=p.name;d.appendChild(nm);
  const dup=document.createElement('span');dup.className='x';dup.textContent='⧉';dup.title='Duplicate preset';
  dup.onclick=e=>{e.stopPropagation();
   const c={id:'x'+Date.now()+Math.floor(Math.random()*99),name:p.name+' copy',o:JSON.parse(JSON.stringify(p.o))};
   const i=WS.pptPresets.indexOf(p);WS.pptPresets.splice(i+1,0,c);
   exSel=c.id;save();exRender();};
  d.appendChild(dup);
  if(WS.pptPresets.length>1){const x=document.createElement('span');x.className='x';x.textContent='✕';
   x.onclick=async e=>{e.stopPropagation();
    if(!await ui.confirm(`Delete preset "${p.name}"?`,{danger:true,ok:'Delete'}))return;
    WS.pptPresets=WS.pptPresets.filter(q=>q.id!==p.id);
    WS.pptChecked=WS.pptChecked.filter(q=>q!==p.id);
    if(exSel===p.id)exSel=WS.pptPresets[0].id;save();exRender();};d.appendChild(x);}
  d.onclick=()=>{exSel=p.id;exRender();};
  el.appendChild(d);});
 const o=exP().o;
 $('exFrameLbl').textContent=frameLabel(o.frame||null);
 $('exName').value=exP().name;$('exTitle').value=o.title||'';
 $('exBase').checked=o.base;$('exDealers').value=o.dealers;$('exPlaces').checked=o.places;
 $('exAreas').value=o.areas;$('exGaps').checked=o.gaps;$('exCities').checked=o.cities;
 $('exLegend').checked=o.legend;$('exKpi').checked=o.kpi;$('exHeat').checked=!!o.heat;$('exPop').checked=!!o.pop;
 $('exLabStyle').value=o.labStyle||'chip';$('exLabSize').value=o.labSize||'M';}
document.querySelectorAll('#exDlg [data-fr]').forEach(c=>c.onclick=()=>{
 const v=c.dataset.fr;
 if(v==='edit'){$('exDlg').close();crop.r=null;cropShow();return;}
 exP().o.frame=v==='view'?null:(v==='case'?caseBounds():REGION_BOUNDS[v].map(x=>[...x]));
 save();
 if(exP().o.frame)map.fitBounds(exP().o.frame,{animate:false,padding:[6,6]});
 $('exFrameLbl').textContent=frameLabel(exP().o.frame);});
$('exBtn').onclick=()=>{exRender();$('exStatus').textContent='';$('exDlg').showModal();};
$('exClose').onclick=()=>$('exDlg').close();
// live bindings — no Save needed
[['exLabStyle','labStyle','v'],['exLabSize','labSize','v'],['exBase','base','c'],['exDealers','dealers','v'],['exPlaces','places','c'],['exAreas','areas','v'],
 ['exGaps','gaps','c'],['exHeat','heat','c'],['exPop','pop','c'],['exCities','cities','c'],
 ['exLegend','legend','c'],['exKpi','kpi','c'],['exTitle','title','v']].forEach(([id,key,kind])=>{
 $(id).addEventListener('change',e=>{exP().o[key]=kind==='c'?e.target.checked:e.target.value;save();});});
$('exName').addEventListener('change',e=>{exP().name=e.target.value.trim()||exP().name;save();exRender();});
$('exNew').onclick=()=>{
 const p={id:'x'+Date.now(),name:'New preset',o:{base:true,dealers:'auto',places:true,areas:'off',gaps:false,cities:false,legend:true,kpi:true,title:''}};
 WS.pptPresets.push(p);exSel=p.id;WS.pptChecked.push(p.id);save();exRender();};
$('exGo').onclick=()=>{
 const sel=WS.pptPresets.filter(p=>WS.pptChecked.includes(p.id));
 if(!sel.length){$('exStatus').textContent='Tick at least one preset.';return;}
 $('exStatus').textContent='Generating '+sel.length+' slide(s)…';
 setTimeout(()=>{buildPptx(sel).then(({b64,warn})=>{
  const a=document.createElement('a');
  a.href='data:application/vnd.openxmlformats-officedocument.presentationml.presentation;base64,'+b64;
  a.download='dealer_network_'+new Date().toISOString().slice(0,10)+'.pptx';a.click();
  $('exStatus').textContent='Done.'+(warn?' Note: basemap not captured (offline?).':'');
 }).catch(e=>{$('exStatus').textContent='Export failed: '+e.message;});},50);};
$('exPng').onclick=()=>{
 $('exStatus').textContent='Rendering PNG…';
 setTimeout(()=>{flatPng(exP().o).then(d=>{
  const a=document.createElement('a');a.href=d;a.download='dealer_network_map.png';a.click();
  $('exStatus').textContent='Done.';});},50);};
