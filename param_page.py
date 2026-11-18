# -*- coding: utf-8 -*-
"""
param_page.py — page « Paramètres » (style dark web, par catégories) et jauges « palettes » animées.
Fragments CSS / HTML / JS ajoutés à la page de Locky (locky_page.page_complete) : mode 'param'.

Les textes juridiques (confidentialité, conditions, licence) sont des TEXTES MODÈLES rédigés d'après le
fonctionnement réel de l'appli ; à faire relire par un juriste avant la publication officielle.
"""

CSS = r"""
#param{display:none;position:absolute;inset:0}
body.m-param #param{display:block}

/* ---- jauges « palettes » : petits blocs qui se remplissent en cascade ---- */
.pal{display:flex;gap:3px;margin:6px 0}
.pal i{flex:1;height:16px;background:#1b1633;border:1px solid #3a2f63;transform:skewX(-18deg)}
.pal.s i{height:9px}
.pal.g i{height:22px}
.pal.ok i.on{background:linear-gradient(180deg,#8dffbf,#1fbf6b);border-color:#39ff88;box-shadow:0 0 6px rgba(57,255,136,.8)}
.pal.ko i.on{background:linear-gradient(180deg,#ff8aa0,#c4203f);border-color:#ff3b5c;box-shadow:0 0 6px rgba(255,59,92,.8)}
.pal.or i.on{background:linear-gradient(180deg,#ffe08a,#ff9d00);border-color:#ffb000;box-shadow:0 0 6px rgba(255,176,0,.8)}
.pal.cy i.on{background:linear-gradient(180deg,#9ffaff,#00b8d4);border-color:#00f0ff;box-shadow:0 0 6px rgba(0,240,255,.8)}
.pal.mg i.on{background:linear-gradient(180deg,#ff9ae8,#c1169f);border-color:#ff2bd6;box-shadow:0 0 6px rgba(255,43,214,.8)}
.pal i.on{animation:pop .32s cubic-bezier(.2,1.4,.4,1) both;animation-delay:calc(var(--d)*26ms)}
.pal i.cur{animation:pop .32s cubic-bezier(.2,1.4,.4,1) both,puls 1.1s ease-in-out .7s infinite;animation-delay:calc(var(--d)*26ms),calc(var(--d)*26ms + .7s)}
@keyframes pop{from{transform:skewX(-18deg) scaleY(.15);opacity:0}to{transform:skewX(-18deg) scaleY(1);opacity:1}}
@keyframes puls{50%{opacity:.55}}
.jl{display:flex;justify-content:space-between;align-items:baseline;font-size:12px;margin-top:6px}
.jl b{font-size:22px}
.jl.ok b{color:var(--ok)}.jl.ko b{color:var(--ro)}.jl.or b{color:var(--or)}.jl.cy b{color:var(--cy)}.jl.mg b{color:var(--mg)}
.mini{display:flex;align-items:center;gap:8px;margin:6px 0;font-size:11px}
.mini .n{flex:0 0 42%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.mini .pal{flex:1;margin:0}
.mini .p{flex:0 0 36px;text-align:right;font-weight:800}

/* ---- paramètres ---- */
.cat{font-size:10px;letter-spacing:.24em;color:var(--mg);margin:14px 2px 6px;text-transform:uppercase}
.cat::before{content:"// ";color:var(--cy)}
.cat:first-child{margin-top:2px}
.pc{display:flex;align-items:center;gap:12px;padding:12px;margin-bottom:8px;border:1px solid rgba(0,240,255,.35);border-left:3px solid var(--cy);
 background:#0f0d20;border-radius:4px;touch-action:manipulation}
.pc:active{background:#1a1740;transform:scale(.985)}
.pc .ic{flex:none;width:38px;height:38px;display:grid;place-items:center;font-size:20px;border-radius:6px;background:rgba(255,255,255,.05)}
.pc .tx{flex:1;min-width:0;display:flex;flex-direction:column}
.pc .tx b{font-size:14px;color:#fff}
.pc .tx small{font-size:11px;color:var(--mut);margin-top:2px;line-height:1.3}
.pc .ch{flex:none;color:var(--cy);font-size:22px}
.pc.or{border-color:rgba(255,176,0,.45);border-left-color:var(--or)}.pc.or .ch{color:var(--or)}
.pc.mg{border-color:rgba(255,43,214,.4);border-left-color:var(--mg)}.pc.mg .ch{color:var(--mg)}
.pc.ok{border-color:rgba(57,255,136,.45);border-left-color:var(--ok)}.pc.ok .ch{color:var(--ok)}
.pc.ko{border-color:rgba(255,59,92,.5);border-left-color:var(--ro)}.pc.ko .ch{color:var(--ro)}
.pc.vi{border-color:rgba(157,107,255,.45);border-left-color:var(--vi)}.pc.vi .ch{color:var(--vi)}
.stat{padding:10px;border:1px dashed rgba(57,255,136,.5);border-radius:4px;background:rgba(57,255,136,.05);font-size:12px;line-height:1.5;margin-bottom:6px}
.stat.off{border-color:rgba(255,176,0,.6);background:rgba(255,176,0,.06)}
.stat b{color:#fff}
.opt{padding:10px 0;border-bottom:1px dashed rgba(255,255,255,.1)}
.opt:last-child{border:0}
.opt .l{display:flex;justify-content:space-between;align-items:center;font-size:13px}
input[type=range]{-webkit-appearance:none;appearance:none;width:100%;height:30px;background:transparent;margin:2px 0;touch-action:pan-x}
input[type=range]::-webkit-slider-runnable-track{height:6px;border-radius:3px;background:#2a2347;border:1px solid #4a3f7a}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:26px;height:26px;margin-top:-11px;border-radius:50%;background:var(--cy);border:2px solid #fff;box-shadow:0 0 10px var(--cy)}
details{border:1px solid rgba(255,43,214,.35);border-radius:4px;margin-bottom:8px;background:#0f0d20}
summary{padding:12px;font-size:13px;font-weight:800;color:var(--or);letter-spacing:.06em;list-style:none;touch-action:manipulation}
summary::-webkit-details-marker{display:none}
summary::before{content:"▸ ";color:var(--cy)}
details[open] summary::before{content:"▾ "}
details .tx{padding:0 12px 12px;font-size:12px;line-height:1.55;color:#d6d8f5}
details .tx p{margin:0 0 8px}
details .tx b{color:#fff}
.warn{padding:10px;border:1px solid var(--or);border-radius:4px;background:rgba(255,176,0,.08);color:#ffd98a;font-size:12px;line-height:1.5;margin-bottom:10px}
.ver{text-align:center;color:var(--mut);font-size:11px;margin:10px 0 4px}
"""

