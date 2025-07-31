# ToBETTER

Prototype d'application d'aide aux paris sportifs.

Ce dépôt contient un squelette minimal avec :

- **Backend FastAPI** (`backend/app`)
  - Authentification basique (inscription, connexion)
  - Gestion des matchs et des prédictions
  - Ajout des favoris (matchs ou prédictions)
  - Route de leaderboard mensuel des équipes les plus victorieuses
  - Détection des value bets en comparant probabilité estimée et cote
  - Script de génération de données de démonstration
  - Schéma de base de données PostgreSQL (`backend/schema.sql`)
  
- **Frontend React** (`frontend`)
  - Pages Accueil, Connexion et Tableau de bord

Ce projet sert uniquement d'exemple simplifié pour le MVP.
