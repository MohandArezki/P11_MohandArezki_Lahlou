# OpenClassrooms - Développeur d'application Python -

**Livrable du Projet 11 : Améliorez une application Web Python par des tests et du débogage**

---

## Présentation du projet

Le projet constitue un POC (proof of concept) visant à présenter une version allégée de la plateforme de réservation de compétitions. L'objectif est de maintenir une structure légère tout en tirant parti des retours des utilisateurs pour améliorer le produit. Vous pouvez télécharger le projet à partir de ce [lien](https://github.com/MohandArezki/P11_MohandArezki_Lahlou.git).

**Objectifs du projet :**
- Identifier et corriger les bugs existants.
- Implémenter de nouvelles fonctionnalités en réponse aux retours utilisateurs.
- Établir une suite de tests exhaustive avec Pytest et Locust.

*Remarque :* Chaque correction ou nouvelle fonctionnalité est développée sur une branche dédiée pour une gestion plus efficace du processus.

---

## Récupération du code source

```bash
git clone https://github.com/MohandArezki/P11_MohandArezki_Lahlou.git
cd P11_MohandArezki_Lahlou 
python3 -m venv env 
source env/bin/activate
pip install -r requirements.txt
```

---

## Utilisation

1. Lancer le serveur Flask :

```bash
flask run
```

2. Accéder au site en visitant l'adresse par défaut : [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## Tests

### Tests unitaires / tests d'intégration

Les tests unitaires et d'intégration sont exécutés avec [Pytest](https://docs.pytest.org/en/7.4.3/index.html) (version 7.4.3).

Pour exécuter l'ensemble des tests unitaires et d'intégration, utilisez la commande :

```bash
pytest tests
```

Pour générer le rapport au format HTML, utilisez la commande :

```bash
pytest --html=pytest_report.html 
```

Le module [Coverage](https://coverage.readthedocs.io/en/7.3.4/) (version 7.3.4) est utilisé pour le rapport de couverture des tests.
pour exploiter ce module, exécutez les commandes suivantes :

Pour generer le rapport :

```bash
coverage run -m pytest
```

Pour afficher le rapport :

```bash
coverage report
```

Pour generer le rapport au format html :

```bash
coverage html
```

### Test de performances

Un test de performance peut être effectué avec le module [Locust](https://locust.io) (version 2.20.0). Pour lancer le serveur de test, utilisez la commande :

```bash
locust -u 6 -H http://127.0.0.1:5000 -f tests/test_performance/locustfile.py
```

Rendez-vous sur [http://localhost:8089](http://localhost:8089).

### Rapports

Les captures d'écran des derniers rapports de tests sont disponibles dans le dossier 'reports'.

- [Rapport Pytest](reports/pytest_report.html) (tous les tests réussis)

- [Rapport de couverture](reports/htmlcov/index.html) (100% de couverture)

- [Rapport de performances Locust](reports/report_1703703479.7864704.html) (6 utilisateurs, 1 par seconde)

---
