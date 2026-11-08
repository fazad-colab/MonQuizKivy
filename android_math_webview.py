# -*- coding: utf-8 -*-
"""
android_math_webview.py — rendu mathématique KaTeX dans une WebView Android (ou aperçu texte sur PC)

 * KaTeX est chargé depuis le dossier LOCAL ./katex (ou ./Katex : la casse est détectée automatiquement).
 * Thème « dark web » : fond noir violacé, néons cyan / magenta / vert.
 * Si KaTeX local est absent ET pas de connexion : un avertissement visible s'affiche.
"""
import os
import weakref
from html import escape

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.utils import platform

from latex_utils import latex_vers_texte

if platform == "android":
    from android.runnable import run_on_ui_thread
else:
    def run_on_ui_thread(func):
        return func

DOSSIER_APP = os.path.dirname(os.path.abspath(__file__))
LETTRES = "ABCDEFGH"
CDN = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist"


# ---------------------------------------------------------------------------
# Détection FLEXIBLE du dossier KaTeX : accepte katex / Katex / KATEX / KaTeX
# (sur Android le FS est sensible à la casse : c'était la cause du rendu cassé)
# ---------------------------------------------------------------------------
def _trouver_dossier_katex():
    for nom in ("katex", "Katex", "KATEX", "KaTeX"):
        chemin = os.path.join(DOSSIER_APP, nom)
        if all(os.path.exists(os.path.join(chemin, *p)) for p in
               (("katex.min.js",), ("katex.min.css",), ("contrib", "auto-render.min.js"))):
            return nom
    return None


KATEX_DIR_NOM = _trouver_dossier_katex()          # ex. "katex" ou None
DOSSIER_KATEX = os.path.join(DOSSIER_APP, KATEX_DIR_NOM) if KATEX_DIR_NOM else None


def katex_local_disponible():
    return KATEX_DIR_NOM is not None


def _html(txt):
    """Échappe le HTML mais conserve $...$ ; les \\n DANS les $...$ deviennent des espaces,
    les \\n HORS des $...$ deviennent <br>. (Sinon une formule multi-ligne casse le rendu KaTeX.)"""
    txt = str(txt or "")
    if "$" not in txt:
        return escape(txt, quote=False).replace("\n", "<br>")
    parts, i = [], 0
    while i < len(txt):
        j = txt.find("$", i)
        if j == -1:
            parts.append(("prose", txt[i:]))
            break
        if j > i:
            parts.append(("prose", txt[i:j]))
        k = txt.find("$", j + 1)
        if k == -1:
            parts.append(("math", txt[j:]))
            break
        parts.append(("math", txt[j:k + 1]))
        i = k + 1
    out = []
    for typ, seg in parts:
        if typ == "math":
            out.append(escape(seg.replace("\n", " "), quote=False))
        else:
            out.append(escape(seg, quote=False).replace("\n", "<br>"))
    return "".join(out)


