from .models import Product


def seed_products(db):
    existing_products = db.query(Product).count()
    if existing_products > 0:
        return

    products = [
        Product(
            name="Clavier mécanique",
            description="Clavier RGB avec switches réactifs",
            price=49.99,
            stock=10
        ),
        Product(
            name="Souris gaming",
            description="Souris optique précise et ergonomique",
            price=29.99,
            stock=15
        ),
        Product(
            name="Casque audio",
            description="Casque sans fil confortable pour le quotidien",
            price=79.99,
            stock=8
        ),
        Product(
            name="Écran 27 pouces",
            description="Moniteur IPS Full HD 144 Hz",
            price=219.99,
            stock=6
        ),
        Product(
            name="Écran ultrawide 34 pouces",
            description="Moniteur incurvé pour productivité et multitâche",
            price=429.99,
            stock=4
        ),
        Product(
            name="Tapis de souris XL",
            description="Grand tapis antidérapant pour setup complet",
            price=19.99,
            stock=20
        ),
        Product(
            name="Microphone USB",
            description="Micro clair pour streaming et visioconférence",
            price=59.99,
            stock=9
        ),
        Product(
            name="Webcam HD",
            description="Webcam 1080p avec autofocus",
            price=44.99,
            stock=11
        ),
        Product(
            name="Support écran",
            description="Bras articulé pour moniteur réglable",
            price=39.99,
            stock=10
        ),
        Product(
            name="Lampe LED bureau",
            description="Éclairage réglable pour espace de travail",
            price=27.99,
            stock=16
        ),
        Product(
            name="Station d’accueil USB-C",
            description="Dock multiport pour setup moderne",
            price=99.99,
            stock=7
        ),
        Product(
            name="Hub USB-C",
            description="Hub compact avec plusieurs ports essentiels",
            price=49.99,
            stock=14
        ),
        Product(
            name="Enceintes de bureau",
            description="Paire d’enceintes compactes pour bureau",
            price=34.99,
            stock=12
        ),
        Product(
            name="Support casque",
            description="Support design pour ranger un casque audio",
            price=18.99,
            stock=18
        ),
        Product(
            name="Repose-poignets",
            description="Accessoire ergonomique pour clavier",
            price=14.99,
            stock=22
        ),
        Product(
            name="SSD externe 1 To",
            description="Stockage portable rapide et compact",
            price=89.99,
            stock=13
        ),
        Product(
            name="Clé Wi-Fi USB",
            description="Adaptateur Wi-Fi haute vitesse",
            price=24.99,
            stock=17
        ),
        Product(
            name="Chaise gaming",
            description="Chaise ergonomique avec support lombaire",
            price=189.99,
            stock=4
        ),
        Product(
            name="Bureau assis-debout",
            description="Bureau réglable en hauteur pour plus de confort",
            price=329.99,
            stock=3
        ),
        Product(
            name="Clavier compact 75%",
            description="Clavier mécanique format compact",
            price=69.99,
            stock=8
        ),
        Product(
            name="Souris sans fil",
            description="Souris légère et silencieuse",
            price=24.99,
            stock=19
        ),
        Product(
            name="Pavé numérique",
            description="Pavé numérique externe pour plus de confort",
            price=21.99,
            stock=15
        ),
        Product(
            name="Ventilateur PC RGB",
            description="Ventilateur silencieux avec éclairage RGB",
            price=16.99,
            stock=25
        ),
        Product(
            name="Barre lumineuse monitor",
            description="Éclairage LED à fixer au-dessus de l’écran",
            price=39.99,
            stock=9
        ),
        Product(
            name="Chargeur sans fil",
            description="Socle de charge rapide pour smartphone",
            price=29.99,
            stock=14
        ),
        Product(
            name="Support ordinateur portable",
            description="Support aluminium pour améliorer la posture",
            price=32.99,
            stock=12
        ),
        Product(
            name="Câble HDMI 2.1",
            description="Câble haute vitesse pour écran ou TV",
            price=12.99,
            stock=30
        ),
        Product(
            name="Multiprise parafoudre",
            description="Multiprise sécurisée pour setup complet",
            price=26.99,
            stock=18
        ),
        Product(
            name="Boîtier PC moyen tour",
            description="Boîtier sobre avec bon airflow",
            price=89.99,
            stock=5
        ),
        Product(
            name="Clavier bureautique",
            description="Clavier silencieux pour usage quotidien",
            price=22.99,
            stock=16
        ),
    ]

    db.add_all(products)
    db.commit()