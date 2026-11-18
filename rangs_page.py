# -*- coding: utf-8 -*-
"""
rangs_page.py — popup de promotion « enflammé » (palettes qui changent de position en continu),
menu Évolution (jauges professionnelles, liste des rangs avec badges, maîtrise des chapitres,
graphiques personnalisables, classement / rivalité). Fragments CSS / HTML / JS ajoutés à la page de Locky.
"""

CSS = r"""
#evo,#rang{display:none;position:absolute;inset:0}
body.m-evo #evo{display:block}
body.m-rang #rang,body.m-rangm #rang{display:block}
.pal.pt i.on{background:var(--pc);border-color:var(--pc);box-shadow:0 0 6px var(--pc)}

/* ================= POPUP DE PROMOTION ================= */
#rang{overflow:hidden;background:radial-gradient(ellipse at 50% 55%,#1a0a24 0%,#07040f 70%);color:#fff}
#rang::after{content:"";position:absolute;inset:0;pointer-events:none;background:repeating-linear-gradient(0deg,rgba(0,0,0,.18) 0 2px,transparent 2px 4px)}
#feu{position:absolute;inset:0;width:100%;height:100%}
#rayons{position:absolute;left:50%;top:44%;width:150vmax;height:150vmax;margin:-75vmax 0 0 -75vmax;opacity:.38;
 background:repeating-conic-gradient(from 0deg,var(--pc) 0 5deg,transparent 5deg 15deg);
 -webkit-mask-image:radial-gradient(circle,#000 0,transparent 45%);mask-image:radial-gradient(circle,#000 0,transparent 45%);animation:tourne 14s linear infinite}
@keyframes tourne{to{transform:rotate(360deg)}}
.rg{position:relative;z-index:2;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:16px}
.rg .top{font-size:11px;letter-spacing:.26em;color:var(--cy);animation:glitch 2.6s infinite}
.rg h1{margin:6px 0 14px;font-size:34px;letter-spacing:.14em;color:#fff;text-shadow:0 0 18px var(--pc),0 0 40px var(--pc);animation:glitch 3.1s infinite .4s}
@keyframes glitch{0%,92%,100%{transform:none;filter:none}93%{transform:translate(-3px,1px);filter:hue-rotate(60deg)}95%{transform:translate(3px,-1px);filter:hue-rotate(-60deg)}97%{transform:translate(-1px,0)}}
.bwrap{position:relative;width:min(58vw,230px);aspect-ratio:1;display:grid;place-items:center;animation:entre .9s cubic-bezier(.2,1.5,.35,1) both,flotte 3s ease-in-out .9s infinite}
@keyframes entre{from{transform:scale(.05) rotate(-200deg);opacity:0;filter:blur(12px)}to{transform:none;opacity:1;filter:none}}
@keyframes flotte{50%{transform:translateY(-9px)}}
.bwrap img,.bwrap .emb{width:100%;height:100%;object-fit:contain;filter:drop-shadow(0 0 18px var(--pc)) drop-shadow(0 0 40px var(--pc))}
.onde{position:absolute;inset:0;border-radius:50%;border:3px solid var(--pc);opacity:0;animation:onde 2.2s ease-out infinite}
.onde.b{animation-delay:1.1s}
@keyframes onde{from{transform:scale(.6);opacity:.9}to{transform:scale(2.3);opacity:0}}
.rg .txt{display:flex;flex-direction:column;align-items:center}
.rg .nom{margin-top:16px;font-size:30px;font-weight:900;letter-spacing:.1em;color:var(--pc);text-shadow:0 0 14px var(--pc);animation:monte .6s .5s both}
.rg .tit{font-size:12px;letter-spacing:.35em;color:#ffd98a;margin-top:2px;animation:monte .6s .65s both}
.rg .sub{margin-top:12px;font-size:12px;color:#cfd2f5;line-height:1.6;animation:monte .6s .8s both}
.rg .jau{width:min(80vw,320px);margin-top:12px;animation:monte .6s .95s both}
.rg .go{margin-top:18px;font-size:11px;letter-spacing:.3em;color:var(--mut);animation:clig 1.4s infinite}
@keyframes monte{from{transform:translateY(18px);opacity:0}to{transform:none;opacity:1}}
@keyframes clig{50%{opacity:.25}}
.div{display:inline-block;margin-top:8px;padding:4px 12px;border:1px solid var(--pc);color:var(--pc);font-size:11px;letter-spacing:.25em;border-radius:3px;animation:monte .6s .3s both,puls 1.4s 1s infinite}
/* version compacte (entraînement : ne coupe rien) */
#rang.mini{background:linear-gradient(90deg,#1b0c26,#0a0612 70%);border:2px solid var(--pc);border-radius:10px;box-shadow:0 0 18px var(--pc)}
#rang.mini #rayons,#rang.mini .onde,#rang.mini .jau,#rang.mini .sub,#rang.mini .div{display:none}
#rang.mini .go{margin-top:4px;font-size:9px;letter-spacing:.2em}
#rang.mini .rg{flex-direction:row;justify-content:flex-start;gap:14px;text-align:left;padding:8px 14px}
#rang.mini .bwrap{width:84px;flex:none;animation:entre .7s cubic-bezier(.2,1.5,.35,1) both}
#rang.mini h1{font-size:15px;margin:0 0 2px}
#rang.mini .top{display:none}
#rang.mini .nom{margin:0;font-size:20px}
#rang.mini .tit{margin:0}
#rang.mini .txt{flex:1;min-width:0;align-items:flex-start}

/* ================= ÉVOLUTION ================= */
.hero{position:relative;padding:14px;margin-bottom:12px;border:1px solid var(--pc);border-radius:6px;overflow:hidden;
 background:linear-gradient(135deg,rgba(255,255,255,.04),transparent 60%),#0f0d20}
.hero::before{content:"";position:absolute;inset:-40%;background:conic-gradient(from 0deg,transparent 0 70%,var(--pc) 85%,transparent 100%);opacity:.16;animation:tourne 7s linear infinite}
.hero>*{position:relative}
.hrow{display:flex;gap:14px;align-items:center}
.hbadge{width:104px;height:104px;flex:none}
.hbadge img,.hbadge .emb{width:100%;height:100%;object-fit:contain;filter:drop-shadow(0 0 12px var(--pc))}
.hnom{font-size:22px;font-weight:900;letter-spacing:.06em;color:var(--pc);text-shadow:0 0 12px var(--pc)}
.htit{font-size:11px;letter-spacing:.25em;color:#ffd98a;margin-top:2px}
.hrp{font-size:12px;color:#cfd2f5;margin-top:6px}.hrp b{font-size:18px;color:#fff}
.tag{display:inline-block;padding:2px 8px;border:1px solid;border-radius:3px;font-size:10px;letter-spacing:.14em;margin:6px 6px 0 0}
.k4{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px}
.rival{padding:10px;border:1px solid var(--ro);border-left:4px solid var(--ro);border-radius:4px;background:rgba(255,59,92,.07);font-size:12px;line-height:1.55;margin-bottom:12px}
.rival b{color:#fff}
.tierh{display:flex;align-items:center;gap:10px;margin:16px 0 6px;padding:8px 10px;border-radius:4px;background:linear-gradient(90deg,var(--pc),transparent);color:#fff;font-weight:900;letter-spacing:.14em;font-size:13px}
.tierh img,.tierh .emb{width:34px;height:34px;object-fit:contain}
.tierh small{margin-left:auto;font-weight:400;font-size:10px;letter-spacing:.08em;opacity:.85}
.rr{display:flex;align-items:center;gap:12px;padding:8px 10px;margin-bottom:6px;border:1px solid #2b2650;border-radius:4px;background:#0f0d20;position:relative}
.rr .bi{width:46px;height:46px;flex:none;display:grid;place-items:center}
.rr .bi img,.rr .bi .emb{width:100%;height:100%;object-fit:contain}
.rr .rn{flex:1;min-width:0;font-size:14px;font-weight:800}
.rr .rn small{display:block;font-weight:400;font-size:10px;color:var(--mut);margin-top:2px}
.rr .st{flex:none;font-size:10px;letter-spacing:.12em;padding:3px 7px;border:1px solid;border-radius:3px}
.rr.ok{border-color:rgba(57,255,136,.35)}.rr.ok .st{color:var(--ok)}
.rr.cur{border-color:var(--pc);box-shadow:0 0 14px var(--pc),inset 0 0 12px rgba(255,255,255,.04);background:#17122c}
.rr.cur .st{color:var(--pc);animation:puls 1.2s infinite}
.rr{touch-action:manipulation}
.rr.sec{animation:none}
@keyframes secoue{25%{transform:translateX(-5px)}75%{transform:translateX(5px)}}
.rr.sk{animation:secoue .3s}
.rr.lock{opacity:.55}.rr.lock .bi img,.rr.lock .bi .emb{filter:grayscale(1) brightness(.6)}.rr.lock .st{color:var(--mut)}
@keyframes puls{50%{opacity:.45}}
.rr .jauge{position:absolute;left:68px;right:10px;bottom:4px}
.emb{display:grid;place-items:center;font-weight:900;color:#fff;background:linear-gradient(145deg,var(--pc),#120a22 85%);
 clip-path:polygon(50% 0,93% 25%,93% 75%,50% 100%,7% 75%,7% 25%);font-size:1.1em;text-shadow:0 0 6px #000}
.chr{padding:10px;margin-bottom:8px;border:1px solid #2b2650;border-radius:4px;background:#0f0d20}
.chr .l{display:flex;justify-content:space-between;align-items:baseline;gap:8px;font-size:13px}
.chr .l b{font-size:18px}
.chr .m{font-size:10px;letter-spacing:.14em;margin-top:2px}
.pod{display:flex;align-items:center;gap:10px;padding:8px 10px;margin-bottom:6px;border:1px solid #2b2650;border-radius:4px;background:#0f0d20}
.pod .p{flex:none;width:30px;text-align:center;font-size:16px;font-weight:900;color:var(--mut)}
.pod.p1{border-color:#ffc93c;background:linear-gradient(90deg,rgba(255,201,60,.18),#0f0d20)}.pod.p1 .p{color:#ffc93c}
.pod.p2{border-color:#cdd6e6}.pod.p2 .p{color:#cdd6e6}.pod.p3{border-color:#d9823b}.pod.p3 .p{color:#d9823b}
.pod.moi{border-color:var(--cy);box-shadow:0 0 12px var(--cy);background:#10213a}
.pod .bi{width:40px;height:40px;flex:none}.pod .bi img,.pod .bi .emb{width:100%;height:100%;object-fit:contain}
.pod .n{flex:1;min-width:0;font-size:13px;font-weight:800;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pod .n small{display:block;font-weight:400;font-size:10px;color:var(--mut)}
.pod .r{flex:none;font-size:15px;font-weight:900;color:var(--cy)}
.chart{padding:10px;border:1px solid rgba(0,240,255,.35);border-radius:4px;background:#0b0a1a;margin-bottom:10px}
.chart svg{width:100%;height:auto;display:block}
#zbox{overflow:hidden;touch-action:pan-y;border-radius:4px;background:#080716}
#gsvg line,#gsvg polygon{vector-effect:non-scaling-stroke}
.chart.fs{position:fixed;inset:0;z-index:20;margin:0;border-radius:0;padding:14px;background:#06050f;display:flex;flex-direction:column}
.chart.fs #zbox{flex:1;display:flex;align-items:center}
.chart.fs #gsvg{width:100%;height:100%}
.zc{display:flex;align-items:center;gap:8px;margin-top:8px}.zc input{flex:1;margin:0}.zc .bt{padding:5px 11px}.zc b{flex:none;width:44px;text-align:right;color:var(--cy);font-size:13px}
.chart .leg{display:flex;flex-wrap:wrap;gap:6px 12px;font-size:11px;margin-top:6px}
.chart .leg i{display:inline-block;width:10px;height:10px;margin-right:5px;transform:skewX(-18deg)}
.draw{stroke-dasharray:1200;stroke-dashoffset:1200;animation:trace 1.4s ease-out forwards}
@keyframes trace{to{stroke-dashoffset:0}}
.grow{transform-box:fill-box;transform-origin:bottom;animation:pousse .7s cubic-bezier(.2,1.2,.4,1) both}
.growx{transform-box:fill-box;transform-origin:left;animation:poussex .7s cubic-bezier(.2,1.2,.4,1) both}
@keyframes pousse{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes poussex{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.optg{margin:8px 0 4px;font-size:10px;letter-spacing:.2em;color:var(--mg)}
.optg:first-child{margin-top:0}
.opts .o{padding:6px 9px}
"""

