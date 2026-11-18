# -*- coding: utf-8 -*-
"""
pages_page.py — page « menu » générique : chaque menu / sous-menu de l'appli est une page plein écran
(en-tête, bandeau joueur facultatif, sections, grandes cartes). L'appli envoie les données, la page les affiche ;
un appui sur une carte renvoie son numéro à Python qui exécute la bonne action.
"""

CSS = r"""
#pg{display:none;position:absolute;inset:0}
body.m-pg #pg{display:block}
#pg .corps{padding:12px 14px 28px}
.pgsous{font-size:13px;color:#cfd2f5;line-height:1.5;margin:2px 2px 12px}
.pgsous b{color:#fff}

/* bandeau joueur (accueil) */
.pghero{position:relative;display:flex;gap:14px;align-items:center;padding:14px;margin-bottom:14px;border:1px solid var(--pc);border-radius:6px;overflow:hidden;
 background:linear-gradient(135deg,rgba(255,255,255,.05),transparent 60%),#0f0d20}
.pghero::before{content:"";position:absolute;inset:-60%;background:conic-gradient(from 0deg,transparent 0 72%,var(--pc) 86%,transparent 100%);opacity:.14;animation:tourne 8s linear infinite}
.pghero>*{position:relative}
.pgb{flex:none;width:86px;height:86px;display:grid;place-items:center}
.pgb img,.pgb .emb{width:100%;height:100%;object-fit:contain;filter:drop-shadow(0 0 10px var(--pc))}
.pgn{font-size:20px;font-weight:900;color:#fff;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pgrg{font-size:14px;font-weight:800;color:var(--pc);text-shadow:0 0 10px var(--pc)}
.pgst{font-size:11px;color:#b4b8dc;margin-top:2px}

/* cartes */
.pgsec{font-size:10px;letter-spacing:.26em;color:var(--mg);margin:18px 2px 8px;text-transform:uppercase}
.pgsec::before{content:"// ";color:var(--cy)}
.pgsec:first-of-type{margin-top:4px}
.pgl2{display:grid;grid-template-columns:1fr;gap:10px}
.pgl2.c2{grid-template-columns:1fr 1fr}
.pgc{position:relative;display:flex;align-items:center;gap:14px;padding:16px 14px;min-height:84px;border:1px solid rgba(255,255,255,.12);border-left:4px solid var(--c);
 border-radius:6px;background:linear-gradient(100deg,rgba(255,255,255,.05),transparent 55%),#0f0d20;touch-action:manipulation;
 opacity:0;animation:pgentre .45s ease-out forwards;animation-delay:calc(var(--k)*55ms)}
@keyframes pgentre{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
.pgc:active{transform:scale(.985);background:#1a1740}
.pgc::after{content:"";position:absolute;left:0;right:0;bottom:0;height:2px;background:linear-gradient(90deg,var(--c),transparent);opacity:.7}
.pgi{flex:none;width:58px;height:58px;display:grid;place-items:center;border-radius:10px;background:rgba(255,255,255,.06);font-size:30px;box-shadow:inset 0 0 14px color-mix(in srgb,var(--c) 30%,transparent)}
.pgi img,.pgi .emb{width:100%;height:100%;object-fit:contain}
.pgt{flex:1;min-width:0;display:flex;flex-direction:column;gap:3px}
.pgt b{font-size:17px;color:#fff;line-height:1.2}
.pgt small{font-size:12px;color:#aab0d8;line-height:1.35}
.pgr{flex:none;display:flex;flex-direction:column;align-items:flex-end;gap:6px}
.pgch{font-size:26px;color:var(--c);line-height:1}
.pgl{font-size:20px}
.pgtag{font-size:10px;letter-spacing:.1em;padding:2px 7px;border:1px solid var(--c);color:var(--c);border-radius:3px;white-space:nowrap}
.pgc.lock{opacity:.6;border-left-color:#4a4780}
.pgc.lock .pgi img,.pgc.lock .pgi .emb{filter:grayscale(1) brightness(.6)}
.pgc.lock .pgt b{color:#aab0d8}
.pgc.new::before{content:"NOUVEAU";position:absolute;top:6px;right:8px;font-size:9px;letter-spacing:.14em;color:#06130b;background:var(--ok);padding:1px 6px;border-radius:2px}
.pgl2.c2 .pgc{flex-direction:column;text-align:center;justify-content:center;padding:18px 10px}
.pgl2.c2 .pgr{flex-direction:row;align-items:center}
.pgl2.c2 .pgt{align-items:center}
.pgsk{animation:secoue .3s}
#pgToast{position:absolute;left:14px;right:14px;bottom:18px;z-index:5;padding:12px 14px;border:1px solid var(--or);background:#1b1208;color:#ffd98a;font-size:13px;line-height:1.4;border-radius:6px;opacity:0;pointer-events:none;transition:opacity .2s}
#pgToast.on{opacity:1}
#pgBtns{display:flex;gap:8px}

/* page de texte (aide…) */
.pgbloc{border:1px solid rgba(255,43,214,.35);border-radius:6px;margin-bottom:10px;background:#0f0d20}
.pgbloc summary{padding:14px;font-size:14px;font-weight:800;color:var(--or);list-style:none;letter-spacing:.04em}
.pgbloc summary::-webkit-details-marker{display:none}
.pgbloc summary::before{content:"▸ ";color:var(--cy)}
.pgbloc[open] summary::before{content:"▾ "}
.pgbloc .tx{padding:0 14px 14px;font-size:13px;line-height:1.65;color:#d6d8f5}
.pgbloc .tx p{margin:0 0 10px}.pgbloc .tx b{color:#fff}.pgbloc .tx i{color:#7ff7ff;font-style:normal;font-weight:700}
.pgfin{display:block;width:100%;margin-top:14px;padding:16px;text-align:center;font:800 15px ui-monospace,monospace;letter-spacing:.14em;color:#fff;border:1px solid var(--cy);border-radius:6px;
 background:linear-gradient(90deg,rgba(0,240,255,.22),rgba(255,43,214,.22));touch-action:manipulation}
"""

