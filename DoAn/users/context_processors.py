def cart_count(request):
    cart = request.session.get("cart", {})

    tong = 0
    for item in cart.values():
        tong += item["qty"]

    return {"cart_count": tong}
