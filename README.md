# 📈 Binance Volatility Trading Bot

Bot de trading algorithmique développé en Python utilisant l’API Binance.

Le projet analyse la volatilité du marché afin de définir automatiquement des zones d’achat et de vente sur le BTC en temps réel.

⚠️ Projet expérimental / éducatif.

---

# ❤️ À propos du projet

Ce projet est très spécial pour moi :  
c’est littéralement le tout premier vrai projet que j’ai développé quand j’ai commencé à apprendre le code.

À cette époque, je découvrais :
- Python
- les APIs REST
- l’automatisation
- le trading algorithmique
- les systèmes temps réel

Je passais des journées entières à :
- tester des idées
- comprendre les erreurs
- relancer le script après chaque crash
- apprendre comment fonctionnaient les marchés
- essayer de construire un système autonome capable de prendre des décisions seul

Le code est imparfait.  
L’architecture est simple.  
Certaines décisions sont naïves.

Mais justement :  
ce projet représente mes débuts.

C’est le moment où j’ai compris que je voulais construire des systèmes complexes et automatisés.

Je laisse volontairement ce repository public comme archive de mon évolution en tant que développeur.

---

# 🚀 Fonctionnalités

- Connexion à l’API Binance
- Récupération du prix BTC en temps réel
- Analyse de volatilité historique
- Calcul automatique des seuils :
  - Take Profit
  - Stop Loss
- Achat / vente automatique
- Gestion du portefeuille Binance
- Affichage live des performances

---

# 🧠 Stratégie

Le bot :

1. Télécharge les données historiques (`klines`)
2. Calcule la volatilité avec l’écart-type (`standard deviation`)
3. Définit automatiquement :
   - une zone de vente haussière
   - une zone de vente baissière
4. Surveille le prix du marché en temps réel
5. Exécute des ordres automatiquement

---

# 📊 Exemple de logique

```python
z_vente = z_achat + (1.63 * (vol / 2))
z_vente1 = z_achat - (1.5 * (vol / 2))
```

Le système utilise la volatilité du marché pour ajuster dynamiquement les seuils.

---

# 📦 Installation

## 1. Cloner le projet

```bash
git clone https://github.com/theorick/trading_binance.git
cd trading_binance
```

## 2. Installer les dépendances

```bash
pip install requests numpy
```

---

# 🔑 Configuration API Binance

Ajouter vos clés API :

```python
API_KEY = 'YOUR_API_KEY'
API_SECRET = 'YOUR_API_SECRET'
```

⚠️ IMPORTANT :

- Activer uniquement le trading Spot
- Désactiver les retraits pour des raisons de sécurité

---

# ▶️ Lancer le bot

```bash
python bot.py
```

---

# 📈 Exemple de sortie console

```bash
prix d'achat : 29658.73
prix de vente : 30120.54
prix actuel : 29984.12

BTC : 0.0214
USDT : 145.22
Balance totale : 782.44$
```

---

# ⚙️ Paramètres modifiables

| Paramètre | Description |
|---|---|
| `interval = '30m'` | Intervalle des bougies |
| `symbol = 'BTCUSDT'` | Pair tradée |
| `1.63` | Multiplicateur take profit |
| `1.5` | Multiplicateur stop loss |

---

# 🛡️ Sécurité

Ne jamais commit :
- vos API keys
- vos secrets Binance

Ajouter un `.gitignore` :

```gitignore
.env
config.py
__pycache__/
```

---

# 📉 Risques

Le trading algorithmique comporte des risques importants :

- pertes financières
- bugs d’exécution
- erreurs API
- forte volatilité

Ce projet est principalement destiné à :
- l’apprentissage
- l’expérimentation
- la recherche

---

# 🔮 Améliorations possibles

- Dashboard web
- Backtesting
- Multi-assets
- Machine Learning
- Notifications Discord / Telegram
- Gestion avancée du risque
- Base de données des trades
- Analyse statistique avancée

---

# 🧪 Technologies utilisées

- Python
- Binance REST API
- Requests
- Statistics
- NumPy

---

# 📜 Licence

MIT License

---

# 👨‍💻 Auteur

Développé par Théo Meuriot.
```
