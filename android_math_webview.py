from kivy.clock import Clock
from kivy.metrics import dp
from kivy.utils import platform
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window


class AndroidMathWebView(Widget):
    """WebView Android native affichée au-dessus de la fenêtre Kivy."""

    def __init__(self, html, **kwargs):
        super().__init__(**kwargs)
        self.html = html
        self._native_view = None

        self.bind(pos=self._schedule_sync, size=self._schedule_sync)
        self.bind(parent=self._on_parent)

        if platform == "android":
            Clock.schedule_once(lambda dt: self._create_native_view(), 0)
        else:
            # Fallback de développement ; la vraie WebView est Android uniquement.
            self.add_widget(Label(
                text="La WebView native est disponible dans l’application Android.",
                text_size=(Window.width - dp(30), None),
                halign="center",
                valign="middle",
            ))

    def _on_parent(self, instance, parent):
        self._schedule_sync()

    def _schedule_sync(self, *args):
        if platform == "android":
            Clock.schedule_once(lambda dt: self._sync_native_view(), 0)

    def _create_native_view(self):
        if platform != "android" or self._native_view is not None:
            return

        from android.runnable import run_on_ui_thread

        @run_on_ui_thread
        def create():
            try:
                from jnius import autoclass

                WebView = autoclass("android.webkit.WebView")
                WebViewClient = autoclass("android.webkit.WebViewClient")
                FrameLayoutParams = autoclass(
                    "android.widget.FrameLayout$LayoutParams"
                )
                Gravity = autoclass("android.view.Gravity")
                View = autoclass("android.view.View")
                PythonActivity = autoclass("org.kivy.android.PythonActivity")

                activity = PythonActivity.mActivity
                webview = WebView(activity)
                webview.setWebViewClient(WebViewClient())

                settings = webview.getSettings()
                settings.setJavaScriptEnabled(True)
                settings.setDomStorageEnabled(True)

                params = FrameLayoutParams(1, 1)
                params.gravity = Gravity.TOP | Gravity.LEFT
                activity.addContentView(webview, params)

                self._native_view = webview
                self._layout_params = params
                self._frame_layout_params = FrameLayoutParams
                self._gravity = Gravity
                self._view_constants = View
                self._sync_native_view()

            except Exception as exc:
                print(f"Erreur création WebView Android : {exc}")

        create()

    def set_html(self, html):
        self.html = html
        self._load_html()

    def _load_html(self):
        if platform != "android" or self._native_view is None:
            return

        from android.runnable import run_on_ui_thread

        @run_on_ui_thread
        def load():
            try:
                # Base HTTPS pour autoriser le chargement de KaTeX depuis son CDN.
                self._native_view.loadDataWithBaseURL(
                    "https://quiz.local/",
                    self.html,
                    "text/html",
                    "UTF-8",
                    None,
                )
            except Exception as exc:
                print(f"Erreur chargement WebView : {exc}")

        load()

    def _sync_native_view(self):
        if platform != "android" or self._native_view is None:
            return

        from android.runnable import run_on_ui_thread

        @run_on_ui_thread
        def sync():
            try:
                GAP_HAUT = int(dp(250)) 

                width = max(1, int(self.width))
                height = max(1, int(self.height) + GAP_HAUT)
                top = max(0, int(Window.height - self.top) - GAP_HAUT)

                params = self._native_view.getLayoutParams()
                params.width = width
                params.height = height
                params.gravity = self._gravity.TOP | self._gravity.LEFT
                params.setMargins(int(self.x), top, 0, 0)
            
                self._native_view.setLayoutParams(params)
                
                if self.parent is None:
                    self._native_view.setVisibility(self._view_constants.GONE)
                else:
                    self._native_view.setVisibility(self._view_constants.VISIBLE)
                    self._native_view.loadDataWithBaseURL(
                        "https://quiz.local/",
                        self.html,
                        "text/html",
                        "UTF-8",
                        None,
                    )
            except Exception as exc:
                print(f"Erreur positionnement WebView : {exc}")

        sync()