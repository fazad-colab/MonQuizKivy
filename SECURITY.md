# Politique de Sécurité

Nous prenons la sécurité de **Math Quiz Comores** très au sérieux. Si tu penses avoir découvert une vulnérabilité, merci de nous aider à protéger nos utilisateurs en la signalant de manière responsable.

## Versions supportées

Seules les versions les plus récentes reçoivent des mises à jour de sécurité. Nous te recommandons de toujours utiliser la dernière version disponible.

| Version | Supportée |
| :--- | :--- |
| 1.6.x | ✅ Oui |
| < 1.6 | ❌ Non |

## Comment signaler une vulnérabilité ?

**Merci de NE PAS créer de ticket (issue) public sur GitHub pour les problèmes de sécurité.** Les vulnérabilités sont des informations sensibles qui ne doivent pas être rendues publiques avant d'être corrigées.

Pour signaler un problème :
1. Envoie un e-mail à **omnimath.dev@gmail.com** (ou contacte-nous en privé via le groupe WhatsApp officiel).
2. Inclus dans ton message :
   - Une description claire de la faille.
   - Les étapes pour la reproduire (si possible).
   - L'impact potentiel (ex: vol de données, blocage de l'application).
   - Toute suggestion de correction (facultatif).

Nous nous engageons à :
- Accuser réception de ton signalement sous 48 heures.
- Te tenir informé de l'avancement de la correction.
- Te créditer (si tu le souhaites) dans les notes de version une fois la faille corrigée.

## Mesures de sécurité en place

Ce projet met en œuvre plusieurs pratiques pour protéger ses utilisateurs :

- **Analyse de code** : Utilisation des outils de sécurité de GitHub (Dependabot, analyse de secrets).
- **Backend Flask** : Le serveur tourne avec `debug=False` en production pour ne jamais exposer de traces d'erreurs sensibles[reference:3].
- **Validation des entrées** : Les API valident strictement les données reçues pour éviter les injections.
- **Pas de secrets dans le code** : Les clés API et mots de passe ne sont jamais stockés dans le code source.

## Bonnes pratiques pour les utilisateurs

- **Mises à jour** : Installe toujours la dernière version de l'application depuis la page officielle des Releases.
- **Mots de passe** : Utilise un mot de passe unique et fort pour ton compte Math Quiz Comores.
- **Méfiance** : Ne partage jamais ton identifiant ou ton mot de passe avec quelqu'un d'autre.

---
*Dernière mise à jour : Novembre 2026*
