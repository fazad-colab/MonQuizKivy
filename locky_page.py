# -*- coding: utf-8 -*-
"""
locky_page.py — interface HTML de Locky (avatar + menu « dark web » + calculatrice scientifique).

Cette page est affichée dans une WebView Android TRANSPARENTE posée AU-DESSUS de tout (y compris de la
WebView des questions) : c'est ce qui permet à Locky de rester devant la page.
Python parle à la page via LK.maj(...) / LK.mode(...) / LK.dire(...) ; la page répond en empilant des
événements dans window.__lk_q (lus par Python).
"""

CSS = r"""
:root{--cy:#00f0ff;--mg:#ff2bd6;--ok:#39ff88;--or:#ffb000;--vi:#9d6bff;--ro:#ff3b5c;--bl:#3d8bff;--ye:#ffe94a;--bg:#07060f;--tx:#e9eaff;--mut:#8a8fb8}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent;-webkit-user-select:none;user-select:none}
html,body{margin:0;height:100%;background:transparent;overflow:hidden;color:var(--tx);font-family:ui-monospace,Menlo,Consolas,"Roboto Mono",monospace}
#av,#menu,#calc{display:none;position:absolute;inset:0}
body.m-avatar #av{display:flex}body.m-menu #menu{display:block}body.m-calc #calc{display:block}

/* ---------- avatar ---------- */
#av{align-items:center;gap:6px;padding:2px;touch-action:none}
#img{height:100%;max-width:55%;object-fit:contain;filter:drop-shadow(0 0 8px rgba(0,240,255,.85));touch-action:none}
#bulle{flex:1;min-width:0;max-height:100%;overflow:hidden;font-size:11px;line-height:1.25;color:var(--ok);font-weight:700;text-align:center;
 padding:6px 8px;background:rgba(7,6,15,.92);border:1px solid rgba(0,240,255,.55);
 clip-path:polygon(8px 0,100% 0,100% calc(100% - 8px),calc(100% - 8px) 100%,0 100%,0 8px);box-shadow:0 0 10px rgba(0,240,255,.35)}
#bulle.vide{display:none}
@keyframes flash{from{background:rgba(255,43,214,.45)}to{background:rgba(7,6,15,.92)}}
#bulle.n{animation:flash .6s ease-out}

/* ---------- cadre façon Free Fire / dark web ---------- */
.cadre{padding:2px;background:linear-gradient(135deg,var(--or),var(--mg) 45%,var(--cy));
 clip-path:polygon(16px 0,100% 0,100% calc(100% - 16px),calc(100% - 16px) 100%,0 100%,0 16px)}
.int{position:absolute;inset:2px;background:linear-gradient(160deg,#16092a,#07060f 55%,#091226);
 clip-path:polygon(15px 0,100% 0,100% calc(100% - 15px),calc(100% - 15px) 100%,0 100%,0 15px);display:flex;flex-direction:column;
 }
.tete{flex:none;display:flex;align-items:center;gap:8px;padding:10px 12px;border-bottom:1px solid rgba(255,176,0,.45);
 background:linear-gradient(90deg,rgba(255,176,0,.22),transparent)}
.tete .t{flex:1;font-weight:800;letter-spacing:.16em;color:var(--or);font-size:14px;text-shadow:0 0 8px var(--or)}
.tete .t small{color:var(--cy);font-weight:400;letter-spacing:.1em}
.bt{flex:none;border:1px solid var(--cy);color:var(--cy);background:rgba(0,240,255,.08);border-radius:6px;padding:7px 11px;font:700 13px ui-monospace,monospace;
 touch-action:manipulation}
.bt:active{transform:scale(.94);background:rgba(0,240,255,.25)}
.bt.x{border-color:var(--ro);color:var(--ro);background:rgba(255,59,92,.1)}
.corps{flex:1;overflow-y:auto;-webkit-overflow-scrolling:touch;overscroll-behavior:contain;touch-action:pan-y;padding:10px 12px 16px}
.sec{margin:0 0 12px;padding:10px;border:1px solid rgba(255,43,214,.35);background:#120f24;border-radius:4px}
.sec h3{margin:0 0 8px;font-size:11px;letter-spacing:.22em;color:var(--mg);text-transform:uppercase}
.sec h3::before{content:"> ";color:var(--cy)}
.row{display:flex;gap:8px;align-items:center}
.id{display:flex;gap:10px;align-items:center}
.id img{width:64px;height:64px;object-fit:contain;filter:drop-shadow(0 0 8px var(--cy))}
.nom{font-size:18px;font-weight:800;color:#fff}
.niv{color:var(--or);font-weight:800;letter-spacing:.1em;font-size:13px}
.seg{display:flex;gap:4px;margin:8px 0 4px}
.seg i{flex:1;height:10px;background:#201a38;border:1px solid #3a2f63;transform:skewX(-20deg)}
.seg i.on{background:linear-gradient(90deg,var(--or),#ffd36a);border-color:var(--or);box-shadow:0 0 8px var(--or)}
.mut{color:var(--mut);font-size:11px;line-height:1.4}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.kpi{border:1px solid rgba(0,240,255,.35);background:rgba(0,240,255,.05);padding:8px;border-radius:4px}
.kpi b{display:block;font-size:20px;color:var(--cy)}
.kpi span{font-size:10px;letter-spacing:.12em;color:var(--mut);text-transform:uppercase}
.kpi.o b{color:var(--or)}.kpi.m b{color:var(--mg)}.kpi.v b{color:var(--ok)}
.barre{display:flex;height:20px;border-radius:3px;overflow:hidden;border:1px solid #3a2f63;margin:6px 0}
.barre .r{background:linear-gradient(90deg,#1fbf6b,var(--ok));color:#021;font-size:11px;font-weight:800;display:grid;place-items:center;min-width:0}
.barre .e{background:linear-gradient(90deg,var(--ro),#b3203c);color:#fff;font-size:11px;font-weight:800;display:grid;place-items:center;min-width:0}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{font-size:11px;padding:4px 8px;border-radius:3px;border:1px solid}
.chip.f{color:var(--ok);border-color:var(--ok);background:rgba(57,255,136,.08)}
.chip.w{color:var(--ro);border-color:var(--ro);background:rgba(255,59,92,.08)}
.sw{display:flex;align-items:center;justify-content:space-between;padding:8px 0;border-bottom:1px dashed rgba(255,255,255,.1);font-size:13px}
.sw:last-child{border:0}
.tog{width:46px;height:24px;border-radius:12px;background:#2a2347;border:1px solid #4a3f7a;position:relative;flex:none}
.tog::after{content:"";position:absolute;top:2px;left:2px;width:18px;height:18px;border-radius:50%;background:var(--mut);transition:.15s}
.tog.on{background:rgba(57,255,136,.25);border-color:var(--ok)}.tog.on::after{left:24px;background:var(--ok);box-shadow:0 0 8px var(--ok)}
.opts{display:flex;gap:6px;flex-wrap:wrap}
.o{padding:7px 10px;border:1px solid #4a3f7a;border-radius:4px;font-size:12px;color:var(--mut);touch-action:manipulation}
.o.on{border-color:var(--mg);color:#fff;background:rgba(255,43,214,.18);box-shadow:0 0 8px rgba(255,43,214,.5)}
.big{display:block;width:100%;padding:14px;margin-top:4px;text-align:center;font:800 14px ui-monospace,monospace;letter-spacing:.14em;border-radius:6px;
 color:#fff;border:1px solid var(--cy);background:linear-gradient(90deg,rgba(0,240,255,.25),rgba(255,43,214,.25));box-shadow:0 0 14px rgba(0,240,255,.35);touch-action:manipulation}
.big:active{transform:scale(.98)}
.big.off{border-color:#555;color:#888;background:#1a1a24;box-shadow:none}

/* ---------- calculatrice ---------- */
#calc .int{background:linear-gradient(160deg,#0d0a1d,#060610)}
#calc .tete{padding:5px 8px;gap:6px;touch-action:none}#calc .tete .t{font-size:12px}#calc .bt{padding:4px 9px;font-size:12px}
.aff{flex:none;padding:3px 10px;border-bottom:1px solid rgba(0,240,255,.3);background:rgba(0,0,0,.45)}
#expr{min-height:14px;max-height:20px;overflow-x:auto;white-space:nowrap;font-size:13px;color:var(--cy);text-align:right;scrollbar-width:none}
#res{font-size:24px;font-weight:800;color:#fff;text-align:right;overflow-x:auto;white-space:nowrap;min-height:28px;line-height:28px}
#res.err{color:var(--ro);font-size:18px}
.ind{display:flex;justify-content:space-between;font-size:10px;color:var(--mut);letter-spacing:.1em}
.tabs{flex:none;display:flex;gap:4px;padding:4px 6px 0}
.tab{flex:1;text-align:center;padding:4px 0;font-size:10px;letter-spacing:.08em;color:var(--mut);border:1px solid #3a2f63;border-bottom:0;border-radius:5px 5px 0 0;touch-action:manipulation}
.tab.on{color:#fff;background:rgba(255,43,214,.2);border-color:var(--mg)}
.pane{display:none;flex:1;min-height:0;overflow-y:auto;padding:4px 6px;-webkit-overflow-scrolling:touch}
.pane.on{display:block}
.keys{display:grid;grid-template-columns:repeat(6,1fr);gap:4px}
.keys.c5{grid-template-columns:repeat(5,1fr)}.keys.c4{grid-template-columns:repeat(4,1fr)}
.k{min-height:34px;display:grid;place-items:center;border-radius:5px;font:700 14px ui-monospace,monospace;border:1px solid;touch-action:manipulation;
 background:rgba(255,255,255,.04)}
.k:active{transform:scale(.92);filter:brightness(1.6)}
.k.num{color:var(--cy);border-color:rgba(0,240,255,.6)}
.k.op{color:var(--mg);border-color:rgba(255,43,214,.7)}
.k.eq{color:#06130b;background:linear-gradient(135deg,var(--ok),#14c46a);border-color:var(--ok);box-shadow:0 0 12px rgba(57,255,136,.6)}
.k.ctl{color:var(--ro);border-color:rgba(255,59,92,.7)}
.k.mem{color:var(--bl);border-color:rgba(61,139,255,.7)}
.k.trg{color:var(--ok);border-color:rgba(57,255,136,.6)}
.k.hyp{color:#2ee6c8;border-color:rgba(46,230,200,.6)}
.k.log{color:var(--or);border-color:rgba(255,176,0,.7)}
.k.pow{color:var(--ye);border-color:rgba(255,233,74,.6)}
.k.cmb{color:var(--vi);border-color:rgba(157,107,255,.7)}
.k.cst{color:#ff8ad8;border-color:rgba(255,138,216,.6)}
.k.phy{color:#9fe8ff;border-color:rgba(159,232,255,.5);font-size:12px}
.grp{font-size:10px;letter-spacing:.2em;color:var(--mut);margin:7px 0 3px;text-transform:uppercase}
.grp:first-child{margin-top:0}
select{width:100%;padding:10px;margin:4px 0;background:#120e26;color:#fff;border:1px solid var(--cy);border-radius:5px;font:14px ui-monospace,monospace}
.cv{font-size:22px;font-weight:800;color:var(--ok);text-align:center;padding:12px;border:1px dashed var(--ok);border-radius:6px;margin-top:8px;word-break:break-all}
.hi{padding:8px;border-bottom:1px solid rgba(255,255,255,.08);font-size:13px;touch-action:manipulation}
.hi small{display:block;color:var(--mut)}.hi b{color:var(--ok)}
"""

