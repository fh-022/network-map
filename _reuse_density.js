// ================ disc canvas layer (isochrones + white spots) ================
const DiscLayer=L.Layer.extend({
 initialize:function(o){this.o=o;this.bands=[];},
 setBands:function(b){this.bands=b;this.redraw();},
 onAdd:function(m){this._map=m;this._c=L.DomUtil.create('canvas','');this._c.style.pointerEvents='none';
  m.getPane('overlayPane').appendChild(this._c);m.on('moveend zoomend resize',this.redraw,this);
  m.on('zoomstart',()=>{if(this._c)this._c.style.display='none';},this);this.redraw();},
 onRemove:function(m){m.off('moveend zoomend resize',this.redraw,this);L.DomUtil.remove(this._c);this._map=null;},
 redraw:function(){if(!this._map)return;const m=this._map,size=m.getSize();
  this._c.style.display='';L.DomUtil.setPosition(this._c,m.containerPointToLayerPoint([0,0]));
  this._c.width=size.x;this._c.height=size.y;
  const ctx=this._c.getContext('2d');ctx.clearRect(0,0,size.x,size.y);
  if(!this.bands.length)return;
  const mPP=40075016.686*Math.cos(m.getCenter().lat*Math.PI/180)/(256*Math.pow(2,m.getZoom()));
  const pxPerKm=1000/mPP;
  const buf=document.createElement('canvas');buf.width=size.x;buf.height=size.y;
  const bctx=buf.getContext('2d');
  if(this.o.mode==='veil'){
   ctx.fillStyle=this.o.veil;ctx.fillRect(0,0,size.x,size.y);
   ctx.globalCompositeOperation='destination-out';
   for(const band of this.bands){
    for(const[la,lo,rkm]of band.discs){
     const p=m.latLngToContainerPoint([la,lo]);
     if(p.x<-400||p.y<-400||p.x>size.x+400||p.y>size.y+400)continue;
     ctx.beginPath();ctx.arc(p.x,p.y,Math.max(2,rkm*pxPerKm),0,6.2832);ctx.fillStyle='#000';ctx.fill();}}
   ctx.globalCompositeOperation='source-over';
  }else{
   for(const band of this.bands){
    bctx.clearRect(0,0,size.x,size.y);bctx.fillStyle=band.color;
    for(const[la,lo,rkm]of band.discs){
     const p=m.latLngToContainerPoint([la,lo]);
     if(p.x<-400||p.y<-400||p.x>size.x+400||p.y>size.y+400)continue;
     bctx.beginPath();bctx.arc(p.x,p.y,Math.max(2,rkm*pxPerKm),0,6.2832);bctx.fill();}
    ctx.globalAlpha=band.alpha;ctx.drawImage(buf,0,0);ctx.globalAlpha=1;}}}});