CSS = """
:root{--bg:#05050a;--card:rgba(18,16,36,.78);--bord:rgba(0,240,255,.28);--cy:#00f0ff;--mg:#ff2bd6;--ok:#39ff88;--ko:#ff3b5c;--tx:#e9eaff;--mut:#8a8fb8}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{height:100%%;margin:0;background:var(--bg);color:var(--tx);font-family:ui-monospace,"JetBrains Mono","Roboto Mono",Menlo,Consolas,monospace}
body{padding:10px 10px 18px;font-size:calc(var(--z,1)*%(fs)spx);line-height:1.55;display:flex;flex-direction:column;min-height:100%%;
 background-image:linear-gradient(rgba(0,240,255,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(0,240,255,.045) 1px,transparent 1px);
 background-size:26px 26px}
.tete{display:flex;justify-content:space-between;align-items:center;font-size:.72em;letter-spacing:.14em;color:var(--cy);text-transform:uppercase;margin:0 2px 8px}
.tete .pt{color:var(--mg);text-shadow:0 0 8px var(--mg)}
.carte{background:var(--card);border:1px solid var(--bord);border-radius:14px;padding:14px;margin-bottom:10px;
 box-shadow:0 0 0 1px rgba(255,43,214,.06),0 8px 28px rgba(0,0,0,.55),inset 0 0 22px rgba(0,240,255,.05);backdrop-filter:blur(6px)}
.enonce{font-size:1.12em;font-family:-apple-system,"Segoe UI",Roboto,sans-serif}
.etiq{font-size:.68em;letter-spacing:.2em;color:var(--mg);margin-bottom:6px;text-transform:uppercase}
.etiq::before{content:"> ";color:var(--cy)}
.props{flex:1 1 auto;display:flex;flex-direction:column}
.opt{flex:1 0 auto;min-height:52px;touch-action:manipulation;cursor:pointer;-webkit-user-select:none;user-select:none;display:flex;gap:10px;align-items:center;padding:11px 12px;margin:8px 0;border-radius:12px;border:1px solid rgba(255,255,255,.12);
 background:rgba(255,255,255,.035);transition:all .18s ease;font-family:-apple-system,"Segoe UI",Roboto,sans-serif}
.opt .lt{flex:0 0 30px;height:30px;border-radius:9px;display:grid;place-items:center;font-family:ui-monospace,monospace;font-weight:700;
 color:var(--cy);border:1px solid var(--cy);box-shadow:0 0 10px rgba(0,240,255,.35)}
.opt .tx{flex:1;min-width:0;overflow-x:auto;overflow-y:hidden;overflow-wrap:anywhere;word-break:break-word}
.opt:active{transform:scale(.985)}
body.lock .opt{pointer-events:none}
body:not(.cliq) .opt{cursor:default}
.opt.sel{border-color:var(--mg);background:rgba(255,43,214,.12);box-shadow:0 0 16px rgba(255,43,214,.35)}
.opt.sel .lt{color:var(--mg);border-color:var(--mg);box-shadow:0 0 10px rgba(255,43,214,.5)}
.opt.bon{border-color:var(--ok);background:rgba(57,255,136,.12);box-shadow:0 0 18px rgba(57,255,136,.4)}
.opt.bon .lt{color:var(--ok);border-color:var(--ok);box-shadow:0 0 10px rgba(57,255,136,.6)}
.opt.mauv{border-color:var(--ko);background:rgba(255,59,92,.12);box-shadow:0 0 18px rgba(255,59,92,.4)}
.opt.mauv .lt{color:var(--ko);border-color:var(--ko)}
.verdict{display:none;font-weight:700;letter-spacing:.08em;margin-bottom:8px}
.verdict.v{color:var(--ok);text-shadow:0 0 10px var(--ok)}.verdict.f{color:var(--ko);text-shadow:0 0 10px var(--ko)}
#expl{display:none;border-color:rgba(255,184,0,.4)}
#expl .etiq{color:#ffb800}
.envoye{display:none;text-align:center;color:var(--cy);letter-spacing:.1em;font-size:.85em;padding:8px}
.carte.ok-c{border-color:rgba(57,255,136,.55)}.carte.ko-c{border-color:rgba(255,59,92,.55)}
.corps{overflow-x:auto;font-family:-apple-system,"Segoe UI",Roboto,sans-serif}
.katex{font-size:1.06em;color:#fff}.katex-display{overflow-x:auto;overflow-y:hidden}
#mq-avert{display:none;color:#ffb800;padding:12px;border:1px solid #ffb800;border-radius:10px;margin-top:12px;font-size:.85em;line-height:1.5}
.tete{flex:none}.etiq{flex:none}
.carte.moi{border-color:rgba(255,43,214,.5)}.carte.ia{border-color:rgba(0,240,255,.5)}
/* height:100%% (fiable sur toutes WebViews) au lieu de 100vh */
body.q{height:100%%;min-height:0;overflow:hidden}
body.q #cEnonce{flex:0 1 auto;min-height:0;overflow-y:auto}
body.q .props{flex:1 1 auto;min-height:0;overflow-y:auto;margin-bottom:6px}
body.q .verdict,body.q .envoye{flex:none}
body.q.rev{height:auto;min-height:100%%;overflow-y:auto}
body.q.rev #cEnonce,body.q.rev .props{flex:none;overflow:visible}
@keyframes pop{from{transform:scale(.97);opacity:.4}to{transform:none;opacity:1}}
.carte{animation:pop .22s ease-out}
"""

