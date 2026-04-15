from .models import Product


def seed_products(db):
    existing_products = db.query(Product).count()
    if existing_products > 0:
        return

    products = [
        Product(name="Clavier mécanique", description="Clavier RGB", price=49.99, stock=10),
        Product(name="Souris gaming", description="Souris optique", price=29.99, stock=15),
        Product(name="Casque audio", description="Casque sans fil", price=79.99, stock=8),

        Product(name="Écran 27 pouces", description="Écran IPS Full HD 144 Hz", price=219.99, stock=6),
        Product(name="Tapis de souris XL", description="Grand tapis antidérapant", price=19.99, stock=20),
        Product(name="Microphone USB", description="Micro pour streaming et visioconférence", price=59.99, stock=9),
        Product(name="Webcam HD", description="Webcam 1080p avec autofocus", price=44.99, stock=11),
        Product(name="Chaise gaming", description="Chaise ergonomique avec support lombaire", price=189.99, stock=4),
        Product(name="Bureau assis-debout", description="Bureau réglable en hauteur", price=329.99, stock=3),
        Product(name="Support écran", description="Bras articulé pour moniteur", price=39.99, stock=10),
        Product(name="Enceintes de bureau", description="Paire d’enceintes compactes", price=34.99, stock=12),
        Product(name="Hub USB-C", description="Hub multiport pour setup moderne", price=49.99, stock=14),
        Product(name="Lampe LED bureau", description="Éclairage réglable pour bureau", price=27.99, stock=16),
        Product(name="Station d’accueil", description="Dock USB-C pour ordinateur portable", price=99.99, stock=7),
        Product(name="SSD externe 1 To", description="Stockage rapide portable", price=89.99, stock=13),
        Product(name="Clé Wi-Fi", description="Adaptateur Wi-Fi USB haute vitesse", price=24.99, stock=17),
        Product(name="Support casque", description="Support design pour casque audio", price=18.99, stock=18),
        Product(name="Repose-poignets", description="Repose-poignets ergonomique", price=14.99, stock=22),
        Product(name="Clavier compact 75%", description="Clavier mécanique format compact", price=69.99, stock=8),
        Product(name="Souris sans fil", description="Souris légère et silencieuse", price=24.99, stock=19),
    ]

    db.add_all(products)
    db.commit()