HTML = r"""
<div id="av"><img id="img" src="badges/locky.png" alt=""><div id="bulle" class="vide"></div></div>

<div id="menu" class="cadre"><div class="int">
  <div class="tete"><div class="t">LOCKY <small>// PROFIL</small></div><div class="bt x" onclick="LK.fermer()">✕</div></div>
  <div class="corps" id="mcorps"></div>
</div></div>

<div id="calc" class="cadre"><div class="int">
  <div class="tete"><div class="t">⠿ CALCUL <small>// PRO · déplaçable</small></div>
    <div class="bt" id="bMode" onclick="C.mode()">DEG</div>
    <div class="bt" onclick="LK.reduire()">▾</div><div class="bt x" onclick="LK.fermer()">✕</div></div>
  <div class="aff"><div class="ind"><span id="iM">&nbsp;</span><span id="iA">Ans = 0</span></div>
    <div id="expr"></div><div id="res">0</div></div>
  <div class="tabs"><div class="tab on" data-p="p1" onclick="C.tab('p1')">BASE</div><div class="tab" data-p="p2" onclick="C.tab('p2')">FONCTIONS</div>
    <div class="tab" data-p="p3" onclick="C.tab('p3')">CONVERTIR</div><div class="tab" data-p="p4" onclick="C.tab('p4')">HIST.</div></div>
  <div class="pane on" id="p1"></div><div class="pane" id="p2"></div><div class="pane" id="p3"></div><div class="pane" id="p4"></div>
</div></div>
"""