JS = """
function mqRendre(){
  if(typeof renderMathInElement!=='undefined'){
    renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false},
      {left:'\\\\(',right:'\\\\)',display:false},{left:'\\\\[',right:'\\\\]',display:true}],throwOnError:false,strict:false});
  }
  mqAjuster();
  if(document.body.getAttribute('data-bas')){window.scrollTo(0,document.body.scrollHeight);}
}
function mqAjuster(){
  var b=document.body;if(!b||!b.classList.contains('q')||b.classList.contains('rev')){return;}
  var e=document.getElementById('cEnonce'),p=document.querySelector('.props');if(!e||!p){return;}
  // réduction douce : jamais en dessous de 0.85 (au-delà, on laisse scroller)
  var z=1;b.style.setProperty('--z','1');
  for(var i=0;i<6;i++){
    var trop=(e.scrollHeight>e.clientHeight+2)||(p.scrollHeight>p.clientHeight+2);
    if(!trop||z<=0.85){break;}
    z=Math.round((z-0.03)*100)/100;b.style.setProperty('--z',String(z));
  }
}
window.addEventListener('resize',function(){mqAjuster();});
window.addEventListener('load',function(){setTimeout(mqAjuster,60);setTimeout(mqAjuster,400);});
window.__mq_choix=-1;
document.addEventListener('click',function(e){
  var o=e.target&&e.target.closest?e.target.closest('.opt'):null;
  if(!o||!document.body.classList.contains('cliq')||document.body.classList.contains('lock')){return;}
  var i=parseInt(o.getAttribute('data-i'));if(isNaN(i)){return;}
  window.__mq_choix=i;document.body.classList.add('lock');
  document.querySelectorAll('.opt').forEach(function(x,k){x.classList.toggle('sel',k===i);});
});
function mqVerrouiller(){document.body.classList.add('lock');}
function mqCharger(src,cb,err){
  var s=document.createElement('script');s.src=src;s.async=true;
  s.onload=cb;
  s.onerror=function(){if(err){err();}else{console.warn('mq: chargement impossible '+src);}};
  document.head.appendChild(s);
}
function mqDemarrer(){
  if(typeof katex!=='undefined'&&typeof renderMathInElement!=='undefined'){mqRendre();return;}
  var avert=document.getElementById('mq-avert');
  var fini=false;
  var minuteur=setTimeout(function(){if(!fini&&avert){avert.style.display='block';}},5000);
  var l=document.createElement('link');l.rel='stylesheet';l.href='%(cdn)s/katex.min.css';document.head.appendChild(l);
  mqCharger('%(cdn)s/katex.min.js',function(){
    mqCharger('%(cdn)s/contrib/auto-render.min.js',function(){
      fini=true;clearTimeout(minuteur);mqRendre();
    },function(){fini=true;clearTimeout(minuteur);if(avert){avert.style.display='block';}});
  },function(){fini=true;clearTimeout(minuteur);if(avert){avert.style.display='block';}});
}
function mqMarquer(i){document.querySelectorAll('.opt').forEach(function(o,k){o.classList.toggle('sel',k===i);});
  var e=document.getElementById('envoye');if(e){e.style.display='block';}}
function mqReveler(choisi,correct){
  document.body.classList.add('lock');document.body.classList.add('rev');
  document.querySelectorAll('.opt').forEach(function(o,k){o.classList.remove('sel');
    if(k===correct){o.classList.add('bon');} else if(k===choisi){o.classList.add('mauv');}});
  var v=document.getElementById('verdict');
  if(v){v.style.display='block';
    if(choisi===correct){v.className='verdict v';v.textContent='> BONNE RÉPONSE';}
    else if(choisi<0){v.className='verdict f';v.textContent='> TEMPS ÉCOULÉ';}
    else{v.className='verdict f';v.textContent='> MAUVAISE RÉPONSE';}}
  var x=document.getElementById('expl');if(x){x.style.display='block';}
  if(v){v.scrollIntoView({behavior:'smooth',block:'start'});}
}
(function(){
  var go=function(){setTimeout(mqDemarrer,30);};
  if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',go);}else{go();}
})();
"""


