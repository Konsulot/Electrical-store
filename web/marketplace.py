from flask import Flask, render_template, request, redirect, url_for, session, flash
import grpc
import os
from cart_pb2_grpc import CartServiceStub
from cart_pb2 import CartItem, AddItemRequest, RemoveItemRequest, GetCartRequest, CartResponse, CartStatus
from user_pb2 import AuthRequest
from user_pb2_grpc import UserServiceStub
from product_pb2 import ProductCategory, ProductListRequest
from product_pb2_grpc import ProductServiceStub
from recommendation_pb2 import RecommendationRequest
from recommendation_pb2_grpc import RecommendationServiceStub

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

user_host = os.getenv("USER_HOST", "localhost")
user_channel = grpc.insecure_channel(f"{user_host}:50051")
user_client = UserServiceStub(user_channel)

product_host = os.getenv("PRODUCT_HOST", "localhost")
product_channel = grpc.insecure_channel(f"{product_host}:50052")
product_client = ProductServiceStub(product_channel)

recommendation_host = os.getenv("RECOMMENDATION_HOST", "localhost")
recommendation_channel = grpc.insecure_channel(f"{recommendation_host}:50053")
recommendation_client = RecommendationServiceStub(recommendation_channel)

cart_host = os.getenv("CART_HOST", "localhost")
cart_channel = grpc.insecure_channel(f"{cart_host}:50054")
cart_client = CartServiceStub(cart_channel)


@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    return render_template("homepage.html", username=username)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        auth_request = AuthRequest(username=username, password=password)
        auth_response = user_client.Authenticate(auth_request)
        if auth_response.user_id != 0:
            session["user_id"] = auth_response.user_id
            session["username"] = username
            flash("Logged in successfully!", "success")
            return redirect(url_for("home"))
        flash("Invalid username or password", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    flash("Logged out successfully!", "success")
    return redirect(url_for("login"))


@app.route("/products")
def products_list():
    products = []
    for category in ProductCategory.keys():
        if category.isnumeric():
            continue
        product_list_request = ProductListRequest(category=ProductCategory.Value(category))
        product_list_response = product_client.GetProducts(product_list_request)
        products.extend(product_list_response.products)
    return render_template("products.html", products=products)


@app.route("/recommendations")
def recommendations():
    recommendations_request = RecommendationRequest(
        user_id=session["user_id"],
        category=ProductCategory.MOBILE,
        max_results=3
    )
    recommendations_response = recommendation_client.Recommend(recommendations_request)
    recommendations = recommendations_response.products
    return render_template("recommendations.html", recommendations=recommendations)


@app.route("/product/<int:id>")
def product_detail(id):
    for category in ProductCategory.keys():
        if category.isnumeric():
            continue
        product_list_request = ProductListRequest(category=ProductCategory.Value(category))
        product_list_response = product_client.GetProducts(product_list_request)
        for product in product_list_response.products:
            if product.id == id:
                return render_template("product_detail.html", product=product)
    return "Product not found", 404


@app.route("/cart")
def cart():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    cart_request = GetCartRequest(cart_id=user_id)

    try:
        cart_response = cart_client.GetCart(cart_request)
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            # Create an empty cart if not found
            cart_response = CartResponse(cart_id=user_id, items=[], status=CartStatus.ACTIVE)
        else:
            flash("Failed to retrieve cart.", "danger")
            return redirect(url_for("home"))

    return render_template("cart.html", cart=cart_response)


@app.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    quantity = int(request.form["quantity"])  # Получаем количество из формы

    # Find the product details
    product = None
    for category in ProductCategory.keys():
        if category.isnumeric():
            continue
        product_list_request = ProductListRequest(category=ProductCategory.Value(category))
        product_list_response = product_client.GetProducts(product_list_request)
        for p in product_list_response.products:
            if p.id == product_id:
                product = p
                break
        if product:
            break

    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for("products_list"))

    cart_item = CartItem(id=product.id, title=product.title, quantity=quantity)
    add_item_request = AddItemRequest(cart_id=user_id, item=cart_item)
    cart_response = cart_client.AddItem(add_item_request)

    if cart_response.status == CartStatus.ACTIVE:
        flash(f"{product.title} (x{quantity}) added to cart.", "success")
    else:
        flash("Failed to add item to cart.", "danger")

    return redirect(url_for("cart"))



@app.route("/cart/remove", methods=["POST"])
def remove_from_cart():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    item_id = int(request.form["item_id"])
    remove_item_request = RemoveItemRequest(cart_id=user_id, item_id=item_id)
    cart_response = cart_client.RemoveItem(remove_item_request)

    if cart_response.status == CartStatus.ACTIVE:
        flash("Item removed from cart.", "success")
    else:
        flash("Failed to remove item from cart.", "danger")

    return redirect(url_for("cart"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
