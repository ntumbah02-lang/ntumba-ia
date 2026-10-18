# ntumba IA Pricing

## Objectif

ntumba IA propose un modèle hybride :
- Open-source public (MIT)
- Version Pro / Commerciale payante
- Support premium et licences d'entreprise

## Modèle recommandé

### 1) Starter
- Prix : 19 € / mois
- Usage personnel
- 1 utilisateur
- Accès à la base du produit
- Support email standard

### 2) Pro
- Prix : 49 € / mois
- Usage professionnel
- 3 utilisateurs
- Accès aux fonctionnalités premium
- Support prioritaire
- Usage commercial

### 3) Enterprise
- Prix : sur devis
- Usage institutionnel / équipe / intégrations
- Accès multi-utilisateur
- SLA / support dédié
- Personnalisation / intégration de workflows

## Modèle de vente

### Option simple
- Vendre une souscription mensuelle / annuelle
- Clé de licence activée après paiement
- Validation de la clé sur chaque session d'usage ou au démarrage du système

### Option plus robuste
- Vendre une licence permanente + support annuel
- Contrat de support séparé selon les besoins

## Paiement recommandé

- Stripe pour le checkout et les webhooks
- Mise à disposition de la clé de licence dans le dashboard client
- Stockage de la licence dans SQLite ou Postgres

## Processus

1. L'utilisateur achète la licence sur le site
2. Stripe traite le paiement
3. Le webhook confirme la transaction
4. La clé est générée et émise
5. Le serveur valide la clé au démarrage / lors des actions Pro
6. Les fonctionnalités premium sont activées

## Recommandation finale

Pour un lancement, je recommande :
- Starter : 19 € / mois
- Pro : 49 € / mois
- Enterprise : sur devis

Cela permet d'obtenir un produit simple à vendre, avec un prix lisible et un modèle de monétisation clair.

## Important

Les documents juridiques doivent être validés par un avocat avant commercialisation sérieuse.
