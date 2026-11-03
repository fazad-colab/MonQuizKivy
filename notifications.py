"""Rappels périodiques affichés pendant que l'application est ouverte."""

import random

from kivy.clock import Clock
from kivy.utils import platform
from plyer import notification


MESSAGES_RAPPEL = [
    ("Petit rappel", "Une courte séance de révision peut faire la différence !"),
    ("À toi de jouer !", "Prêt pour quelques questions de mathématiques ?"),
    ("Continue tes progrès", "Reviens réviser un chapitre quand tu as un moment."),
]


def start_periodic_notifications(app, min_delay=2 * 60 * 60, max_delay=4 * 60 * 60):
    """Démarre des notifications espacées de 2 à 4 heures, app ouverte seulement."""
    if getattr(app, "_rappels_demarre", False):
        return
    app._rappels_demarre = True

    def programmer_prochain_rappel(*_):
        # Un rappel n'est pas programmé avant que le précédent soit déclenché.
        delai = random.randint(min_delay, max_delay)
        Clock.schedule_once(envoyer_rappel, delai)

    def notifier_si_autorise(*_):
        try:
            titre, message = random.choice(MESSAGES_RAPPEL)
            notification.notify(
                title=titre,
                message=message,
                app_name="Math Quiz Comores",
                timeout=10,
            )
        except Exception as erreur:
            # Ne jamais empêcher l'application de fonctionner si les notifications
            # ne sont pas disponibles ou ont été refusées.
            print(f"Notification non envoyée : {erreur}")

    def envoyer_rappel(_dt):
        if platform == "android":
            try:
                from android.permissions import request_permissions

                def resultat_permission(permissions, grants):
                    if grants and all(grants):
                        notifier_si_autorise()
                    programmer_prochain_rappel()

                request_permissions(
                    ["android.permission.POST_NOTIFICATIONS"],
                    resultat_permission,
                )
                return
            except Exception as erreur:
                print(f"Permission notification indisponible : {erreur}")
        else:
            notifier_si_autorise()
        programmer_prochain_rappel()

    # Premier rappel après un délai aléatoire, pas immédiatement au démarrage.
    programmer_prochain_rappel()
