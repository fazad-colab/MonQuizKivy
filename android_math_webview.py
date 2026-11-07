# -*- coding: utf-8 -*-
"""
android_math_webview.py — rendu mathématique KaTeX dans une WebView Android (ou aperçu texte sur PC)

 * KaTeX est chargé depuis le dossier LOCAL  ./katex  (à la racine du projet, à côté de main.py) :
       katex/katex.min.css   katex/katex.min.js   katex/contrib/auto-render.min.js   katex/fonts/*
   -> fonctionne hors connexion. Si le dossier est absent/incomplet : repli automatique sur le CDN.
 * Thème « dark web » : fond noir violacé, néons cyan / magenta / vert, cartes en verre, police mono.
 * La correction (bonne/mauvaise réponse + explication LaTeX) s'affiche DANS la page :
   une vue native Android passe toujours AU-DESSUS de Kivy, donc un Popup Kivy serait caché derrière.
"""
import os
import weakref
from html import escape

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.utils import platform

from latex_utils import latex_vers_texte

if platform == "android":
    from android.runnable import run_on_ui_thread
else:
    def run_on_ui_thread(func):
        return func

DOSSIER_APP = os.path.dirname(os.path.abspath(__file__))
DOSSIER_KATEX = os.path.join(DOSSIER_APP, "katex")
LETTRES = "ABCDEFGH"
CDN = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist"


def katex_local_disponible():
    return all(os.path.exists(os.path.join(DOSSIER_KATEX, *p)) for p in
               (("katex.min.js",), ("katex.min.css",), ("contrib", "auto-render.min.js")))


def _html(txt):
    """Échappe le HTML mais conserve $...$ et \\ ; les retours à la ligne deviennent <br>."""
    return escape(str(txt or ""), quote=False).replace("\n", "<br>")


CSS = """
:root{--bg:#05050a;--card:rgba(18,16,36,.78);--bord:rgba(0,240,255,.28);--cy:#00f0ff;--mg:#ff2bd6;--ok:#39ff88;--ko:#ff3b5c;--tx:#e9eaff;--mut:#8a8fb8}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;background:var(--bg);color:var(--tx);font-family:ui-monospace,"JetBrains Mono","Roboto Mono",Menlo,Consolas,monospace}
body{padding:10px 10px 18px;font-size:%(fs)spx;line-height:1.55;
 background-image:linear-gradient(rgba(0,240,255,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(0,240,255,.045) 1px,transparent 1px);
 background-size:26px 26px}
.tete{display:flex;justify-content:space-between;align-items:center;font-size:.72em;letter-spacing:.14em;color:var(--cy);text-transform:uppercase;margin:0 2px 8px}
.tete .pt{color:var(--mg);text-shadow:0 0 8px var(--mg)}
.carte{background:var(--card);border:1px solid var(--bord);border-radius:14px;padding:14px;margin-bottom:10px;
 box-shadow:0 0 0 1px rgba(255,43,214,.06),0 8px 28px rgba(0,0,0,.55),inset 0 0 22px rgba(0,240,255,.05);backdrop-filter:blur(6px)}
.enonce{font-size:1.12em;font-family:-apple-system,"Segoe UI",Roboto,sans-serif}
.etiq{font-size:.68em;letter-spacing:.2em;color:var(--mg);margin-bottom:6px;text-transform:uppercase}
.etiq::before{content:"> ";color:var(--cy)}
.opt{display:flex;gap:10px;align-items:center;padding:11px 12px;margin:8px 0;border-radius:12px;border:1px solid rgba(255,255,255,.12);
 background:rgba(255,255,255,.035);transition:all .18s ease;font-family:-apple-system,"Segoe UI",Roboto,sans-serif}
.opt .lt{flex:0 0 30px;height:30px;border-radius:9px;display:grid;place-items:center;font-family:ui-monospace,monospace;font-weight:700;
 color:var(--cy);border:1px solid var(--cy);box-shadow:0 0 10px rgba(0,240,255,.35)}
.opt .tx{flex:1;min-width:0;overflow-x:auto;overflow-y:hidden}
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
.katex{font-size:1.06em;color:#fff}.katex-display{overflow-x:auto;overflow-y:hidden}
@keyframes pop{from{transform:scale(.97);opacity:.4}to{transform:none;opacity:1}}
.carte{animation:pop .22s ease-out}
"""