def _head_katex():
    """Retourne les balises <link>/<script> de KaTeX (chemin = nom réel du dossier détecté)."""
    if not KATEX_DIR_NOM:
        return ""
    return (
        f'<link rel="stylesheet" href="{KATEX_DIR_NOM}/katex.min.css">'
        f'<script src="{KATEX_DIR_NOM}/katex.min.js"></script>'
        f'<script src="{KATEX_DIR_NOM}/contrib/auto-render.min.js"></script>'
    )


AVERT_HTML = (
    '<div id="mq-avert">'
    "⚠ Les formules mathématiques ne peuvent pas s'afficher : KaTeX n'est pas installé et la connexion Internet est indisponible."
    " Vérifie que le dossier <code>katex/</code> est bien présent à la racine de l'application."
    "</div>"
)


def generer_page(q, titre_tete="", points="", avec_explication=True, taille_police=16, cliquable=False):
    """Construit la page HTML complète pour un dict question (voir moteur_quiz.generer_question)."""
    head_katex = _head_katex()
    opts = ""
    for i, o in enumerate(q.get("options", [])):
        opts += f'<div class="opt" id="o{i}" data-i="{i}"><div class="lt">{LETTRES[i]}</div><div class="tx">{_html(o)}</div></div>'
    expl = ""
    if avec_explication and q.get("explication"):
        expl = f'<div class="carte" id="expl"><div class="etiq">Démonstration</div><div>{_html(q["explication"])}</div></div>'
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
{head_katex}<style>{CSS % {"fs": taille_police}}</style><script>{JS % {"cdn": CDN}}</script></head><body class="q {'cliq' if cliquable else ''}">
<div class="tete"><span>{_html(titre_tete)}</span><span class="pt">{_html(points)}</span></div>
<div class="carte" id="cEnonce"><div class="etiq">Énoncé</div><div class="enonce">{_html(q.get("enonce", ""))}</div></div>
<div class="carte props"><div class="etiq">Propositions</div>{opts}</div>
<div class="envoye" id="envoye">&gt; RÉPONSE ENVOYÉE — EN ATTENTE DES AUTRES…</div>
<div class="verdict" id="verdict"></div>{expl}{AVERT_HTML}
</body></html>"""


def generer_page_document(titre, cartes, taille_police=16, defiler_bas=False):
    """Page de lecture avec rendu mathématique. cartes = [(étiquette, texte_avec_$maths$, style)]."""
    head_katex = _head_katex()
    corps = ""
    for etiq, texte, style in cartes:
        cl = {"ok": " ok-c", "ko": " ko-c", "moi": " moi", "ia": " ia"}.get(style, "")
        corps += f'<div class="carte{cl}"><div class="etiq">{_html(etiq)}</div><div class="corps">{_html(texte)}</div></div>'
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
{head_katex}<style>{CSS % {"fs": taille_police}}</style><script>{JS % {"cdn": CDN}}</script></head><body{' data-bas="1"' if defiler_bas else ''}>
<div class="tete"><span>{_html(titre)}</span></div>{corps}{AVERT_HTML}</body></html>"""


