from flask import Flask, render_template, request, redirect, flash
import os
import requests

app = Flask(__name__)
app.secret_key = "microservices-ecommerce-secret-key"

CATALOG_SERVICE_URL = os.getenv("CATALOG_SERVICE_URL", "http://catalog-service:8001")
CART_SERVICE_URL = os.getenv("CART_SERVICE_URL", "http://cart-service:8002")
CHECKOUT_SERVICE_URL = os.getenv("CHECKOUT_SERVICE_URL", "http://checkout-service:8003")

USER_ID = "user1"


def get_products():
    try:
        response = requests.get(f"{CATALOG_SERVICE_URL}/products", timeout=5)
        return response.json()
    except Exception:
        return []


def get_cart():
    try:
        response = requests.get(f"{CART_SERVICE_URL}/cart/{USER_ID}", timeout=5)
        return response.json()
    except Exception:
        return {"userId": USER_ID, "items": []}


@app.route("/")
def index():
    products = get_products()
    cart = get_cart()

    product_map = {product["id"]: product for product in products}

    enriched_items = []
    total = 0.0

    for item in cart.get("items", []):
        product = product_map.get(item["productId"])

        if product:
            line_total = product["price"] * item["quantity"]
            total += line_total

            enriched_items.append({
                "productId": item["productId"],
                "name": product["name"],
                "price": product["price"],
                "quantity": item["quantity"],
                "lineTotal": round(line_total, 2)
            })

    cart["items"] = enriched_items
    cart_total = round(total, 2)

    return render_template(
        "index.html",
        products=products,
        cart=cart,
        cart_total=cart_total
    )


@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    product_id = int(request.form["product_id"])
    quantity = int(request.form.get("quantity", 1))

    if quantity < 1:
        flash("La quantité doit être supérieure à 0.", "error")
        return redirect("/")

    payload = {
        "productId": product_id,
        "quantity": quantity
    }

    try:
        response = requests.post(
            f"{CART_SERVICE_URL}/cart/{USER_ID}/items",
            json=payload,
            timeout=5
        )

        if response.status_code in [200, 201]:
            flash("Produit ajouté au panier.", "success")
        else:
            flash("Impossible d'ajouter le produit au panier.", "error")
    except Exception:
        flash("Erreur lors de l'ajout au panier.", "error")

    return redirect("/")


@app.route("/remove-from-cart", methods=["POST"])
def remove_from_cart():
    product_id = int(request.form["product_id"])

    try:
        response = requests.delete(
            f"{CART_SERVICE_URL}/cart/{USER_ID}/items/{product_id}",
            timeout=5
        )

        if response.status_code == 200:
            flash("Produit supprimé du panier.", "success")
        else:
            flash("Impossible de supprimer le produit du panier.", "error")
    except Exception:
        flash("Erreur lors de la suppression du produit.", "error")

    return redirect("/")


@app.route("/checkout", methods=["POST"])
def checkout():
    try:
        response = requests.post(
            f"{CHECKOUT_SERVICE_URL}/checkout/{USER_ID}",
            timeout=10
        )

        if response.status_code in [200, 201]:
            flash("Commande validée avec succès. Le panier a été vidé.", "success")
        else:
            try:
                error_detail = response.json().get("detail", "Erreur lors du checkout.")
            except Exception:
                error_detail = "Erreur lors du checkout."
            flash(error_detail, "error")
    except Exception:
        flash("Le service de checkout est indisponible.", "error")

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)