HTML = r"""
<div id="evo" class="cadre"><div class="int">
  <div class="tete"><div class="bt" id="eBack" onclick="R.retour()">‹</div><div class="t" id="eTitre">ÉVOLUTION</div><div class="bt x" onclick="LK.fermer()">✕</div></div>
  <div class="corps" id="ecorps"></div>
</div></div>

<div id="rang" onclick="R.fin()"><div id="rayons"></div><canvas id="feu"></canvas><div class="rg" id="rg"></div></div>
"""

JS = r"""
var R=(function(){
  var vue='home',tmr=null,anim=null,pp=null;
  var TITRES={home:'ÉVOLUTION',grade:'MON GRADE & RYTHME',rangs:'LISTE DES RANGS',chap:'MAÎTRISE DES CHAPITRES',graph:'GRAPHIQUES & STATS',clas:'CLASSEMENT & RIVALITÉ'};
  function $(i){return document.getElementById(i);}
  function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function D(){return (LK.etat().rangs)||{liste:[],idx:0,rp:0,rp_in:0,seuil:10,total_rp:0,hist:[],notes:[],chap:[],cfg:{},clas:{}};}
  function pct(a,b){return b?Math.round(100*a/b):0;}

  /* ---------- badge (image du dossier badges/, sinon emblème de secours) ---------- */
  function emb(r,px){return '<div class="emb" style="--pc:'+r.col+';width:'+px+'px;height:'+px+'px;font-size:'+Math.round(px*.34)+'px">'+(r.v?['','I','II','III','IV','V'][r.v]:'★')+'</div>';}
  function badge(r,px,cls){
    if(!r)return '';
    if(!r.b)return emb(r,px);
    return '<img src="'+esc(r.b)+'" alt="" style="--pc:'+r.col+'" data-i="'+r.i+'" data-px="'+px+'" onerror="R.err(this)">';
  }
  function err(img){var L=D().liste,r=L[parseInt(img.getAttribute('data-i'),10)];if(!r)return;var d=document.createElement('div');d.innerHTML=emb(r,parseInt(img.getAttribute('data-px'),10)||60);img.parentNode.replaceChild(d.firstChild,img);}

  /* ================== POPUP DE PROMOTION ================== */
  function promo(p){
    stop();pp=p;var el=$('rang');
    el.className=p.mini?'mini':'';el.style.setProperty('--pc',p.col);
    var r={i:p.idx,n:p.nom,t:p.tier,v:p.niv,b:p.b,col:p.col};
    var jau=pal(p.replay?100:Math.round(100*p.rp_in/Math.max(1,p.seuil)),'pt',20,'g');
    $('rg').innerHTML=
      '<div class="bwrap"><div class="onde"></div><div class="onde b"></div>'+badge(r,p.mini?84:200)+'</div>'+
      '<div class="txt"><div class="top">'+(p.replay?'// REPLAY · RANG DÉBLOQUÉ //':'// NOUVEAU RANG DÉBLOQUÉ //')+'</div><h1>'+(p.division?'NOUVELLE DIVISION':'PROMOTION')+'</h1>'+
      (p.division&&!p.mini?'<div class="div">'+esc(p.tier.toUpperCase())+'</div>':'')+
      '<div class="nom">'+esc(p.nom.toUpperCase())+'</div><div class="tit">'+esc((p.titre||'').toUpperCase())+'</div>'+
      '<div class="sub">Rang '+(p.idx+1)+' / '+p.total+(p.nb>1?' · +'+p.nb+' rangs d\'un coup':'')+'<br>'+(p.replay?'Débloqué à '+p.cumul+' RP cumulés':p.total_rp+' RP · prochain rang dans '+Math.max(0,p.seuil-p.rp_in)+' RP')+'</div>'+
      '<div class="jau">'+jau+'</div><div class="go">'+(p.mini?'TOUCHE POUR FERMER':'TOUCHE POUR CONTINUER')+'</div></div>';
    feu(p.col,p.mini);
  }
  function fin(){if(!pp)return;stop();LK.ev({a:'rang_fin'});}
  function stop(){if(tmr){clearTimeout(tmr);tmr=null;}if(anim){cancelAnimationFrame(anim);anim=null;}pp=null;}

  /* palettes de feu : petits rectangles qui montent, vacillent et changent de position en permanence */
  function feu(col,mini){
    var cv=$('feu'),ctx=cv.getContext('2d'),dpr=Math.min(window.devicePixelRatio||1,2),W,H;
    function mesure(){W=cv.width=Math.max(1,cv.clientWidth*dpr);H=cv.height=Math.max(1,cv.clientHeight*dpr);}
    mesure();
    var N=mini?46:150,P=[],t=0,cx,cy;
    function nouv(rand){return {x:Math.random()*W,y:rand?Math.random()*H:H+12*dpr,vx:(Math.random()-.5)*.7*dpr,vy:-(2+Math.random()*4.6)*dpr,
      s:(3+Math.random()*8)*dpr,l:rand?Math.random()*90:0,m:90+Math.random()*120,ph:Math.random()*6.28,rot:(Math.random()-.5)*.5};}
    for(var i=0;i<N;i++)P.push(nouv(true));
    var ORB=mini?10:34,O=[];for(var j=0;j<ORB;j++)O.push({a:Math.random()*6.28,r:.5+Math.random()*.5,v:(Math.random()<.5?-1:1)*(.01+Math.random()*.03),s:(2+Math.random()*4)*dpr});
    function teinte(k){      /* jaune -> orange -> rouge -> magenta -> violet sombre */
      var h=k<.35?55-k*90:(k<.7?24-(k-.35)*40:350-(k-.7)*100);return 'hsl('+h+',100%,'+(60-k*28)+'%)';}
    function boucle(){
      var cw=(cv.clientWidth*dpr)|0,ch=(cv.clientHeight*dpr)|0;if(cw&&ch&&(cw!==W||ch!==H)){W=cv.width=cw;H=cv.height=ch;}   /* la vue native peut être redimensionnée après le début */
      t++;ctx.globalCompositeOperation='source-over';ctx.clearRect(0,0,W,H);ctx.globalCompositeOperation='lighter';
      for(var i=0;i<P.length;i++){var p=P[i];p.l++;p.x+=p.vx+Math.sin(t*.07+p.ph)*.9*dpr;p.y+=p.vy;p.s*=.992;
        if(p.l>p.m||p.y<-20||p.s<1){P[i]=p=nouv(false);}
        var k=p.l/p.m;ctx.globalAlpha=Math.max(0,1-k)*.9;ctx.fillStyle=teinte(k);
        ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.rot+t*.02*(i%2?1:-1));ctx.fillRect(-p.s/2,-p.s*.9,p.s,p.s*1.8);ctx.restore();}
      cx=W/2;cy=mini?H/2:H*.44;
      for(var o=0;o<O.length;o++){var q=O[o];q.a+=q.v;var rr=(mini?H*.5:Math.min(W,H)*.27)*(q.r+Math.sin(t*.05+o)*.08);
        var x=cx+Math.cos(q.a)*rr+(Math.random()-.5)*3*dpr,y=cy+Math.sin(q.a)*rr*(mini?1:1.05)+(Math.random()-.5)*3*dpr;
        ctx.globalAlpha=.55+.4*Math.sin(t*.2+o);ctx.fillStyle=col;ctx.fillRect(x,y,q.s,q.s*1.7);}
      anim=requestAnimationFrame(boucle);
    }
    boucle();
  }

  /* ================== ÉVOLUTION ================== */
  function cat(t){return '<div class="cat">'+t+'</div>';}
  function carte(ic,t,s,clic,cls){return '<div class="pc '+(cls||'')+'" onclick="'+clic+'"><span class="ic">'+ic+'</span><span class="tx"><b>'+t+'</b>'+(s?'<small>'+s+'</small>':'')+'</span><span class="ch">›</span></div>';}
  function cur(){var d=D();return d.liste[d.idx]||{col:'#00f0ff',n:'—',t:'',v:1,i:0};}
  function kpi(v,l,c){return '<div class="kpi '+(c||'')+'"><b>'+v+'</b><span>'+l+'</span></div>';}
  function precision(d){var ok=0,t=0;(d.chap||[]).forEach(function(c){ok+=c[1];t+=c[2];});return {ok:ok,t:t,p:pct(ok,t)};}

  function vHome(d){
    var r=cur(),pr=precision(d),suiv=d.liste[d.idx+1],reste=Math.max(0,d.seuil-d.rp_in),c=d.clas||{};
    var h='<div class="hero" style="--pc:'+r.col+'"><div class="hrow"><div class="hbadge">'+badge(r,104)+'</div><div style="min-width:0">'+
      '<div class="hnom">'+esc(r.n.toUpperCase())+'</div><div class="htit">'+esc((r.ti||'').toUpperCase())+'</div>'+
      '<div class="hrp"><b>'+d.total_rp+'</b> RP au total</div>'+
      '<span class="tag" style="color:'+r.col+';border-color:'+r.col+'">RANG '+(d.idx+1)+'/'+d.liste.length+'</span>'+
      (c.pos?'<span class="tag" style="color:var(--cy);border-color:var(--cy)">#'+c.pos+' CLASSEMENT</span>':'')+'</div></div>'+
      '<div class="jl" style="--pc:'+r.col+';margin-top:12px"><span>'+(suiv?'VERS '+esc(suiv.n.toUpperCase()):'RANG MAXIMAL')+'</span><b style="color:'+r.col+'">'+d.rp_in+' / '+d.seuil+'</b></div>'+
      pal(Math.round(100*d.rp_in/Math.max(1,d.seuil)),'pt',20,'g')+
      '<div class="mut">'+(suiv?reste+' RP pour monter en <b style="color:#fff">'+esc(suiv.n)+'</b>':'Tu as atteint le sommet : défends ta place !')+'</div></div>'+
      '<div class="k4">'+kpi(pr.p+'%','Précision globale','v')+kpi(pr.t,'Réponses analysées','')+kpi(d.best_rp||0,'Meilleur score RP','o')+kpi((d.jours||0)+' j','Jours connectés','m')+'</div>';
    if(c.rival){h+='<div class="rival">⚔️ <b>RIVAL : '+esc(c.rival.nom)+'</b> ('+esc(c.rival.rang)+')<br>'+
      (c.rival.devant?'Il te devance de <b>'+c.rival.ecart+' RP</b> : rattrape-le !':'Tu le devances de <b>'+c.rival.ecart+' RP</b> : il te poursuit, ne lâche rien !')+'</div>';}
    return h+cat('Mon espace')+
      carte('🏆','Mon grade, XP & rythme','Progression, rythme et projection',"R.go('grade')",'or')+
      carte('🎬','Mes animations débloquées',(d.idx+1)+' animation(s) de promotion à revoir quand tu veux',"R.go('rangs')",'mg')+
      carte('📜','Liste officielle des rangs','51 rangs avec leurs badges',"R.go('rangs')",'')+
      carte('🧠','Maîtrise des chapitres','Jauges par chapitre, tri, niveaux',"R.go('chap')",'ok')+
      carte('📊','Graphiques & statistiques','Courbes, barres, radar, anneau — personnalisables',"R.go('graph')",'')+
      carte('⚔️','Classement & rivalité','Top joueurs, ta position, ton rival',"R.go('clas')",'ko');
  }

  function vGrade(d){
    var r=cur(),pr=precision(d),ry=d.rythme||[0,0],g=ry[0],suiv=d.liste[d.idx+1],reste=Math.max(0,d.seuil-d.rp_in);
    var proj=(g>0&&suiv)?Math.ceil(reste/g):null;
    return '<div class="hero" style="--pc:'+r.col+'"><div class="hrow"><div class="hbadge">'+badge(r,104)+'</div><div><div class="hnom">'+esc(r.n.toUpperCase())+'</div><div class="htit">'+esc((r.ti||'').toUpperCase())+'</div></div></div></div>'+
      '<div class="sec"><h3>Progression du rang</h3><div class="jl" style="--pc:'+r.col+'"><span>RP DANS CE RANG</span><b style="color:'+r.col+'">'+d.rp_in+'/'+d.seuil+'</b></div>'+
      pal(Math.round(100*d.rp_in/Math.max(1,d.seuil)),'pt',20,'g')+
      '<div class="jl cy" style="margin-top:12px"><span>PROGRESSION GLOBALE</span><b>'+Math.round(100*d.idx/Math.max(1,d.liste.length-1))+'%</b></div>'+pal(100*d.idx/Math.max(1,d.liste.length-1),'cy',20,'g')+'</div>'+
      '<div class="sec"><h3>Rythme actuel</h3><div class="k4" style="margin:0">'+
        kpi((g>0?'+':'')+g,'RP / réponse (30 dernières)',g>0?'v':'m')+kpi((ry[1]>0?'+':'')+ry[1]+' RP','Tendance récente',ry[1]>=0?'v':'m')+
        kpi(d.total_rp,'RP total','o')+kpi(d.niveau_profil||1,'Niveau de profil','m')+'</div>'+
      '<div class="mut" style="margin-top:8px">'+(proj?'À ce rythme : <b style="color:#fff">~'+proj+' réponses</b> avant '+esc(suiv.n)+'.':(suiv?'Réponds juste pour relancer ta progression.':'Rang maximal atteint.'))+'</div></div>'+
      '<div class="sec"><h3>Précision</h3><div class="jl ok"><span>RÉUSSITE</span><b>'+pr.p+'%</b></div>'+pal(pr.p,'ok',20,'g')+
      '<div class="jl ko"><span>ÉCHEC</span><b>'+(pr.t?100-pr.p:0)+'%</b></div>'+pal(pr.t?100-pr.p:0,'ko',20,'g')+'</div>';
  }

  function vRangs(d){
    var h='<div class="stat">Chaque rang demande 10 RP, +5 % à chaque nouvelle couleur. Les rangs verrouillés sont grisés.</div>',t='';
    d.liste.forEach(function(r){
      if(r.t!==t){t=r.t;var prem=d.liste.filter(function(x){return x.t===r.t;});
        h+='<div class="tierh" style="--pc:'+r.col+'">'+badge(prem[0],34)+'<span>'+esc(r.t.toUpperCase())+'</span><small>'+esc(r.ti)+' · dès '+prem[0].c+' RP</small></div>';}
      var etat=r.i<d.idx?'ok':(r.i===d.idx?'cur':'lock');
      h+='<div class="rr '+etat+'" id="rr'+r.i+'" style="--pc:'+r.col+'" onclick="'+(etat==='lock'?'R.verrou(this)':'R.revoir('+r.i+')')+'"><div class="bi">'+badge(r,46)+'</div><div class="rn">'+esc(r.n)+'<small>dès '+r.c+' RP · '+(etat==='lock'?r.s+' RP pour passer':'▶ touche pour revoir l\'animation')+'</small>'+(etat==='cur'?'<div style="margin-top:5px">'+pal(Math.round(100*d.rp_in/Math.max(1,d.seuil)),'pt',20,'s')+'</div>':'')+'</div>'+
        '<div class="st">'+(etat==='ok'?'✔ DÉBLOQUÉ':(etat==='cur'?'◉ ACTUEL':'🔒 VERROUILLÉ'))+'</div>'+'</div>';
    });
    return h;
  }

  var tri='desc';
  var Z={z:1,x:0,y:0};
  function niveau(p,t){return t<3?['Novice','mut']:(p>=85?['MAÎTRE','ok']:(p>=65?['EXPERT','cy']:(p>=40?['CONFIRMÉ','or']:['APPRENTI','ko'])));}
  function vChap(d){
    var L=(d.chap||[]).map(function(c){return {n:c[0],ok:c[1],t:c[2],p:pct(c[1],c[2])};});
    if(!L.length)return '<div class="stat off">Aucun chapitre joué pour le moment. Réponds à quelques questions !</div>';
    L.sort(tri==='asc'?function(a,b){return a.p-b.p;}:(tri==='vol'?function(a,b){return b.t-a.t;}:function(a,b){return b.p-a.p;}));
    var h='<div class="opts" style="margin-bottom:10px">'+[['desc','Meilleurs'],['asc','À travailler'],['vol','Plus joués']].map(function(o){return '<div class="o'+(tri===o[0]?' on':'')+'" onclick="R.tri(\''+o[0]+'\')">'+o[1]+'</div>';}).join('')+'</div>';
    L.forEach(function(c){var nv=niveau(c.p,c.t),cl=c.p>=80?'ok':(c.p>=50?'cy':(c.p>=30?'or':'ko'));
      h+='<div class="chr"><div class="l"><span>'+esc(c.n)+'</span><b style="color:var(--'+(cl==='ok'?'ok':cl==='cy'?'cy':cl==='or'?'or':'ro')+')">'+c.p+'%</b></div>'+pal(c.p,cl,20,'s')+
        '<div class="m" style="color:var(--'+(nv[1]==='ok'?'ok':nv[1]==='cy'?'cy':nv[1]==='or'?'or':nv[1]==='mut'?'mut':'ro')+')">'+nv[0]+' · '+c.ok+'/'+c.t+' bonnes réponses</div></div>';});
    return h;
  }

  /* ---------------- classement ---------------- */
  function vClas(d){
    var c=d.clas||{};
    if(c.hors_ligne)return '<div class="stat off">○ Hors ligne : le classement mondial demande une connexion Internet et un compte.<br>Ton rang local : <b>'+esc(cur().n)+'</b> · '+d.total_rp+' RP.</div>';
    if(!c.charge)return '<div class="stat">Chargement du classement…</div>';
    if(!c.lignes||!c.lignes.length)return '<div class="stat off">Le classement est vide pour le moment.</div>';
    var h='<div class="stat">⚔️ Top '+c.lignes.length+' des joueurs'+(c.pos?' · <b>tu es #'+c.pos+'</b>':' · tu n\'es pas encore dans le top '+c.lignes.length)+'</div>';
    if(c.rival)h+='<div class="rival">🎯 <b>'+esc(c.rival.nom)+'</b> : '+(c.rival.devant?'à <b>'+c.rival.ecart+' RP</b> devant toi.':'<b>'+c.rival.ecart+' RP</b> derrière toi.')+'</div>';
    c.lignes.forEach(function(r){
      var rr={i:0,n:r.rang,t:r.t,v:r.v,b:r.b,col:r.col};
      h+='<div class="pod p'+(r.pos<=3?r.pos:'')+(r.moi?' moi':'')+'" style="--pc:'+r.col+'"><div class="p">'+(r.pos===1?'🥇':r.pos===2?'🥈':r.pos===3?'🥉':r.pos)+'</div><div class="bi">'+badge(rr,40)+'</div>'+
        '<div class="n">'+esc(r.nom)+(r.moi?' <span style="color:var(--cy)">(TOI)</span>':'')+(r.on?' <span style="color:var(--ok)">●</span>':'')+'<small>'+esc(r.rang)+(r.classe?' · '+esc(r.classe):'')+'</small></div><div class="r">'+r.rp+'</div></div>';});
    return h;
  }

  /* ---------------- graphiques personnalisables ---------------- */
  var PAL={neon:['#00f0ff','#ff2bd6','#39ff88','#ffb000','#9d6bff','#ff3b5c','#3d8bff','#ffe94a'],
           feu:['#ffe08a','#ffb000','#ff7a00','#ff3b5c','#c1169f','#9d6bff','#ff9a3c','#ff5d8f'],
           toxique:['#39ff88','#b6ff3a','#00f0b0','#e6ff6b','#1fbf6b','#7dffb4','#00d4aa','#a8ff78'],
           glace:['#6fe6ff','#5aa2ff','#9ad7ff','#c5b3ff','#00b8d4','#3d8bff','#a0f0ff','#7a8cff'],
           arc:['#ff3b5c','#ffb000','#ffe94a','#39ff88','#00f0ff','#3d8bff','#9d6bff','#ff2bd6']};
  var DEF={m:'rp',type:'aire',pal:'neon',plage:50,top:8,tri:'desc',grille:true,points:true,valeurs:false,lisse:true,multi:false};
  function cfg(){var d=D(),c=d.cfg||{},o={};for(var k in DEF)o[k]=(c[k]!==undefined)?c[k]:DEF[k];return o;}
  function r1(x){return Math.round(x*10)/10;}
  function courbe(pts,lis){
    if(pts.length<2)return 'M'+pts[0][0]+','+pts[0][1];
    if(!lis||pts.length<3)return 'M'+pts.map(function(p){return r1(p[0])+','+r1(p[1]);}).join('L');
    var d='M'+r1(pts[0][0])+','+r1(pts[0][1]);
    for(var i=0;i<pts.length-1;i++){var p0=pts[i-1]||pts[i],p1=pts[i],p2=pts[i+1],p3=pts[i+2]||p2;
      d+='C'+r1(p1[0]+(p2[0]-p0[0])/6)+','+r1(p1[1]+(p2[1]-p0[1])/6)+' '+r1(p2[0]-(p3[0]-p1[0])/6)+','+r1(p2[1]-(p3[1]-p1[1])/6)+' '+r1(p2[0])+','+r1(p2[1]);}
    return d;
  }
  function serie(c,d){
    var m=c.m,v=[],lab=[],unit='',seq=false,pc=false;
    function chap(tp){var L=(d.chap||[]).map(function(x){return {n:x[0],ok:x[1],t:x[2],p:pct(x[1],x[2])};});
      L.sort(c.tri==='asc'?function(a,b){return (tp?a.t-b.t:a.p-b.p);}:(c.tri==='alpha'?function(a,b){return a.n<b.n?-1:1;}:function(a,b){return (tp?b.t-a.t:b.p-a.p);}));
      if(c.top>0)L=L.slice(0,c.top);return L;}
    if(m==='rp'||m==='notes'){var s=(m==='rp'?d.hist:d.notes)||[];if(c.plage>0)s=s.slice(-c.plage);v=s;lab=s.map(function(_,i){return String(i+1);});unit=(m==='rp'?' RP':'/20');seq=true;}
    else if(m==='reussite'){var L=chap(false);v=L.map(function(x){return x.p;});lab=L.map(function(x){return x.n;});unit='%';pc=true;}
    else if(m==='volume'){var L2=chap(true);v=L2.map(function(x){return x.t;});lab=L2.map(function(x){return x.n;});unit='';}
    else{var pr=precision(d);v=[pr.ok,pr.t-pr.ok];lab=['Réussites','Échecs'];unit='';}
    return {v:v,lab:lab,unit:unit,seq:seq,pc:pc,split:m==='split',m:m};
  }
  function chart(c,d){
    var S=serie(c,d),col=PAL[c.pal]||PAL.neon,type=c.type;
    if(!S.v.length)return '<div class="mut" style="padding:20px;text-align:center">Pas encore assez de données pour ce graphique.</div>';
    if(S.split&&type!=='barres')type='anneau';
    if(!S.seq&&!S.split&&type==='anneau'&&S.m==='reussite')type='barres';
    if(type==='radar'&&(S.seq||S.split||S.v.length<3))type='barres';
    if(S.seq&&(type==='radar'||type==='anneau'))type='aire';
    var W=320,H=210,mx=Math.max.apply(null,S.v.concat([1])),max=S.pc?100:(S.m==='notes'?20:mx*1.1),svg='',leg='';
    var main=col[0],FX=W/2,FY=H/2;
    var defs='<defs><linearGradient id="gA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="'+main+'" stop-opacity=".55"/><stop offset="1" stop-color="'+main+'" stop-opacity="0"/></linearGradient>'+
      '<linearGradient id="gB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="'+main+'"/><stop offset="1" stop-color="'+col[1]+'"/></linearGradient>'+
      '<filter id="lueur"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>';
    if(type==='ligne'||type==='aire'){
      var L=34,Rm=10,T=14,B=26,w=W-L-Rm,h=H-T-B,n=S.v.length;
      var pts=S.v.map(function(y,i){return [L+(n>1?w*i/(n-1):w/2),T+h-(h*y/max)];});
      if(c.grille){for(var g=0;g<=4;g++){var yy=T+h*g/4;svg+='<line x1="'+L+'" y1="'+yy+'" x2="'+(W-Rm)+'" y2="'+yy+'" stroke="#2b2650" stroke-width=".7"/><text x="'+(L-5)+'" y="'+(yy+3)+'" fill="#8a8fb8" font-size="8" text-anchor="end">'+Math.round(max*(1-g/4))+'</text>';}}
      FX=pts[pts.length-1][0];FY=pts[pts.length-1][1];       /* le zoom vise d'abord le dernier point (ta progression récente) */
      var d1=courbe(pts,c.lisse);
      if(type==='aire')svg+='<path d="'+d1+'L'+pts[pts.length-1][0]+','+(T+h)+'L'+pts[0][0]+','+(T+h)+'Z" fill="url(#gA)"/>';
      svg+='<path class="draw" d="'+d1+'" fill="none" stroke="'+main+'" stroke-width="2.2" filter="url(#lueur)" pathLength="1200"/>';
      if(c.points||c.valeurs)pts.forEach(function(p,i){if(n>40&&i%Math.ceil(n/20))return;if(c.points)svg+='<circle cx="'+r1(p[0])+'" cy="'+r1(p[1])+'" r="2.6" fill="#0b0a1a" stroke="'+col[1]+'" stroke-width="1.5"/>';
        if(c.valeurs&&n<=14)svg+='<text x="'+r1(p[0])+'" y="'+r1(p[1]-6)+'" fill="#fff" font-size="8" text-anchor="middle">'+S.v[i]+'</text>';});
      var step=Math.ceil(n/6);S.lab.forEach(function(t,i){if(i%step===0||i===n-1)svg+='<text x="'+r1(pts[i][0])+'" y="'+(H-8)+'" fill="#8a8fb8" font-size="8" text-anchor="middle">'+esc(t.length>9?t.slice(0,8)+'…':t)+'</text>';});
    }else if(type==='barres'&&S.seq){
      var L2=34,Rm2=10,T2=14,B2=26,w2=W-L2-Rm2,h2=H-T2-B2,n2=S.v.length,bw=Math.max(2,Math.min(26,w2/n2-2));
      if(c.grille){for(var g2=0;g2<=4;g2++){var y2=T2+h2*g2/4;svg+='<line x1="'+L2+'" y1="'+y2+'" x2="'+(W-Rm2)+'" y2="'+y2+'" stroke="#2b2650" stroke-width=".7"/><text x="'+(L2-5)+'" y="'+(y2+3)+'" fill="#8a8fb8" font-size="8" text-anchor="end">'+Math.round(max*(1-g2/4))+'</text>';}}
      S.v.forEach(function(y,i){var x=L2+(w2*(i+.5)/n2)-bw/2,hh=Math.max(1,h2*y/max);
        svg+='<rect class="grow" style="animation-delay:'+Math.min(i*20,500)+'ms" x="'+r1(x)+'" y="'+r1(T2+h2-hh)+'" width="'+bw+'" height="'+r1(hh)+'" fill="'+(c.multi?col[i%col.length]:'url(#gB)')+'" rx="1.5"/>';
        if(c.valeurs&&n2<=14)svg+='<text x="'+r1(x+bw/2)+'" y="'+r1(T2+h2-hh-3)+'" fill="#fff" font-size="8" text-anchor="middle">'+y+'</text>';});
    }else if(type==='barres'){
      var n3=S.v.length,rh=26,Lb=104,Rb=40;H=n3*rh+14;svg='';
      S.v.forEach(function(y,i){var yy=8+i*rh,ww=Math.max(2,(W-Lb-Rb)*y/(S.pc?100:Math.max(mx,1))),cc=c.multi?col[i%col.length]:'url(#gB)';
        svg+='<text x="'+(Lb-6)+'" y="'+(yy+13)+'" fill="#d6d8f5" font-size="9" text-anchor="end">'+esc(S.lab[i].length>17?S.lab[i].slice(0,16)+'…':S.lab[i])+'</text>'+
          '<rect x="'+Lb+'" y="'+yy+'" width="'+(W-Lb-Rb)+'" height="16" fill="#1b1633" rx="2"/>'+
          '<rect class="growx" style="animation-delay:'+(i*60)+'ms" x="'+Lb+'" y="'+yy+'" width="'+r1(ww)+'" height="16" fill="'+cc+'" rx="2"/>'+
          '<text x="'+(W-Rb+5)+'" y="'+(yy+12)+'" fill="#fff" font-size="10" font-weight="700">'+y+(S.unit==='%'?'%':'')+'</text>';});
    }else if(type==='radar'){
      var cx=W/2,cy=H/2+2,R0=72,n4=S.v.length,rm=S.pc?100:Math.max(mx,1);
      for(var ring=1;ring<=4;ring++){var pp2=[];for(var a=0;a<n4;a++){var an=-Math.PI/2+2*Math.PI*a/n4;pp2.push(r1(cx+Math.cos(an)*R0*ring/4)+','+r1(cy+Math.sin(an)*R0*ring/4));}
        svg+='<polygon points="'+pp2.join(' ')+'" fill="none" stroke="#2b2650" stroke-width=".8"/>';}
      var pv=[];for(var a2=0;a2<n4;a2++){var an2=-Math.PI/2+2*Math.PI*a2/n4,rr=R0*S.v[a2]/rm;pv.push(r1(cx+Math.cos(an2)*rr)+','+r1(cy+Math.sin(an2)*rr));
        svg+='<line x1="'+cx+'" y1="'+cy+'" x2="'+r1(cx+Math.cos(an2)*R0)+'" y2="'+r1(cy+Math.sin(an2)*R0)+'" stroke="#2b2650" stroke-width=".8"/>'+
          '<text x="'+r1(cx+Math.cos(an2)*(R0+13))+'" y="'+r1(cy+Math.sin(an2)*(R0+13)+3)+'" fill="#d6d8f5" font-size="8" text-anchor="'+(Math.cos(an2)>.3?'start':(Math.cos(an2)<-.3?'end':'middle'))+'">'+esc(S.lab[a2].length>13?S.lab[a2].slice(0,12)+'…':S.lab[a2])+'</text>';}
      svg+='<polygon points="'+pv.join(' ')+'" fill="'+main+'" fill-opacity=".28" stroke="'+main+'" stroke-width="2" filter="url(#lueur)"/>';
      if(c.points)pv.forEach(function(p){var q=p.split(',');svg+='<circle cx="'+q[0]+'" cy="'+q[1]+'" r="3" fill="'+col[1]+'"/>';});
    }else{                                   /* anneau */
      var tot=S.v.reduce(function(a,b){return a+b;},0)||1,Cr=2*Math.PI*58,acc=0;
      svg+='<circle cx="110" cy="105" r="58" fill="none" stroke="#1b1633" stroke-width="26"/>';
      S.v.forEach(function(y,i){var len=Cr*y/tot,cc=S.split?(i===0?'#39ff88':'#ff3b5c'):col[i%col.length];
        svg+='<circle cx="110" cy="105" r="58" fill="none" stroke="'+cc+'" stroke-width="26" stroke-dasharray="'+r1(len)+' '+r1(Cr-len)+'" stroke-dashoffset="'+r1(-acc)+'" transform="rotate(-90 110 105)"/>';
        acc+=len;leg+='<span><i style="background:'+cc+'"></i>'+esc(S.lab[i])+' · '+Math.round(100*y/tot)+'%</span>';});
      svg+='<text x="110" y="102" fill="#fff" font-size="20" font-weight="900" text-anchor="middle">'+(S.split?Math.round(100*S.v[0]/tot)+'%':tot)+'</text><text x="110" y="116" fill="#8a8fb8" font-size="8" text-anchor="middle">'+(S.split?'RÉUSSITE':'TOTAL')+'</text>';
      svg='<g transform="translate(50 0)">'+svg+'</g>';
    }
    return '<svg id="gsvg" data-w="'+W+'" data-h="'+H+'" data-fx="'+r1(FX)+'" data-fy="'+r1(FY)+'" viewBox="0 0 '+W+' '+H+'">'+defs+svg+'</svg>'+(leg?'<div class="leg">'+leg+'</div>':'');
  }
  function opt(k,lst,c){return '<div class="opts">'+lst.map(function(o){return '<div class="o'+(String(c[k])===String(o[0])?' on':'')+'" onclick="R.set(\''+k+'\','+(typeof o[0]==='number'?o[0]:'\''+o[0]+'\'')+')">'+o[1]+'</div>';}).join('')+'</div>';}
  function tg(k,l,c){return '<div class="sw"><span>'+l+'</span><div class="tog'+(c[k]?' on':'')+'" onclick="R.set(\''+k+'\','+(c[k]?'false':'true')+')"></div></div>';}
  function graphBoite(){
    var d=D(),c=cfg(),S=serie(c,d);
    var titres={rp:'Progression des RP',notes:'Notes d\'examen',reussite:'Réussite par chapitre',volume:'Réponses par chapitre',split:'Réussites vs échecs'};
    return '<div class="chart"><div class="jl"><span style="letter-spacing:.14em;color:var(--cy)">'+titres[c.m].toUpperCase()+'</span></div><div id="zbox">'+chart(c,d)+'</div>'+
      '<div class="zc"><div class="bt" onclick="R.zb(-1)">−</div><input type="range" id="zr" min="1" max="10" step="0.1" value="'+Z.z+'" oninput="R.zs(this.value)"><div class="bt" onclick="R.zb(1)">+</div><div class="bt" onclick="R.zr()">⟲</div><div class="bt" onclick="R.fs()">⛶</div><b id="zlab">×'+Z.z.toFixed(1)+'</b></div>'+
      '<div class="mut" style="margin-top:6px">Zoom jusqu\'à ×10 : pince à deux doigts, glisse pour te déplacer, double-tap = ×3.</div></div>';
  }
  function graphOpts(){
    var c=cfg();
    return '<div class="sec"><h3>Personnaliser</h3>'+
      '<div class="optg">DONNÉES</div>'+opt('m',[['rp','Progression RP'],['reussite','Réussite / chapitre'],['volume','Volume / chapitre'],['notes','Notes d\'examen'],['split','Réussite vs échec']],c)+
      '<div class="optg">TYPE DE GRAPHIQUE</div>'+opt('type',[['ligne','Ligne'],['aire','Aire'],['barres','Barres'],['radar','Radar'],['anneau','Anneau']],c)+
      '<div class="optg">PALETTE</div>'+opt('pal',[['neon','Néon'],['feu','Feu'],['toxique','Toxique'],['glace','Glace'],['arc','Arc-en-ciel']],c)+
      '<div class="optg">PÉRIODE (courbes)</div>'+opt('plage',[[20,'20'],[50,'50'],[100,'100'],[0,'Tout']],c)+
      '<div class="optg">CHAPITRES : NOMBRE</div>'+opt('top',[[5,'Top 5'],[8,'Top 8'],[12,'Top 12'],[0,'Tous']],c)+
      '<div class="optg">CHAPITRES : TRI</div>'+opt('tri',[['desc','Décroissant'],['asc','Croissant'],['alpha','A → Z']],c)+
      '<div style="margin-top:8px">'+tg('grille','Grille',c)+tg('points','Points',c)+tg('valeurs','Valeurs',c)+tg('lisse','Courbe lissée',c)+tg('multi','Couleurs variées',c)+'</div>'+
      '<div class="big" style="margin-top:10px;padding:10px" onclick="R.resetCfg()">↺ RÉINITIALISER</div></div>';
  }
  function cl(v,a,b){return Math.max(a,Math.min(b,v));}
  function svgDim(){var s=$('gsvg');return s?{W:+s.getAttribute('data-w'),H:+s.getAttribute('data-h')}:null;}
  function applyZ(){
    var s=$('gsvg'),D0=svgDim();if(!s)return;var w=D0.W/Z.z,h=D0.H/Z.z;
    Z.x=cl(Z.x,0,D0.W-w);Z.y=cl(Z.y,0,D0.H-h);s.setAttribute('viewBox',r1(Z.x)+' '+r1(Z.y)+' '+r1(w)+' '+r1(h));
    /* trait et points gardent une taille lisible quand on zoome (la courbe reste visible, les points ne deviennent pas énormes) */
    var tr=s.querySelectorAll('path.draw'),k=0;for(k=0;k<tr.length;k++)tr[k].setAttribute('stroke-width',(2.2/Math.pow(Z.z,.8)).toFixed(2));
    var ci=s.querySelectorAll('circle');
    for(k=0;k<ci.length;k++){var c=ci[k];if(c.__r0===undefined)c.__r0=+c.getAttribute('r');
      if(c.__r0<10){c.setAttribute('r',(c.__r0/Math.pow(Z.z,.7)).toFixed(2));if(c.getAttribute('stroke-width'))c.setAttribute('stroke-width',(1.5/Math.pow(Z.z,.7)).toFixed(2));}}
    var l=$('zlab');if(l)l.textContent='×'+Z.z.toFixed(1);var r=$('zr');if(r)r.value=Z.z;
  }
  function zoomDepuis(nz,px,py,bz,bx,by){      /* garde sous le doigt le point (px,py) de la zone */
    var D0=svgDim();if(!D0)return;nz=cl(nz,1,10);
    var ux=bx+px*(D0.W/bz),uy=by+py*(D0.H/bz);Z.z=nz;Z.x=ux-px*(D0.W/nz);Z.y=uy-py*(D0.H/nz);applyZ();
  }
  function foyer(){var s=$('gsvg');if(!s||Z.z>1.001)return [.5,.5];return [+s.getAttribute('data-fx')/+s.getAttribute('data-w'),+s.getAttribute('data-fy')/+s.getAttribute('data-h')];}
  function zoomLier(){
    var b=$('zbox');if(!b||!$('gsvg'))return;applyZ();
    var mode=null,last=null,d0=0,z0=1,m0=null,x0=0,y0=0,bouge=false,tapT=0;
    function rect(){return b.getBoundingClientRect();}
    function dist(t){var dx=t[0].clientX-t[1].clientX,dy=t[0].clientY-t[1].clientY;return Math.sqrt(dx*dx+dy*dy)||1;}
    function mid(t){var r=rect();return [((t[0].clientX+t[1].clientX)/2-r.left)/r.width,((t[0].clientY+t[1].clientY)/2-r.top)/r.height];}
    b.addEventListener('touchstart',function(e){
      bouge=false;
      if(e.touches.length===2){e.preventDefault();mode='pinch';d0=dist(e.touches);z0=Z.z;m0=mid(e.touches);x0=Z.x;y0=Z.y;}
      else if(e.touches.length===1&&Z.z>1.001){e.preventDefault();mode='pan';last=[e.touches[0].clientX,e.touches[0].clientY];}
      else mode=null;
    },{passive:false});
    b.addEventListener('touchmove',function(e){
      if(mode==='pinch'&&e.touches.length===2){e.preventDefault();bouge=true;zoomDepuis(z0*dist(e.touches)/d0,m0[0],m0[1],z0,x0,y0);}
      else if(mode==='pan'&&e.touches.length===1){e.preventDefault();bouge=true;var D0=svgDim(),r=rect(),t=e.touches[0];
        Z.x-=(t.clientX-last[0])*(D0.W/Z.z)/r.width;Z.y-=(t.clientY-last[1])*(D0.H/Z.z)/r.height;last=[t.clientX,t.clientY];applyZ();}
    },{passive:false});
    b.addEventListener('touchend',function(e){
      if(e.touches.length===0&&!bouge&&mode!=='pinch'){                     /* double-tap : ×3 sur le point touché, ou retour à ×1 */
        var now=Date.now();
        if(now-tapT<300){tapT=0;if(Z.z>1.001){Z.z=1;Z.x=0;Z.y=0;applyZ();}else{var r=rect(),t=e.changedTouches[0];zoomDepuis(3,(t.clientX-r.left)/r.width,(t.clientY-r.top)/r.height,1,0,0);}}
        else tapT=now;
      }
      if(e.touches.length===0)mode=null;
    },{passive:true});
    b.addEventListener('wheel',function(e){e.preventDefault();var r=rect();zoomDepuis(Z.z*(e.deltaY<0?1.25:.8),(e.clientX-r.left)/r.width,(e.clientY-r.top)/r.height,Z.z,Z.x,Z.y);},{passive:false});
  }
  function vGraph(){return '<div id="gBoite">'+graphBoite()+'</div><div id="gOpts">'+graphOpts()+'</div>';}

  function rendre(force){
    var d=D(),sc=$('ecorps'),top=force?0:sc.scrollTop;
    if(vue==='graph'&&!force&&$('gBoite'))return;          /* ne pas casser le graphique pendant qu'on le règle */
    var f={home:vHome,grade:vGrade,rangs:vRangs,chap:vChap,graph:vGraph,clas:vClas}[vue]||vHome;
    $('eTitre').textContent=TITRES[vue]||'ÉVOLUTION';$('eBack').textContent=vue==='home'?'🏆':'‹';
    var r=cur();$('evo').style.setProperty('--pc',r.col);
    sc.innerHTML=f(d);sc.scrollTop=top;
    if(vue==='graph')zoomLier();
    if(vue==='rangs'&&force){var e=$('rr'+d.idx);if(e&&e.scrollIntoView)setTimeout(function(){e.scrollIntoView({block:'center'});},60);}
  }
  function go(v){vue=v;rendre(true);if(v==='clas'||v==='home')LK.ev({a:'evo',k:'open',v:v});}
  return {
    promo:promo,fin:fin,stop:stop,err:err,
    evoOuvrir:function(){vue='home';rendre(true);LK.ev({a:'evo',k:'open',v:'home'});},
    evoRendre:function(){rendre(false);},
    go:go,retour:function(){if(vue==='home')LK.fermer();else{vue='home';rendre(true);}},
    tri:function(t){tri=t;rendre(true);},
    set:function(k,v){var c=cfg();c[k]=v;LK.etat().rangs.cfg=c;LK.ev({a:'evo_cfg',cfg:c});Z={z:1,x:0,y:0};$('gBoite').innerHTML=graphBoite();$('gOpts').innerHTML=graphOpts();zoomLier();},
    resetCfg:function(){var c={};for(var k in DEF)c[k]=DEF[k];LK.etat().rangs.cfg=c;LK.ev({a:'evo_cfg',cfg:c});Z={z:1,x:0,y:0};$('gBoite').innerHTML=graphBoite();$('gOpts').innerHTML=graphOpts();zoomLier();},
    revoir:function(i){LK.ev({a:'evo',k:'revoir',i:i});},
    verrou:function(el){el.classList.remove('sk');void el.offsetWidth;el.classList.add('sk');},
    zb:function(s){var f=s>0?1.4:1/1.4,q=foyer();zoomDepuis(Z.z*f,q[0],q[1],Z.z,Z.x,Z.y);},
    zs:function(v){var q=foyer();zoomDepuis(parseFloat(v),q[0],q[1],Z.z,Z.x,Z.y);},
    zr:function(){Z={z:1,x:0,y:0};applyZ();},
    fs:function(){var c=document.querySelector('#gBoite .chart');if(c){c.classList.toggle('fs');setTimeout(applyZ,60);}}
  };
})();
"""