JS = """
function mqRendre(){
  if(typeof renderMathInElement==='undefined'){return;}
  renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false},
    {left:'\\\\(',right:'\\\\)',display:false},{left:'\\\\[',right:'\\\\]',display:true}],throwOnError:false,strict:false});
}
function mqCharger(src,cb){var s=document.createElement('script');s.src=src;s.onload=cb;document.head.appendChild(s);}
function mqDemarrer(){
  if(typeof katex==='undefined'||typeof renderMathInElement==='undefined'){
    // repli CDN : KaTeX local absent ou incomplet
    var l=document.createElement('link');l.rel='stylesheet';l.href='%(cdn)s/katex.min.css';document.head.appendChild(l);
    mqCharger('%(cdn)s/katex.min.js',function(){mqCharger('%(cdn)s/contrib/auto-render.min.js',mqRendre);});
  } else {mqRendre();}
}
function mqMarquer(i){document.querySelectorAll('.opt').forEach(function(o,k){o.classList.toggle('sel',k===i);});
  var e=document.getElementById('envoye');if(e){e.style.display='block';}}
function mqReveler(choisi,correct){
  document.querySelectorAll('.opt').forEach(function(o,k){o.classList.remove('sel');
    if(k===correct){o.classList.add('bon');} else if(k===choisi){o.classList.add('mauv');}});
  var v=document.getElementById('verdict');
  if(v){v.style.display='block';
    if(choisi===correct){v.className='verdict v';v.textContent='> BONNE RÉPONSE';}
    else if(choisi<0){v.className='verdict f';v.textContent='> TEMPS ÉCOULÉ';}
    else{v.className='verdict f';v.textContent='> MAUVAISE RÉPONSE';}}
  var x=document.getElementById('expl');if(x){x.style.display='block';}
  window.scrollTo({top:document.body.scrollHeight,behavior:'smooth'});
}
document.addEventListener('DOMContentLoaded',function(){setTimeout(mqDemarrer,30);});
"""


