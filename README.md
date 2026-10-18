# ntumba IA

Bienvenue dans le projet `ntumba IA`, un point de départ simple pour construire une application Python d'intelligence artificielle.

## Objectif

Ce dépôt contient une base propre et fonctionnelle pour :
- démarrer un projet Python rapidement,
- organiser le code de manière claire,
- préparer l'intégration d'une API IA (OpenAI, etc.),
- servir comme base pour un prototype ou une application interne.

## Structure du projet

```text
ntumba-ia/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── ntumba_ia/
│   ├── __init__.py
│   ├── __main__.py
│   └── app.py
└── tests/
    └── __init__.py
```

## Prérequis

- Python 3.10+
- pip

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Copiez le fichier d'exemple :

```bash
cp .env.example .env
```

Puis modifiez les valeurs si nécessaire.

## Lancer l'application

```bash
python -m ntumba_ia
```

## Exemple de sortie

```text
Bienvenue dans ntumba IA
Votre assistant est prêt.
```

## Personnalisation

Vous pouvez étendre le fichier `ntumba_ia/app.py` pour ajouter :
- des appels à une API d'IA,
- un chatbot en ligne de commande,
- une interface web,
- des fonctionnalités de traitement de texte, d'analyse ou d'automatisation.

## Licence

Ce projet est sous licence MIT.