HTML = r"""
<div id="param" class="cadre"><div class="int">
  <div class="tete"><div class="bt" id="pBack" onclick="P.retour()">‹</div><div class="t" id="pTitre">PARAMÈTRES</div><div class="bt x" onclick="LK.fermer()">✕</div></div>
  <div class="corps" id="pcorps"></div>
</div></div>
"""

JS = r"""
/* ---------- jauge « palettes » : n blocs, les `pct`% premiers allumés, animation en cascade ---------- */
function pal(pct,cls,n,taille){
  n=n||20;var on=Math.round(Math.max(0,Math.min(100,pct))/100*n),h='<div class="pal '+cls+(taille?' '+taille:'')+'">';
  for(var i=0;i<n;i++){h+='<i'+(i<on?' class="'+(i===on-1?'on cur':'on')+'"':'')+' style="--d:'+i+'"></i>';}
  return h+'</div>';
}
function palN(val,max,cls,taille){      /* val blocs allumés sur max (ex. 6/7 jours) */
  var h='<div class="pal '+cls+(taille?' '+taille:'')+'">';
  for(var i=0;i<max;i++){h+='<i'+(i<val?' class="'+(i===val-1?'on cur':'on')+'"':'')+' style="--d:'+(i*3)+'"></i>';}
  return h+'</div>';
}

var P=(function(){
  var vue='home',glisse=false;
  var TITRES={home:'PARAMÈTRES',compte:'MON COMPTE',audio:'RÉGLAGES AUDIO',dev:'DÉVELOPPEUR',reseau:'RÉSEAU',apropos:'À PROPOS & VERSION'};
  function $(i){return document.getElementById(i);}
  function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function carte(ic,t,s,clic,cls){return '<div class="pc '+(cls||'')+'" onclick="'+clic+'"><span class="ic">'+ic+'</span><span class="tx"><b>'+t+'</b>'+(s?'<small>'+s+'</small>':'')+'</span><span class="ch">›</span></div>';}
  function cat(t){return '<div class="cat">'+t+'</div>';}
  function tog(k,lbl,on){return '<div class="opt"><div class="l"><span>'+lbl+'</span><div class="tog'+(on?' on':'')+'" onclick="P.audio(\''+k+'\','+(on?'false':'true')+')"></div></div></div>';}
  function glissiere(k,lbl,v,cls){
    return '<div class="opt"><div class="l"><span>'+lbl+'</span><b id="lv_'+k+'" style="color:var(--cy)">'+v+'%</b></div>'+
      '<input type="range" min="0" max="100" step="5" value="'+v+'" oninput="P.curseur(\''+k+'\',this.value,\''+cls+'\')" onpointerdown="P.g(1)" onpointerup="P.g(0)" onpointercancel="P.g(0)">'+
      '<div id="pl_'+k+'">'+pal(v,cls,20,'s')+'</div></div>';
  }

  function vHome(S){
    var c=S.compte||{};
    return cat('Compte & données')+
      carte('👤','Mon compte',c.connecte?('Connecté : '+esc(c.nom)):'Non connecté — connexion, données, infos personnelles',"P.go('compte')",'or')+
      cat('Son')+carte('🔊','Réglages audio','Musique, volumes, sons d\'interaction, mode silencieux',"P.go('audio')",'mg')+
      cat('Réseau')+carte('📡','Serveur & Internet','Internet ou Wi-Fi de la classe',"P.go('reseau')",'')+
      cat('Communauté')+carte('🤝','Rester connecté au Développeur','Liens directs : WhatsApp, YouTube, GitHub, Facebook, site…',"P.go('dev')",'ok')+
      cat('Aide & informations')+
      carte('❓','Comment fonctionne l\'appli','Guide d\'utilisation',"LK.act('aide')",'vi')+
      carte('🦊','Profil de Locky & calculatrice','Niveau, analyse, records',"LK.act('locky')",'vi')+
      carte('ℹ️','À propos & Version','Confidentialité, conditions, développeur, licence',"P.go('apropos')",'')+
      '<div class="ver">'+esc(S.version||'')+'</div>';
  }
  function vCompte(S){
    var c=S.compte||{};
    var st=c.connecte?('<div class="stat">● Connecté<br><b>'+esc(c.nom)+'</b> · '+esc(c.email||'e-mail non renseigné')+'<br>Île : '+esc(c.ile||'—')+' · ID : '+esc(c.ident||'—')+'</div>')
      :('<div class="stat off">○ '+(c.hors_ligne?'Mode hors-ligne (aucun compte relié)':'Aucun compte relié')+'<br>Les fonctions en ligne (classement, salles, sauvegarde) sont désactivées.</div>');
    return st+cat('Connexion')+
      carte(c.connecte?'🔓':'🔐',c.connecte?'Se déconnecter':'Se connecter / créer un compte',c.connecte?'Ce téléphone sera vidé de ta progression (elle reste sur ton compte)':'Retrouver ou créer ton compte sécurisé',"LK.act('compte')",c.connecte?'ko':'ok')+
      cat('Mes données')+
      carte('📄','Consulter mes données','Récapitulatif de tes informations enregistrées',"LK.act('donnees')",'')+
      carte('🆔','Copier mon identifiant','Pour te reconnecter ou être retrouvé par tes amis',"LK.act('copier_id')",'')+
      cat('Informations personnelles')+
      carte('✏️','Modifier mes informations','Nom, classe, âge, sexe, île, e-mail, mot de passe',"LK.act('infos')",'or')+
      cat('Zone dangereuse')+
      carte('🗑️','Supprimer mes données en ligne','Efface ton profil du serveur (classement, stats en ligne)',"LK.act('suppr_ligne')",'ko')+
      carte('🧹','Effacer ma progression sur ce téléphone','Points, statistiques et historique remis à zéro',"LK.act('suppr_local')",'ko');
  }
  function vAudio(S){
    var a=S.audio||{musique:true,vol:50,sons:true,vol_fx:100,muet:false};
    return '<div class="sec"><h3>Musique</h3>'+tog('musique','🎵 Musique de fond',a.musique)+glissiere('vol','🔉 Volume de la musique',a.vol,'cy')+
      '<div class="opt"><div class="big" style="margin:0;padding:10px" onclick="P.audio(\'suivante\',1)">⏭ PISTE SUIVANTE</div></div></div>'+
      '<div class="sec"><h3>Effets</h3>'+tog('sons','🔔 Sons d\'interaction (boutons, réponses)',a.sons)+glissiere('vol_fx','🔊 Volume des effets',a.vol_fx,'mg')+'</div>'+
      '<div class="sec"><h3>Général</h3>'+tog('muet','🔇 Mode silencieux (coupe tout)',a.muet)+
      '<div class="mut" style="margin-top:6px">En quittant le mode silencieux, tes réglages précédents sont restaurés.</div></div>';
  }
  function vReseau(S){
    return cat('Connexion')+carte('📶','Activer Internet','Ouvre les réglages Wi-Fi / données du téléphone',"LK.act('internet')",'')+
      carte('🏫','Serveur (Internet ou Wi-Fi de la classe)','Choisir le serveur utilisé par l\'appli',"LK.act('serveur')",'or');
  }
  function vDev(S){
    return '<div class="stat">Suis le développeur et rejoins la communauté : mises à jour, astuces, entraide.</div>'+
      cat('Communauté')+carte('💬','Rejoindre la communauté WhatsApp','Groupe officiel — accès direct',"LK.lien('communaute')",'ok')+
      cat('Réseaux & sites')+
      carte('🌐','Site officiel Omnimath','fazad-colab.github.io/Omnimath.dev',"LK.lien('site')",'')+
      carte('▶️','YouTube — @Omnimath.14','Vidéos et tutoriels',"LK.lien('youtube')",'ko')+
      carte('📘','Facebook — Omnimath','Page officielle',"LK.lien('facebook')",'vi')+
      carte('💻','GitHub — MonQuizKivy','Code source du projet',"LK.lien('github')",'mg')+
      carte('🔎','Rechercher « Omnimath » sur Google','Retrouver toutes les infos',"LK.lien('google')",'or');
  }
  function vApropos(S){
    return '<div class="warn">⚠️ <b>Application non 100 % hors ligne.</b> Le quiz, l\'entraînement, l\'examen, les défis, les cours et la calculatrice fonctionnent sans Internet. '+
      'Mais le compte (création, connexion, vérification e-mail, changement de mot de passe ou d\'e-mail), la sauvegarde/synchronisation, le classement, les salles en ligne, l\'assistant IA, les requêtes libres et l\'envoi d\'avis exigent une connexion.</div>'+
      '<div class="sec"><h3>Version</h3><div style="font-size:14px;color:#fff;font-weight:800">Math Quiz Comores</div><div class="mut">'+esc(S.version||'')+'<br>Édité par Omnimath — Comores</div></div>'+
      '<details><summary>POLITIQUE DE CONFIDENTIALITÉ</summary><div class="tx">'+
        '<p><b>1. Données concernées.</b> Nom, île de résidence, adresse e-mail, mot de passe, identifiant du joueur ; classe, niveau, âge et sexe (si tu les renseignes) ; progression (points de rang, XP, statistiques par chapitre, scores) ; numéro WhatsApp (facultatif) ; contenus que tu envoies volontairement (avis, requêtes à l\'assistant IA).</p>'+
        '<p><b>2. Finalités.</b> Gérer ton compte, sauvegarder et synchroniser ta progression, afficher le classement, faire fonctionner les salles en ligne et l\'assistant IA, améliorer l\'application.</p>'+
        '<p><b>3. Sécurité.</b> Le mot de passe n\'est jamais stocké en clair : seule une empreinte chiffrée est conservée. L\'appli garde uniquement un jeton de session ; les échanges avec le serveur sont authentifiés par ce jeton.</p>'+
        '<p><b>4. Partage.</b> Tes données ne sont ni vendues ni utilisées pour de la publicité. Ton nom, ton île et ta progression peuvent apparaître aux autres joueurs dans le classement et les salles en ligne.</p>'+
        '<p><b>5. Consentement.</b> La synchronisation en ligne se fait avec ton accord. Tu peux le retirer à tout moment en supprimant tes données en ligne.</p>'+
        '<p><b>6. Tes droits.</b> Paramètres › Mon compte : consulter tes données, les modifier (nom, classe, île, e-mail, mot de passe), supprimer tes données en ligne, effacer la progression de ce téléphone.</p>'+
        '<p><b>7. Conservation.</b> Tes données sont conservées tant que ton compte existe ; elles sont supprimées du serveur sur ta demande.</p>'+
        '<p><b>8. Élèves mineurs.</b> L\'usage par un mineur se fait avec l\'accord d\'un parent, tuteur ou enseignant.</p>'+
        '<p><b>9. Contact.</b> Via les liens de « Rester connecté au Développeur ».</p></div></details>'+
      '<details><summary>CONDITIONS D\'UTILISATION</summary><div class="tx">'+
        '<p><b>1. Objet.</b> Math Quiz Comores est une application éducative gratuite d\'entraînement aux mathématiques et aux sciences.</p>'+
        '<p><b>2. Compte.</b> Tu es responsable de la confidentialité de ton mot de passe et de l\'exactitude de tes informations. Un compte est strictement personnel.</p>'+
        '<p><b>3. Usages interdits.</b> Usurpation d\'identité, triche organisée, spam, tentative de piratage ou de surcharge du serveur, insultes ou contenus illicites dans les contenus envoyés, extraction automatisée des questions.</p>'+
        '<p><b>4. Version bêta.</b> L\'appli est fournie « en l\'état », en phase de test. Des erreurs ou interruptions peuvent survenir ; les résultats ne remplacent pas l\'enseignement officiel.</p>'+
        '<p><b>5. Assistant IA.</b> Ses réponses peuvent contenir des erreurs : vérifie-les avec ton cours ou ton enseignant.</p>'+
        '<p><b>6. Suspension.</b> Un compte qui enfreint ces règles peut être suspendu ou supprimé.</p>'+
        '<p><b>7. Évolution.</b> Ces conditions peuvent évoluer avec l\'application ; l\'usage continu vaut acceptation.</p></div></details>'+
      '<details><summary>LE DÉVELOPPEUR & SES OBJECTIFS</summary><div class="tx">'+
        '<p><b>Fazad Nassur</b> — fondateur et développeur principal d\'Omnimath, éditeur de logiciels et d\'applications éducatives fondé aux Comores.</p>'+
        '<p><b>Mission :</b> démocratiser l\'excellence scientifique par le numérique et offrir à chaque élève des outils modernes, intuitifs et adaptés aux réalités locales pour surmonter les difficultés en mathématiques.</p>'+
        '<p><b>Objectifs :</b></p><p>• Accessibilité : une utilisation fluide, même avec un accès restreint à Internet.<br>• Souveraineté pédagogique : des contenus alignés sur les programmes d\'études.<br>• Innovation continue : des mises à jour régulières fondées sur les retours des utilisateurs.<br>• Gratuité et aucune publicité.</p></div></details>'+
      '<details><summary>LICENCE — TOUS DROITS RÉSERVÉS</summary><div class="tx">'+
        '<p><b>© 2026 Fazad Nassur / Omnimath. Tous droits réservés.</b></p>'+
        '<p>L\'application, son code, ses questions, ses contenus pédagogiques, son design, ses logos, son nom et sa mascotte sont protégés. Aucune partie ne peut être copiée, modifiée, redistribuée, publiée, vendue ou utilisée à des fins commerciales sans autorisation écrite du titulaire.</p>'+
        '<p>Il t\'est accordé un droit d\'utilisation personnel, non exclusif, non transférable et révocable, à des fins éducatives. Toute rétro-ingénierie ou extraction des contenus est interdite.</p>'+
        '<p>Les composants tiers (Kivy, KaTeX, Flask…) restent soumis à leurs propres licences libres.</p></div></details>'+
      '<div class="ver">'+esc(S.version||'')+'</div>';
  }

  function rendre(force){
    if(glisse&&!force)return;
    var S=LK.etat(),sc=$('pcorps'),top=force?0:sc.scrollTop;
    var f={home:vHome,compte:vCompte,audio:vAudio,dev:vDev,reseau:vReseau,apropos:vApropos}[vue]||vHome;
    $('pTitre').textContent=TITRES[vue]||'PARAMÈTRES';
    $('pBack').textContent=vue==='home'?'⚙':'‹';
    sc.innerHTML=f(S);sc.scrollTop=top;
  }
  return {
    rendre:rendre,
    go:function(v){vue=v;rendre(true);},
    retour:function(){if(vue==='home')LK.fermer();else{vue='home';rendre(true);}},
    reset:function(){vue='home';},
    g:function(b){glisse=!!b;if(!b)setTimeout(function(){rendre();},50);},
    audio:function(k,v){var S=LK.etat();if(!S.audio)S.audio={};if(k!=='suivante')S.audio[k]=v;LK.ev({a:'audio',k:k,v:v});if(k!=='suivante')rendre(true);},
    curseur:function(k,v,cls){v=parseInt(v,10);var S=LK.etat();if(!S.audio)S.audio={};S.audio[k]=v;
      $('lv_'+k).textContent=v+'%';var bl=$('pl_'+k).querySelectorAll('i'),on=Math.round(v/100*bl.length);
      for(var i=0;i<bl.length;i++){bl[i].className=i<on?'on':'';bl[i].style.animation='none';}LK.ev({a:'audio',k:k,v:v});}
  };
})();
"""