def generer_page(q, titre_tete="", points="", avec_explication=True, taille_police=16):
    """Construit la page HTML complète pour un dict question (voir moteur_quiz.generer_question)."""
    local = katex_local_disponible()
    head_katex = (
        '<link rel="stylesheet" href="katex/katex.min.css">'
        '<script src="katex/katex.min.js"></script>'
        '<script src="katex/contrib/auto-render.min.js"></script>'
    ) if local else ""
    opts = ""
    for i, o in enumerate(q.get("options", [])):
        opts += f'<div class="opt" id="o{i}"><div class="lt">{LETTRES[i]}</div><div class="tx">{_html(o)}</div></div>'
    expl = ""
    if avec_explication and q.get("explication"):
        expl = f'<div class="carte" id="expl"><div class="etiq">Démonstration</div><div>{_html(q["explication"])}</div></div>'
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
{head_katex}<style>{CSS % {"fs": taille_police}}</style><script>{JS % {"cdn": CDN}}</script></head><body>
<div class="tete"><span>{_html(titre_tete)}</span><span class="pt">{_html(points)}</span></div>
<div class="carte"><div class="etiq">Énoncé</div><div class="enonce">{_html(q.get("enonce", ""))}</div></div>
<div class="carte"><div class="etiq">Propositions</div>{opts}</div>
<div class="envoye" id="envoye">&gt; RÉPONSE ENVOYÉE — EN ATTENTE DES AUTRES…</div>
<div class="verdict" id="verdict"></div>{expl}
</body></html>"""


class AndroidMathWebView(Widget):
    """Widget Kivy : WebView native sur Android ; aperçu texte sur PC."""

    _instances = weakref.WeakSet()

    def __init__(self, html="", **kwargs):
        super().__init__(**kwargs)
        self.html = html
        self._native_view = None
        self._detruit = False
        self._visible = True
        self._base_url = "file://" + DOSSIER_APP + "/"
        self._derniere_question = None
        AndroidMathWebView._instances.add(self)

        self.bind(pos=self._schedule_sync, size=self._schedule_sync)
        self.bind(parent=self._on_parent)

        if platform == "android":
            Clock.schedule_once(lambda dt: self._create_native_view(), 0)
        else:
            self._fallback = Label(text="", halign="left", valign="top", markup=True, color=(0.9, 0.95, 1, 1))
            self._fallback.bind(size=lambda inst, val: setattr(inst, "text_size", (val[0] - 16, val[1])))
            self.add_widget(self._fallback)
            self.bind(pos=self._maj_fallback, size=self._maj_fallback)

    # ------------------------------------------------------------------ API
    def set_question(self, q, titre_tete="", points="", avec_explication=True):
        """Affiche une question (dict du moteur)."""
        self._derniere_question = (q, avec_explication)
        self.html = generer_page(q, titre_tete, points, avec_explication)
        if platform == "android":
            if self._native_view is not None:
                self._charger_html()
        else:
            lignes = [f"[b][color=00f0ff]{titre_tete}[/color][/b]   [color=ff2bd6]{points}[/color]", "", q.get("enonce_txt") or latex_vers_texte(q.get("enonce", "")), ""]
            for i, o in enumerate(q.get("options_txt") or [latex_vers_texte(x) for x in q.get("options", [])]):
                lignes.append(f"[b]{LETTRES[i]}[/b]  {o}")
            self._fallback.text = "\n".join(lignes)

    def set_content(self, enonce, options=None, bonne_reponse="", explication=""):
        """Compatibilité avec l'ancienne API."""
        q = {"enonce": enonce, "options": options or [], "explication": explication, "bonne_reponse": bonne_reponse}
        self.set_question(q)

    def marquer(self, index):
        """Élève : met en évidence l'option choisie (sans dire si elle est juste)."""
        self._js(f"mqMarquer({int(index)})")

    def reveler(self, choisi, correct):
        """Montre vert/rouge + explication."""
        self._js(f"mqReveler({int(choisi)},{int(correct)})")
        if platform != "android" and self._derniere_question:
            q = self._derniere_question[0]
            self._fallback.text += f"\n\n[b]{'Bonne réponse' if choisi == correct else 'Faux'}[/b] — {LETTRES[correct]}\n{q.get('explication_txt', '')}"

    def set_visible(self, visible):
        """Cache/affiche la vue native (indispensable avant d'ouvrir un Popup Kivy)."""
        self._visible = visible
        if platform == "android" and self._native_view is not None:
            view = self._native_view

            @run_on_ui_thread
            def _vis():
                try:
                    view.setVisibility(0 if visible else 4)   # VISIBLE / INVISIBLE
                except Exception as e:
                    print(f"[AndroidMathWebView] visibilité: {e}")
            _vis()

    @classmethod
    def masquer_tous(cls):
        for w in list(cls._instances):
            w.set_visible(False)

    @classmethod
    def afficher_tous(cls):
        for w in list(cls._instances):
            w.set_visible(True)

    # ---------------------------------------------------------- PC (aperçu)
    def _maj_fallback(self, *args):
        if hasattr(self, "_fallback"):
            self._fallback.pos = self.pos
            self._fallback.size = self.size

    # -------------------------------------------------------- cycle de vie
    def _on_parent(self, instance, parent):
        if parent is not None:
            self._schedule_sync()
        else:
            Clock.schedule_once(self.detruire, 0)

    def _schedule_sync(self, *args):
        if platform == "android":
            Clock.schedule_once(lambda dt: self._sync_native_view(), 0)

    def detruire(self, *args):
        if self.parent is not None:
            return
        self._detruit = True
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

                st = webview.getSettings()
                st.setJavaScriptEnabled(True)
                st.setDomStorageEnabled(True)
                st.setLoadsImagesAutomatically(True)
                # KaTeX local : accès aux fichiers de l'application (css, js, polices)
                st.setAllowFileAccess(True)
                st.setAllowFileAccessFromFileURLs(True)
                st.setAllowUniversalAccessFromFileURLs(True)
                st.setSupportZoom(False)
                st.setBuiltInZoomControls(False)

                params = FrameLayoutParams(1, 1)
                params.gravity = Gravity.TOP | Gravity.LEFT
                activity.addContentView(webview, params)

                self._native_view = webview
                self._appliquer_layout()
                if not self._visible:
                    webview.setVisibility(4)
                self._charger_html()
            except Exception as e:
                print(f"[AndroidMathWebView] Erreur création: {e}")
        create()

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

    def _sync_native_view(self):
        if platform == "android" and self._native_view is not None:
            self._appliquer_layout()

    def _appliquer_layout(self):
        if self._native_view is None:
            return
        webview = self._native_view
        w = max(1, int(self.width))
        h = max(1, int(self.height))
        x = int(self.x)
        top = max(0, int(Window.height - self.top))

        @run_on_ui_thread
        def lay():
            try:
                params = webview.getLayoutParams()
                params.width = w
                params.height = h
                params.setMargins(x, top, 0, 0)
                webview.setLayoutParams(params)
            except Exception as e:
                print(f"[AndroidMathWebView] Erreur layout: {e}")
        lay()
