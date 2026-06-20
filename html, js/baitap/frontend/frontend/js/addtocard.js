let gioHang = JSON.parse(localStorage.getItem("gioHang") || "[]");
const addToCartButtons = document.querySelectorAll(".add-to-cart");
function cartCount() {
    let cart = JSON.parse(localStorage.getItem("gioHang") || "[]");
    let totalQty = cart.reduce((sum, item) => sum + (item.qty || 0), 0); //Dùng hàm reduce để tính tổng các thuộc tính qty của sản phẩm có trong mảng
    const cartCount = document.getElementById("cart-count");
    if (cartCount) {
        cartCount.innerText = totalQty;
    }
}
cartCount();

addToCartButtons.forEach(function(button) {
    button.addEventListener("click", function(e) {
        e.preventDefault();
        const productContainer = button.closest(".single-products");
        
        if (productContainer) {
            const productId = productContainer.id;
            const sanPhamDaCo = gioHang.find(item => item.id === productContainer.id);
            if (sanPhamDaCo) {
                sanPhamDaCo.qty += 1;
            } else{
                const productImage = productContainer.querySelector(".img").src;
                const productPrice = productContainer.querySelector(".price").textContent;
                const productName = productContainer.querySelector(".name").textContent;
                const objCon = {
                    id: productId,
                    image: productImage,
                    price: productPrice,
                    name: productName,
                    qty: 1
                };
                gioHang.push(objCon);
            }
            localStorage.setItem("gioHang", JSON.stringify(gioHang));
            cartCount();
            console.log(gioHang);
        }
    });
});