JS = r"""
/* =================== MOTEUR DE CALCUL (analyseur récursif, sans eval) =================== */
var Calc=(function(){
  var angle='DEG';
  function toRad(x){return angle==='DEG'?x*Math.PI/180:(angle==='GRAD'?x*Math.PI/200:x);}
  function fromRad(x){return angle==='DEG'?x*180/Math.PI:(angle==='GRAD'?x*200/Math.PI:x);}
  function fact(n){if(n<0||n!==Math.floor(n)||n>170)throw new Error('n! : entier 0..170');var r=1;for(var i=2;i<=n;i++)r*=i;return r;}
  function ent(x,nom){if(x!==Math.floor(x)||x<0)throw new Error(nom+' : entiers ≥ 0');return x;}
  function nCr(n,r){ent(n,'nCr');ent(r,'nCr');if(r>n)return 0;r=Math.min(r,n-r);var v=1;for(var i=1;i<=r;i++)v=v*(n-r+i)/i;return Math.round(v);}
  function nPr(n,r){ent(n,'nPr');ent(r,'nPr');if(r>n)return 0;var v=1;for(var i=0;i<r;i++)v*=(n-i);return v;}
  var F={
    sin:function(x){var r=toRad(x);var v=Math.sin(r);return Math.abs(v)<1e-15?0:v;},
    cos:function(x){var r=toRad(x);var v=Math.cos(r);return Math.abs(v)<1e-15?0:v;},
    tan:function(x){var c=Math.cos(toRad(x));if(Math.abs(c)<1e-15)throw new Error('tan indéfinie');return Math.sin(toRad(x))/c;},
    asin:function(x){if(Math.abs(x)>1)throw new Error('asin : |x|≤1');return fromRad(Math.asin(x));},
    acos:function(x){if(Math.abs(x)>1)throw new Error('acos : |x|≤1');return fromRad(Math.acos(x));},
    atan:function(x){return fromRad(Math.atan(x));},
    sinh:Math.sinh,cosh:Math.cosh,tanh:Math.tanh,asinh:Math.asinh,
    acosh:function(x){if(x<1)throw new Error('acosh : x≥1');return Math.acosh(x);},
    atanh:function(x){if(Math.abs(x)>=1)throw new Error('atanh : |x|<1');return Math.atanh(x);},
    ln:function(x){if(x<=0)throw new Error('ln : x>0');return Math.log(x);},
    log:function(x){if(x<=0)throw new Error('log : x>0');return Math.log10(x);},
    log2:function(x){if(x<=0)throw new Error('log₂ : x>0');return Math.log2(x);},
    exp:Math.exp,
    sqrt:function(x){if(x<0)throw new Error('√ : x≥0');return Math.sqrt(x);},
    cbrt:Math.cbrt,abs:Math.abs,floor:Math.floor,ceil:Math.ceil,round:Math.round,
    root:function(x,n){if(n===0)throw new Error('racine d\'ordre 0');if(x<0&&Math.abs(n%2)===1)return -Math.pow(-x,1/n);if(x<0)throw new Error('racine paire de négatif');return Math.pow(x,1/n);},
    mod:function(a,b){if(b===0)throw new Error('mod 0');return ((a%b)+b)%b;},
    C:nCr,P:nPr,fact:fact,
    atan2:function(y,x){return fromRad(Math.atan2(y,x));},
    min:Math.min,max:Math.max,pow:Math.pow
  };
  var CONST={pi:Math.PI,e:Math.E,phi:(1+Math.sqrt(5))/2,ans:0};
  function norm(s){
    return s.replace(/×/g,'*').replace(/÷/g,'/').replace(/[−–]/g,'-').replace(/π/g,'pi').replace(/φ/g,'phi')
      .replace(/√/g,'sqrt').replace(/∛/g,'cbrt').replace(/log₂/g,'log2').replace(/;/g,',').replace(/\s+/g,'');
  }
  function tokens(s){
    var t=[],i=0,m;
    while(i<s.length){
      var r=s.slice(i);
      if((m=/^(\d+\.?\d*|\.\d+)(E[+-]?\d+)?/.exec(r))){t.push({t:'n',v:parseFloat(m[0])});i+=m[0].length;}
      else if((m=/^[a-zA-Z][a-zA-Z0-9]*/.exec(r))){t.push({t:'i',v:m[0]});i+=m[0].length;}
      else if('+-*/^(),!%'.indexOf(r[0])>=0){t.push({t:r[0]});i++;}
      else throw new Error('Symbole inconnu : '+r[0]);
    }
    return t;
  }
  function evaluer(src){
    var T=tokens(norm(src)),p=0;
    function pk(){return T[p];}
    function eat(x){if(!T[p]||T[p].t!==x)throw new Error('Syntaxe : « '+x+' » attendu');return T[p++];}
    function expr(){var v=terme();while(pk()&&(pk().t==='+'||pk().t==='-')){var o=T[p++].t;var w=terme();v=o==='+'?v+w:v-w;}return v;}
    function debutFacteur(){var k=pk();return k&&(k.t==='n'||k.t==='i'||k.t==='(');}
    function terme(){
      var v=unaire();
      while(pk()){
        if(pk().t==='*'||pk().t==='/'){var o=T[p++].t;var w=unaire();if(o==='/'&&w===0)throw new Error('Division par zéro');v=o==='*'?v*w:v/w;}
        else if(debutFacteur()){v=v*unaire();}           /* multiplication implicite : 2π, 3(4+1), 2sin(x) */
        else break;
      }
      return v;
    }
    function unaire(){
      if(pk()&&pk().t==='-'){p++;return -unaire();}
      if(pk()&&pk().t==='+'){p++;return unaire();}
      return puissance();
    }
    function puissance(){
      var b=postfixe();
      if(pk()&&pk().t==='^'){p++;var e=unaire();return Math.pow(b,e);}   /* associatif à droite, 2^-3 OK */
      return b;
    }
    function postfixe(){
      var v=primaire();
      while(pk()&&(pk().t==='!'||pk().t==='%')){var o=T[p++].t;v=o==='!'?fact(v):v/100;}
      return v;
    }
    function primaire(){
      var k=pk();if(!k)throw new Error('Expression incomplète');
      if(k.t==='n'){p++;return k.v;}
      if(k.t==='('){p++;var v=expr();eat(')');return v;}
      if(k.t==='i'){
        p++;var nom=k.v;
        if(pk()&&pk().t==='('){
          p++;var a=[expr()];while(pk()&&pk().t===','){p++;a.push(expr());}eat(')');
          var f=F[nom];if(!f)throw new Error('Fonction inconnue : '+nom);
          return f.apply(null,a);
        }
        if(nom in CONST)return CONST[nom];
        throw new Error('Inconnu : '+nom);
      }
      throw new Error('Syntaxe');
    }
    var r=expr();
    if(p<T.length)throw new Error('Syntaxe : reste « '+T[p].t+' »');
    if(typeof r!=='number'||isNaN(r))throw new Error('Résultat indéfini');
    if(!isFinite(r))throw new Error('Dépassement de capacité');
    return r;
  }
  function fmt(x){
    if(x===0)return '0';
    var a=Math.abs(x);
    if(a>=1e12||a<1e-9){var s=x.toExponential(9).replace(/\.?0+e/,'e');return s.replace('e+','×10^').replace('e-','×10^-').replace('e','×10^');}
    var s=String(Number(x.toPrecision(12)));
    return s;
  }
  return {evaluer:evaluer,fmt:fmt,setAns:function(v){CONST.ans=v;},mode:function(m){if(m)angle=m;return angle;}};
})();

/* =================== INTERFACE CALCULATRICE =================== */
var C=(function(){
  var E=[],mem=0,hist=[],val=null,angles=['DEG','RAD','GRAD'];
  function K(l,ins,cl,act){return {l:l,i:ins,c:cl,a:act};}
  var BASE=[
    K('MC',0,'mem','mc'),K('MR',0,'mem','mr'),K('M+',0,'mem','mp'),K('M−',0,'mem','mm'),K('ANS','ans','mem'),K('C',0,'ctl','clr'),
    K('7','7','num'),K('8','8','num'),K('9','9','num'),K('÷','÷','op'),K('(','(','op'),K(')',')','op'),
    K('4','4','num'),K('5','5','num'),K('6','6','num'),K('×','×','op'),K('^','^','pow'),K('√','√(','pow'),
    K('1','1','num'),K('2','2','num'),K('3','3','num'),K('−','−','op'),K('x²','^2','pow'),K('%','%','op'),
    K('0','0','num'),K('.','.','num'),K('EXP','E','op'),K('+','+','op'),K('⌫',0,'ctl','del'),K('=',0,'eq','eval')
  ];
  var FN=[
    ['Trigonométrie',[K('sin','sin(','trg'),K('cos','cos(','trg'),K('tan','tan(','trg'),K('sin⁻¹','asin(','trg'),K('cos⁻¹','acos(','trg'),K('tan⁻¹','atan(','trg')]],
    ['Hyperboliques',[K('sinh','sinh(','hyp'),K('cosh','cosh(','hyp'),K('tanh','tanh(','hyp'),K('sinh⁻¹','asinh(','hyp'),K('cosh⁻¹','acosh(','hyp'),K('tanh⁻¹','atanh(','hyp')]],
    ['Logarithmes & exponentielles',[K('ln','ln(','log'),K('log','log(','log'),K('log₂','log₂(','log'),K('eˣ','exp(','log'),K('10ˣ','10^(','log'),K('|x|','abs(','log')]],
    ['Puissances & racines',[K('x³','^3','pow'),K('∛','∛(','pow'),K('ʸ√x','root(','pow'),K('x⁻¹','^(-1)','pow'),K('n!','!','pow'),K('mod','mod(','pow')]],
    ['Combinatoire & arrondis',[K('nCr','C(','cmb'),K('nPr','P(','cmb'),K('⌊x⌋','floor(','cmb'),K('⌈x⌉','ceil(','cmb'),K('arr.','round(','cmb'),K('atan2','atan2(','cmb')]],
    ['Constantes & séparateurs',[K('π','π','cst'),K('e','e','cst'),K('φ','φ','cst'),K(';',';','cst'),K('min','min(','cst'),K('max','max(','cst')]],
    ['Constantes physiques (SI)',[K('c','(299792458)','phy'),K('g','(9.80665)','phy'),K('h','(6.62607015E-34)','phy'),K('N_A','(6.02214076E23)','phy'),K('k_B','(1.380649E-23)','phy'),K('R','(8.314462618)','phy'),
      K('G','(6.6743E-11)','phy'),K('e⁻','(1.602176634E-19)','phy'),K('ε₀','(8.8541878128E-12)','phy'),K('μ₀','(1.25663706212E-6)','phy'),K('m_e','(9.1093837015E-31)','phy'),K('m_p','(1.67262192369E-27)','phy')]]
  ];
  var UN={
    'Longueur':{b:'m',u:{'mm':.001,'cm':.01,'m':1,'km':1000,'pouce':.0254,'pied':.3048,'mile':1609.344}},
    'Masse':{b:'kg',u:{'mg':1e-6,'g':.001,'kg':1,'tonne':1000,'livre':.45359237,'once':.028349523125}},
    'Durée':{b:'s',u:{'ms':.001,'s':1,'min':60,'h':3600,'jour':86400,'semaine':604800}},
    'Aire':{b:'m²',u:{'cm²':1e-4,'m²':1,'ha':1e4,'km²':1e6}},
    'Volume':{b:'L',u:{'mL':.001,'cL':.01,'L':1,'m³':1000}},
    'Vitesse':{b:'m/s',u:{'m/s':1,'km/h':1/3.6,'mph':.44704,'nœud':.514444}},
    'Angle':{b:'rad',u:{'degré':Math.PI/180,'radian':1,'grade':Math.PI/200,'tour':2*Math.PI}},
    'Énergie':{b:'J',u:{'J':1,'kJ':1000,'cal':4.184,'kcal':4184,'Wh':3600,'kWh':3.6e6}},
    'Pression':{b:'Pa',u:{'Pa':1,'hPa':100,'kPa':1000,'bar':1e5,'atm':101325}},
    'Température':{b:'K',u:{'°C':1,'K':1,'°F':1}}
  };
  function $(i){return document.getElementById(i);}
  function ex(){return E.join('');}
  function tok(k){
    if(k.a){act(k.a);return;}
    var s=k.i;
    if(s==='ans'){s='ans';}
    E.push(s);maj();
  }
  function act(a){
    if(a==='clr'){E=[];val=null;}
    else if(a==='del'){E.pop();}
    else if(a==='mc'){mem=0;}
    else if(a==='mr'){E.push('('+Calc.fmt(mem).replace('×10^','E')+')');}
    else if(a==='mp'||a==='mm'){if(val!==null){mem+=(a==='mp'?val:-val);}}
    else if(a==='eval'){egal();return;}
    maj();
  }
  function maj(){
    $('expr').textContent=ex()||'';$('expr').scrollLeft=1e6;
    $('iM').textContent=mem!==0?('M = '+Calc.fmt(mem)):'\u00a0';
    var r=$('res');
    if(!E.length){r.className='';r.textContent='0';val=null;return;}
    try{val=Calc.evaluer(ex());r.className='';r.textContent=Calc.fmt(val);}
    catch(e){val=null;r.className='';r.textContent='…';}      /* aperçu en direct : silencieux tant que l'expression est incomplète */
  }
  function egal(){
    if(!E.length)return;
    var r=$('res');
    try{
      var v=Calc.evaluer(ex());
      hist.unshift({e:ex(),r:Calc.fmt(v),v:v});if(hist.length>40)hist.pop();
      Calc.setAns(v);$('iA').textContent='Ans = '+Calc.fmt(v);
      E=[Calc.fmt(v).replace('×10^','E')];val=v;
      $('expr').textContent=hist[0].e+' =';r.className='';r.textContent=Calc.fmt(v);
      histRendre();convMaj();
    }catch(x){r.className='err';r.textContent=x.message||'Erreur';}
  }
  function touche(k){var d=document.createElement('div');d.className='k '+k.c;d.textContent=k.l;
    var f=function(ev){ev.preventDefault();tok(k);};d.addEventListener('click',f);return d;}
  function construire(){
    var g=document.createElement('div');g.className='keys';BASE.forEach(function(k){g.appendChild(touche(k));});$('p1').appendChild(g);
    FN.forEach(function(grp){
      var t=document.createElement('div');t.className='grp';t.textContent=grp[0];$('p2').appendChild(t);
      var gg=document.createElement('div');gg.className='keys';grp[1].forEach(function(k){gg.appendChild(touche(k));});$('p2').appendChild(gg);
    });
    var cats=Object.keys(UN),h='<div class="grp">Grandeur</div><select id="cvCat"></select><div class="grp">Valeur à convertir</div><div class="cv" id="cvIn" style="color:var(--cy);border-color:var(--cy)">0</div>'+
      '<div class="grp">De</div><select id="cvDe"></select><div class="grp">Vers</div><select id="cvVers"></select><div class="cv" id="cvOut">0</div>'+
      '<div class="mut" style="margin-top:8px">La valeur convertie est le résultat affiché par la calculatrice (onglet BASE).</div>';
    $('p3').innerHTML=h;
    cats.forEach(function(c){var o=document.createElement('option');o.textContent=c;$('cvCat').appendChild(o);});
    $('cvCat').onchange=function(){convUnites();convMaj();};$('cvDe').onchange=$('cvVers').onchange=convMaj;
    convUnites();histRendre();
  }
  function convUnites(){
    var c=$('cvCat').value,u=Object.keys(UN[c].u);
    ['cvDe','cvVers'].forEach(function(id,n){var s=$(id);s.innerHTML='';u.forEach(function(x){var o=document.createElement('option');o.textContent=x;s.appendChild(o);});s.selectedIndex=Math.min(n,u.length-1);});
  }
  function enBase(c,u,x){if(c==='Température'){return u==='°C'?x+273.15:(u==='°F'?(x-32)*5/9+273.15:x);}return x*UN[c].u[u];}
  function deBase(c,u,x){if(c==='Température'){return u==='°C'?x-273.15:(u==='°F'?(x-273.15)*9/5+32:x);}return x/UN[c].u[u];}
  function convMaj(){
    var v=(val!==null)?val:(hist.length?hist[0].v:0),c=$('cvCat').value;
    $('cvIn').textContent=Calc.fmt(v);
    try{$('cvOut').textContent=Calc.fmt(deBase(c,$('cvVers').value,enBase(c,$('cvDe').value,v)));}catch(e){$('cvOut').textContent='Erreur';}
  }
  function histRendre(){
    var p=$('p4');if(!hist.length){p.innerHTML='<div class="mut">Aucun calcul pour le moment.</div>';return;}
    p.innerHTML='';
    hist.forEach(function(h){var d=document.createElement('div');d.className='hi';d.innerHTML='<small></small><b></b>';
      d.firstChild.textContent=h.e;d.lastChild.textContent='= '+h.r;
      d.addEventListener('click',function(){E=[h.r.replace('×10^','E')];tab('p1');maj();});p.appendChild(d);});
  }
  function tab(id){
    ['p1','p2','p3','p4'].forEach(function(p){$(p).classList.toggle('on',p===id);});
    document.querySelectorAll('.tab').forEach(function(t){t.classList.toggle('on',t.getAttribute('data-p')===id);});
    if(id==='p3')convMaj();
  }
  function mode(){var m=angles[(angles.indexOf(Calc.mode())+1)%3];Calc.mode(m);$('bMode').textContent=m;maj();}
  document.addEventListener('DOMContentLoaded',construire);
  return {tab:tab,mode:mode,maj:maj};
})();

/* =================== LOCKY : avatar, menu, échanges avec Python =================== */
var LK=(function(){
  var S={cfg:{messages:true,freq:'normal',coin:''},calc:{ok:true,raison:''}},mode='avatar';
  window.__lk_q=[];
  function ev(o){var q=window.__lk_q;if(o.a==='drag'&&o.ph==='m'||o.a==='audio'){var l=q[q.length-1];if(l&&l.a===o.a&&l.ph===o.ph&&l.k===o.k&&l.w===o.w){q[q.length-1]=o;return;}}q.push(o);}
  function $(i){return document.getElementById(i);}
  function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function setMode(m){var pm=mode;mode=m;document.body.className='m-'+m;if(m==='menu')rendre();if(m==='calc')C.maj();if(m==='param'){P.reset();P.rendre(true);}if(m==='evo'){if(pm==='rang')R.evoRendre();else R.evoOuvrir();}if(m!=='rang'&&m!=='rangm')R.stop();}
  var bt=null;
  function dire(t){
    var b=$('bulle');if(!b)return;
    if(bt){clearTimeout(bt);bt=null;}
    if(!t||S.cfg.messages===false){b.className='vide';b.textContent='';return;}
    b.textContent=t;b.className='n';
    bt=setTimeout(function(){b.className='vide';b.textContent='';},5000+Math.random()*2000);   /* le message disparaît après 5 à 7 s */
  }
  function chips(l,c,vide){
    if(!l||!l.length)return '<span class="mut">'+vide+'</span>';
    var col=c==='f'?'ok':'ko';
    return l.map(function(x){return '<div class="mini"><span class="n">'+esc(x[0])+'</span>'+pal(x[1],col,10,'s')+'<span class="p" style="color:var(--'+(c==='f'?'ok':'ro')+')">'+x[1]+'%</span></div>';}).join('');
  }
  function tog(k,lbl){return '<div class="sw"><span>'+lbl+'</span><div class="tog'+(S.cfg[k]!==false?' on':'')+'" onclick="LK.cfg(\''+k+'\','+(S.cfg[k]!==false?'false':'true')+')"></div></div>';}
  function opts(k,lst){return '<div class="opts">'+lst.map(function(o){return '<div class="o'+(S.cfg[k]===o[0]?' on':'')+'" onclick="LK.cfg(\''+k+'\',\''+o[0]+'\')">'+o[1]+'</div>';}).join('')+'</div>';}
  function rendre(){
    var s=S;
    var tot=s.total||0,rp=tot?s.reussite:0,ec=tot?s.echec:0;
    var h='<div class="sec"><div class="id"><img src="badges/locky.png"><div><div class="nom">'+esc(s.nom||'Locky')+'</div><div class="niv">NIV. '+(s.niveau||1)+'</div></div></div>'+
      '<div class="jl or"><span>CONNEXION QUOTIDIENNE</span><b>'+(s.pts||0)+'/7</b></div>'+palN(s.pts||0,7,'or','g')+'<div class="mut">Progression : '+(s.pts||0)+'/7 — chaque jour de connexion = +1 point ; à 7 points Locky gagne 1 niveau.</div></div>'+
      '<div class="grid2" style="margin-bottom:12px"><div class="kpi o"><b>'+(s.jours||0)+' j</b><span>Jours connectés</span></div><div class="kpi m"><b>'+(s.rp||0)+'</b><span>Points de rang</span></div></div>'+
      '<div class="sec"><h3>Analyse du joueur</h3>'+
      (tot?'<div class="jl ok"><span>RÉUSSITE</span><b>'+rp+'%</b></div>'+pal(rp,'ok',20,'g')+
        '<div class="jl ko"><span>ÉCHEC</span><b>'+ec+'%</b></div>'+pal(ec,'ko',20,'g')+
        '<div class="mut" style="margin:4px 0 10px">'+tot+' réponse(s) analysée(s)</div>'
        :'<div class="mut" style="margin-bottom:10px">Réponds à quelques questions : Locky pourra analyser ton jeu.</div>')+
      '<div class="mut" style="margin-bottom:5px;color:var(--ok)">POINTS FORTS</div><div style="margin-bottom:10px">'+chips(s.forts,'f','pas encore assez de données')+'</div>'+
      '<div class="mut" style="margin-bottom:5px;color:var(--ro)">POINTS FAIBLES</div><div>'+chips(s.faibles,'w','pas encore assez de données')+'</div></div>'+
      '<div class="sec"><h3>Records</h3><div class="grid2"><div class="kpi v"><b>'+(s.rp_best||0)+'</b><span>Meilleur score RP</span></div>'+
      '<div class="kpi o"><b>'+(s.note_best==null?'—':s.note_best+'/20')+'</b><span>Meilleure note examen</span></div></div></div>'+
      '<div class="sec"><h3>Paramètres de Locky</h3>'+tog('messages','Messages de Locky')+
      '<div class="sw" style="display:block"><div style="margin-bottom:6px">Fréquence des messages</div>'+opts('freq',[['calme','Calme'],['normal','Normal'],['bavard','Bavard']])+'</div>'+
      '<div class="sw" style="display:block"><div style="margin-bottom:6px">Position de Locky</div>'+opts('coin',[['hg','↖ Haut gauche'],['hd','↗ Haut droite'],['bg','↙ Bas gauche'],['bd','↘ Bas droite']])+
      '<div class="mut" style="margin-top:6px">Astuce : glisse Locky vers un coin pour le déplacer.</div></div></div>'+
      '<div class="big'+(s.calc&&s.calc.ok?'':' off')+'" onclick="LK.calc()">🧮 CALCULATRICE'+(s.calc&&s.calc.ok?'':' — INTERDITE')+'</div>'+
      (s.calc&&!s.calc.ok?'<div class="mut" style="text-align:center;margin-top:6px">'+esc(s.calc.raison)+'</div>':'');
    var sc=$('mcorps'),top=sc.scrollTop;sc.innerHTML=h;sc.scrollTop=top;
  }
  /* --- gestes sur l'avatar : tap = menu, double tap = excitation, glisser = changer de coin --- */
  var g=null,tapT=null;
  function sc(e){var d=window.devicePixelRatio||1;return {x:(e.screenX||0)*d,y:(e.screenY||0)*d,ok:!!(e.screenX||e.screenY)};}
  function gesteDebut(e){g={x:e.clientX,y:e.clientY,s:sc(e),drag:false};}
  function gesteBouge(e){
    if(!g)return;var dx=e.clientX-g.x,dy=e.clientY-g.y;
    if(!g.drag&&g.s.ok&&(Math.abs(dx)>10||Math.abs(dy)>10)){g.drag=true;ev({a:'drag',w:'avatar',ph:'s',x:g.s.x,y:g.s.y});}
    if(g.drag){var s=sc(e);ev({a:'drag',w:'avatar',ph:'m',x:s.x,y:s.y});}
  }
  function gesteFin(e){
    if(!g)return;var G=g;g=null;
    if(G.drag){ev({a:'drag',w:'avatar',ph:'e'});return;}
    var dx=e.clientX-G.x,dy=e.clientY-G.y;
    if(Math.abs(dx)>36||Math.abs(dy)>36){ev({a:'coin',dx:dx,dy:dy});return;}     /* secours si screenX est indisponible */
    if(tapT){clearTimeout(tapT);tapT=null;ev({a:'dbl'});return;}
    tapT=setTimeout(function(){tapT=null;ev({a:'tap'});},280);
  }
  function dragEntete(el,w){
    var d=false;
    el.addEventListener('pointerdown',function(e){if(e.target.closest&&e.target.closest('.bt'))return;var s=sc(e);if(!s.ok)return;d=true;
      try{el.setPointerCapture(e.pointerId);}catch(x){}ev({a:'drag',w:w,ph:'s',x:s.x,y:s.y});});
    el.addEventListener('pointermove',function(e){if(!d)return;var s=sc(e);ev({a:'drag',w:w,ph:'m',x:s.x,y:s.y});});
    var f=function(){if(d){d=false;ev({a:'drag',w:w,ph:'e'});}};
    el.addEventListener('pointerup',f);el.addEventListener('pointercancel',f);
  }
  document.addEventListener('DOMContentLoaded',function(){
    var a=$('av');
    /* pointer events uniquement : touch + souris émulée envoyaient 2 événements par appui (faux « double tap ») */
    a.addEventListener('pointerdown',function(e){e.preventDefault();gesteDebut(e);});
    a.addEventListener('pointermove',function(e){gesteBouge(e);});
    a.addEventListener('pointerup',function(e){e.preventDefault();gesteFin(e);});
    a.addEventListener('pointercancel',function(){g=null;});
    a.addEventListener('contextmenu',function(e){e.preventDefault();});
    dragEntete(document.querySelector('#calc .tete'),'calc');
    setMode('avatar');ev({a:'pret'});
  });
  return {
    maj:function(o){for(var k in o){if(k==='cfg'){S.cfg=o.cfg;}else S[k]=o[k];}
      if(o.bulle!==undefined){dire(o.bulle);}
      if(mode==='menu')rendre();else if(mode==='param')P.rendre();else if(mode==='evo')R.evoRendre();},
    mode:setMode,dire:dire,etat:function(){return S;},ev:ev,
    act:function(k){ev({a:'p',k:k});},lien:function(k){ev({a:'lien',k:k});},
    fermer:function(){ev({a:'fermer'});},
    reduire:function(){ev({a:'fermer'});},
    calc:function(){ev({a:'calc'});},
    cfg:function(k,v){S.cfg[k]=v;ev({a:'cfg',k:k,v:v});if(mode==='menu')rendre();}
  };
})();
"""


import param_page as _pp
import rangs_page as _rp
import pages_page as _pgp


def page_complete():
    """Document HTML complet (chargé une seule fois dans la WebView de Locky)."""
    return ('<!doctype html><html lang="fr"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">'
            '<style>' + CSS + _pp.CSS + _rp.CSS + _pgp.CSS + '</style></head><body class="m-avatar">' + HTML + _pp.HTML + _rp.HTML + _pgp.HTML +
            '<script>' + JS + _pp.JS + _rp.JS + _pgp.JS + '</script></body></html>')