class AndroidMathWebView(Widget):
    """Widget Kivy : WebView native sur Android ; aperçu texte (avec boutons) sur PC."""

    _instances = weakref.WeakSet()

    def __init__(self, html="", **kwargs):
        self.sous_entete = kwargs.pop("sous_entete", True)
        super().__init__(**kwargs)
        self.html = html
        self._native_view = None
        self._detruit = False
        self._visible = True
        self._base_url = "file://" + DOSSIER_APP + "/"
        self._derniere_question = None
        self._on_choix = None
        self._verrouille = False
        self._poll_ev = None
        self._frame_ev = None
        self._cb = None
        self._dernier_layout = None
        AndroidMathWebView._instances.add(self)

        self.bind(parent=self._on_parent)

        if platform == "android":
            Clock.schedule_once(lambda dt: self._create_native_view(), 0)
        else:
            self._fallback_box = BoxLayout(orientation="vertical", spacing=dp(4))
            self._fallback = Label(text="", halign="left", valign="top", markup=True, color=(0.9, 0.95, 1, 1))
            self._fallback.bind(size=lambda inst, val: setattr(inst, "text_size", (val[0] - 16, val[1])))
            self._fallback_opts = BoxLayout(orientation="vertical", size_hint_y=None, height=0, spacing=dp(4))
            self._fallback_box.add_widget(self._fallback)
            self._fallback_box.add_widget(self._fallback_opts)
            self.add_widget(self._fallback_box)
            self.bind(pos=self._maj_fallback, size=self._maj_fallback)

    # ------------------------------------------------------------------ API
    def set_question(self, q, titre_tete="", points="", avec_explication=True, cliquable=False, on_choix=None):
        self._derniere_question = (q, avec_explication)
        self._verrouille = False
        self._on_choix = on_choix if cliquable else None
        self.html = generer_page(q, titre_tete, points, avec_explication, cliquable=bool(cliquable and on_choix))
        if platform == "android":
            if self._native_view is not None:
                self._charger_html()
                self._demarrer_poll()
        else:
            lignes = [f"[b][color=00f0ff]{titre_tete}[/color][/b]   [color=ff2bd6]{points}[/color]", "",
                      q.get("enonce_txt") or latex_vers_texte(q.get("enonce", "")), ""]
            textes = q.get("options_txt") or [latex_vers_texte(x) for x in q.get("options", [])]
            self._fallback_opts.clear_widgets()
            if self._on_choix:
                for i, o in enumerate(textes):
                    b = Button(text=f"{LETTRES[i]}  {o}", size_hint_y=None, height=dp(44), halign="center", valign="middle")
                    b.bind(on_release=lambda inst, k=i: self._choix_utilisateur(k))
                    self._fallback_opts.add_widget(b)
                self._fallback_opts.height = dp(48) * len(textes)
            else:
                self._fallback_opts.height = 0
                for i, o in enumerate(textes):
                    lignes.append(f"[b]{LETTRES[i]}[/b]  {o}")
            self._fallback.text = "\n".join(lignes)

    def set_document(self, titre, cartes, defiler_bas=False):
        self._on_choix = None
        self.html = generer_page_document(titre, cartes, defiler_bas=defiler_bas)
        if platform == "android":
            if self._native_view is not None:
                self._charger_html()
        else:
            lignes = [f"[b][color=00f0ff]{titre}[/color][/b]", ""]
            for etiq, texte, style in cartes:
                lignes += [f"[b]{etiq}[/b]", latex_vers_texte(texte), ""]
            self._fallback_opts.clear_widgets()
            self._fallback_opts.height = 0
            self._fallback.text = "\n".join(lignes)

    def set_content(self, enonce, options=None, bonne_reponse="", explication=""):
        q = {"enonce": enonce, "options": options or [], "explication": explication, "bonne_reponse": bonne_reponse}
        self.set_question(q)

    def marquer(self, index):
        self._js(f"mqMarquer({int(index)})")

    def verrouiller(self):
        self._verrouille = True
        self._js("mqVerrouiller()")
        if platform != "android" and hasattr(self, "_fallback_opts"):
            for b in self._fallback_opts.children:
                b.disabled = True

    def reveler(self, choisi, correct):
        self._verrouille = True
        self._js(f"mqReveler({int(choisi)},{int(correct)})")
        if platform != "android" and self._derniere_question:
            q = self._derniere_question[0]
            for b in self._fallback_opts.children:
                b.disabled = True
            self._fallback.text += f"\n\n[b]{'Bonne réponse' if choisi == correct else 'Faux'}[/b] — {LETTRES[correct]}\n{q.get('explication_txt', '')}"

    def set_visible(self, visible):
        self._visible = visible
        self._dernier_layout = None
        if platform != "android" and hasattr(self, "_fallback_box"):
            self._fallback_box.opacity = 1 if visible else 0

    @classmethod
    def masquer_tous(cls):
        for w in list(cls._instances):
            w.set_visible(False)

    @classmethod
    def afficher_tous(cls):
        for w in list(cls._instances):
            w.set_visible(True)

    # ---------------------------------------------------- clic sur une proposition
    def _choix_utilisateur(self, i):
        cb = self._on_choix
        if cb is None or self._verrouille or self._detruit:
            return
        self._verrouille = True
        cb(i)

    def _demarrer_poll(self):
        if platform != "android" or self._poll_ev is not None or self._on_choix is None:
            return
        self._poll_ev = Clock.schedule_interval(self._poll_choix, 0.12)

    def _creer_callback(self):
        from jnius import PythonJavaClass, java_method

        class _Rappel(PythonJavaClass):
            __javainterfaces__ = ["android/webkit/ValueCallback"]
            __javacontext__ = "app"

            def __init__(self, fn):
                super().__init__()
                self._fn = fn

            @java_method("(Ljava/lang/Object;)V")
            def onReceiveValue(self, valeur):
                try:
                    self._fn(valeur)
                except Exception as e:
                    print(f"[AndroidMathWebView] rappel: {e}")
        return _Rappel(self._valeur_recue)

    def _valeur_recue(self, valeur):
        try:
            brut = valeur.toString() if hasattr(valeur, "toString") else valeur
            i = int(str(brut).strip().strip('"'))
        except Exception:
            return
        if i >= 0:
            Clock.schedule_once(lambda dt: self._choix_utilisateur(i), 0)

    def _poll_choix(self, dt):
        if self._native_view is None or self._detruit:
            return
        if self._on_choix is None or self._verrouille:
            return
        if self._cb is None:
            self._cb = self._creer_callback()
        webview, cb = self._native_view, self._cb

        @run_on_ui_thread
        def lire():
            try:
                webview.evaluateJavascript(
                    "(function(){var c=window.__mq_choix;window.__mq_choix=-1;return (typeof c==='number')?c:-1;})()", cb)
            except Exception as e:
                print(f"[AndroidMathWebView] lecture du choix: {e}")
        lire()

    # ---------------------------------------------------------- PC (aperçu)
    def _maj_fallback(self, *args):
        if hasattr(self, "_fallback_box"):
            self._fallback_box.pos = self.pos
            self._fallback_box.size = self.size

    # -------------------------------------------------------- cycle de vie
    def _on_parent(self, instance, parent):
        if parent is None:
            Clock.schedule_once(self.detruire, 0)

    def detruire(self, *args):
        if self.parent is not None:
            return
        self._detruit = True
        for ev in (self._poll_ev, self._frame_ev):
            if ev is not None:
                ev.cancel()
        self._poll_ev = self._frame_ev = None
        if platform != "android" or self._native_view is None:
            return
        webview = self._native_view
        self._native_view = None

        @run_on_ui_thread
        def remove():
            try:
                p = webview.getParent()
                if p is not None:
                    p.removeView(webview)
                webview.destroy()
            except Exception as e:
                print(f"[AndroidMathWebView] Erreur destruction: {e}")
        remove()

    def _create_native_view(self):
        if platform != "android" or self._native_view is not None or self._detruit:
            return

        @run_on_ui_thread
        def create():
            try:
                from jnius import autoclass
                WebView = autoclass("android.webkit.WebView")
                WebViewClient = autoclass("android.webkit.WebViewClient")
                FrameLayoutParams = autoclass("android.widget.FrameLayout$LayoutParams")
                Gravity = autoclass("android.view.Gravity")
                Color = autoclass("android.graphics.Color")
                PythonActivity = autoclass("org.kivy.android.PythonActivity")

                activity = PythonActivity.mActivity
                webview = WebView(activity)
                webview.setWebViewClient(WebViewClient())
                webview.setBackgroundColor(Color.parseColor("#05050A"))
                webview.setVerticalScrollBarEnabled(False)
                webview.setVisibility(4)

                st = webview.getSettings()
                st.setJavaScriptEnabled(True)
                st.setDomStorageEnabled(True)
                st.setLoadsImagesAutomatically(True)
                st.setAllowFileAccess(True)
                st.setAllowFileAccessFromFileURLs(True)
                st.setAllowUniversalAccessFromFileURLs(True)
                st.setSupportZoom(False)
                st.setBuiltInZoomControls(False)

                params = FrameLayoutParams(1, 1)
                params.gravity = Gravity.TOP | Gravity.LEFT
                try:
                    conteneur = PythonActivity.mLayout
                    conteneur.addView(webview, params)
                except Exception:
                    activity.addContentView(webview, params)

                self._native_view = webview
                self._charger_html()
                Clock.schedule_once(lambda dt: self._demarrer_suivi(), 0)
            except Exception as e:
                print(f"[AndroidMathWebView] Erreur création: {e}")
        create()

    def _demarrer_suivi(self):
        if self._detruit or self._frame_ev is not None:
            return
        self._frame_ev = Clock.schedule_interval(self._sync_frame, 1 / 20.0)
        self._demarrer_poll()

    def _charger_html(self):
        if self._native_view is None or not self.html:
            return
        webview, html, base = self._native_view, self.html, self._base_url

        @run_on_ui_thread
        def charger():
            try:
                webview.loadDataWithBaseURL(base, html, "text/html", "UTF-8", None)
            except Exception as e:
                print(f"[AndroidMathWebView] Erreur chargement: {e}")
        charger()

    def _js(self, code):
        if platform != "android" or self._native_view is None:
            return
        webview = self._native_view

        @run_on_ui_thread
        def exe():
            try:
                webview.evaluateJavascript(code, None)
            except Exception as e:
                print(f"[AndroidMathWebView] Erreur JS: {e}")
        exe()

    # ------------------------------------------------ position de la vue native
    def _zone_visible(self):
        if not self._visible or self.get_root_window() is None:
            return None
        x, y = self.to_window(self.x, self.y)
        g, b, d, h = x, y, x + self.width, y + self.height
        p = self.parent
        for _ in range(60):
            if p is None or not hasattr(p, "parent"):
                break
            if getattr(p, "opacity", 1) <= 0.01:
                return None
            if isinstance(p, ScrollView):
                px, py = p.to_window(p.x, p.y)
                g, b = max(g, px), max(b, py)
                d, h = min(d, px + p.width), min(h, py + p.height)
            p = p.parent
        if self.sous_entete:
            try:
                app = App.get_running_app()
                en_tete = getattr(app, "info_layout", None)
                if en_tete is not None and en_tete.get_root_window() is not None:
                    _, ey = en_tete.to_window(en_tete.x, en_tete.y)
                    h = min(h, ey - dp(4))
            except Exception:
                pass
        if d - g < 2 or h - b < 2:
            return None
        return g, b, d, h

    def _sync_frame(self, dt):
        if self._native_view is None or self._detruit:
            return
        z = self._zone_visible()
        if z is None:
            cle = (0, 0, 0, 0, False)
        else:
            g, b, d, h = z
            cle = (int(g), int(Window.height - h), int(d - g), int(h - b), True)
        if cle == self._dernier_layout:
            return
        self._dernier_layout = cle
        webview = self._native_view
        x, top, w, hh, visible = cle

        @run_on_ui_thread
        def appliquer():
            try:
                if visible:
                    params = webview.getLayoutParams()
                    params.width = max(1, w)
                    params.height = max(1, hh)
                    params.setMargins(x, max(0, top), 0, 0)
                    webview.setLayoutParams(params)
                    webview.requestLayout()          # ← indispensable sur certains Android
                    webview.invalidate()
                webview.setVisibility(0 if visible else 4)
            except Exception as e:
                print(f"[AndroidMathWebView] Erreur layout: {e}")
        appliquer()