# 🛒 Microservices E-Commerce (DevOps Project)

## 📌 Description

Ce projet est une application e-commerce basée sur une architecture **microservices**, conçue pour mettre en pratique des concepts DevOps, cloud et backend.

Il simule un workflow complet :
- affichage d’un catalogue
- gestion d’un panier
- passage de commande
- communication inter-services
- gestion multi-base de données

L’ensemble est orchestré avec **Docker Compose**.

---

## 🏗️ Architecture

### Services applicatifs
- **web-ui** (Flask) → interface utilisateur
- **catalog-service** (FastAPI + MySQL) → gestion des produits
- **cart-service** (FastAPI + DynamoDB Local) → gestion du panier
- **checkout-service** (FastAPI + Redis) → orchestration de commande
- **orders-service** (FastAPI + PostgreSQL + RabbitMQ) → gestion des commandes

### Services techniques
- **MySQL** → base catalogue
- **PostgreSQL** → base commandes
- **DynamoDB Local** → stockage panier
- **Redis** → cache checkout
- **RabbitMQ** → messaging asynchrone

---

## 🔄 Flux fonctionnel

1. L’utilisateur consulte le catalogue via le `web-ui`
2. Il ajoute des produits au panier (`cart-service`)
3. Le checkout :
   - récupère le panier
   - récupère les infos produits
   - calcule le total
4. Une commande est créée via `orders-service`
5. Un message est envoyé via RabbitMQ
6. Le panier est automatiquement vidé

---

## ⚙️ Stack technique

### Backend
- Python
- FastAPI
- Flask

### Data
- MySQL
- PostgreSQL
- DynamoDB Local
- Redis

### Messaging
- RabbitMQ

### DevOps
- Docker
- Docker Compose

---

## 🚀 Lancement du projet

### 1. Cloner le repo

```bash
git clone <repo-url>
cd microservices-ecommerce

2. Lancer les services
docker compose up --build -d
3. Vérifier les conteneurs
docker ps
🌐 Accès aux services
Service	URL
Web UI	http://localhost:8080

Catalog API	http://localhost:8001/docs

Cart API	http://localhost:8002/docs

Checkout API	http://localhost:8003/docs

Orders API	http://localhost:8004/docs

RabbitMQ UI	http://localhost:15672
RabbitMQ credentials
user: guest
password: guest
🧪 Exemple de tests
Ajouter au panier
curl -X POST http://localhost:8002/cart/user1/items \
  -H "Content-Type: application/json" \
  -d '{"productId":1,"quantity":2}'
Voir le panier
curl http://localhost:8002/cart/user1
Checkout
curl -X POST http://localhost:8003/checkout/user1
✅ Fonctionnalités implémentées
Architecture microservices complète
Communication inter-services (HTTP + async)
Multi-base de données (SQL + NoSQL)
Cache avec Redis
Messaging avec RabbitMQ
UI simple avec Flask
Panier dynamique
Checkout complet
Vidage automatique du panier après commande
Healthchecks Docker