HTML = r"""
<div id="pg" class="cadre"><div class="int">
  <div class="tete"><div class="bt" id="pgBack" onclick="PG.retour()">‹</div><div class="t" id="pgTitre">MENU</div><div id="pgBtns"></div></div>
  <div class="corps" id="pgcorps"></div>
  <div id="pgToast"></div>
</div></div>
"""

JS = r"""
var PG=(function(){
  var P=null,tm=null;
  function $(i){return document.getElementById(i);}
  function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function emb(col,txt,px){return '<div class="emb" style="--pc:'+col+';width:'+px+'px;height:'+px+'px;font-size:'+Math.round(px*.34)+'px">'+esc(txt||'★')+'</div>';}
  function badge(r,px){
    if(!r.b)return emb(r.col||'#00f0ff',r.v,px);
    return '<img src="'+esc(r.b)+'" alt="" onerror="PG.err(this,\''+esc(r.col||'#00f0ff')+'\',\''+esc(r.v||'')+'\','+px+')">';
  }
  function err(img,col,txt,px){var d=document.createElement('div');d.innerHTML=emb(col,txt,px);img.parentNode.replaceChild(d.firstChild,img);}

  /* [b]..[/b] et [i]..[/i] (balisage Kivy) -> HTML sûr */
  function balises(t){
    return esc(t).replace(/\[b\]/g,'<b>').replace(/\[\/b\]/g,'</b>').replace(/\[i\]/g,'<i>').replace(/\[\/i\]/g,'</i>');
  }

  function carte(it,k){
    var col=it.col||'#00f0ff';
    var ico=it.rang?badge(it.rang,46):'<span>'+esc(it.i||'•')+'</span>';
    var cls='pgc'+(it.etat==='lock'?' lock':'')+(it.etat==='new'?' new':'');
    return '<div class="'+cls+'" style="--c:'+col+';--pc:'+col+';--k:'+k+'" onclick="PG.item('+it.n+',this)">'+
      '<div class="pgi">'+ico+'</div><div class="pgt"><b>'+esc(it.t)+'</b>'+(it.d?'<small>'+esc(it.d)+'</small>':'')+
      (it.bar!=null?pal(it.bar,'pt',20,'s'):'')+'</div>'+
      '<div class="pgr">'+(it.tag?'<span class="pgtag">'+esc(it.tag)+'</span>':'')+(it.etat==='lock'?'<span class="pgl">🔒</span>':'<span class="pgch">›</span>')+'</div></div>';
  }

  function rendre(){
    $('pgTitre').textContent=(P.titre||'').toUpperCase();
    $('pgBack').style.display=P.retour?'':'none';
    $('pgBtns').innerHTML=(P.btns||[]).map(function(b){return '<div class="bt" onclick="PG.btn(\''+b.k+'\')">'+b.i+'</div>';}).join('');
    var h='';
    if(P.sous)h+='<div class="pgsous">'+balises(P.sous)+'</div>';
    if(P.hero){var o=P.hero;
      h+='<div class="pghero" style="--pc:'+o.col+'"><div class="pgb">'+badge({b:o.b,col:o.col,v:o.v},86)+'</div><div style="min-width:0;flex:1">'+
        '<div class="pgn">'+esc(o.nom)+'</div><div class="pgrg">'+esc(o.rang)+'</div>'+pal(o.pct,'pt',20,'g')+
        '<div class="pgst">'+esc(o.stat)+'</div></div></div>';}
    var k=0;
    (P.secs||[]).forEach(function(s){
      if(s.t)h+='<div class="pgsec">'+esc(s.t)+'</div>';
      h+='<div class="pgl2'+(P.cols===2?' c2':'')+'">'+s.items.map(function(it){return carte(it,k++);}).join('')+'</div>';
    });
    if(P.blocs){
      P.blocs.forEach(function(b,i){h+='<details class="pgbloc"'+(i===0?' open':'')+'><summary>'+esc(b.t)+'</summary><div class="tx">'+
        b.h.split('\n').filter(function(x){return x.trim();}).map(function(x){return '<p>'+balises(x)+'</p>';}).join('')+'</div></details>';});
      h+='<div class="pgfin" onclick="PG.retour()">J\'AI COMPRIS</div>';
    }
    var sc=$('pgcorps');sc.innerHTML=h;sc.scrollTop=0;
  }

  function toast(m){
    var t=$('pgToast');t.textContent=m;t.classList.add('on');
    if(tm)clearTimeout(tm);tm=setTimeout(function(){t.classList.remove('on');},3200);
  }
  return {
    ouvrir:function(p){P=p;rendre();},
    err:err,
    item:function(n,el){
      var it=null;(P.secs||[]).forEach(function(s){s.items.forEach(function(x){if(x.n===n)it=x;});});
      if(!it)return;
      if(it.etat==='lock'){if(el){el.classList.remove('pgsk');void el.offsetWidth;el.classList.add('pgsk');}toast(it.msg||'Pas encore disponible.');return;}
      LK.ev({a:'pg',k:'item',i:n});
    },
    retour:function(){LK.ev({a:'pg',k:'retour'});},
    btn:function(k){LK.ev({a:'pg',k:'btn',v:k});},
    toast:toast
  };
})();
"""
