let getLocal = localStorage.getItem("gioHang");
if (getLocal) {
    let gioHang = JSON.parse(getLocal);
    const tbody = document.getElementById("cart-table");

    function updateTotalPrice() {
        const cartSubTotal = document.querySelector(".cart_sub_total");
        if (!cartSubTotal) return;
        let subTotal = 0;
        const allTotals = document.querySelectorAll(".cart_total_price"); 
        allTotals.forEach(total => {
            let totalNum = parseFloat(total.innerText.replace(/[^0-9.-]+/g,"")) || 0;
            subTotal += totalNum;
        });
        cartSubTotal.innerText = "$" + subTotal;
    }

    tbody.innerHTML = (gioHang).map(item => {
        let priceNum = 0;
        if (item.price) {
            priceNum = parseFloat(item.price.replace(/[^0-9.-]+/g,"")); // Loại bỏ ký tự không phải số và dấu chấm thập phân
        }
        let total = priceNum * item.qty;
        return `
        <tr id="${item.id}">
            <td class="cart_product">
                <img src="${item.image}" width="110">
            </td>
            <td class="cart_description">
                <h4>${item.name}</h4>
                <p>Web ID: ${item.id}</p>
            </td>
            <td class="cart_price">
                <p>${item.price}</p>
            </td>
            <td class="cart_quantity">
                <div class="cart_quantity_button">
                    <a class="cart_quantity_up" style="cursor: pointer;"> + </a>
                    <input class="cart_quantity_input" type="text" name="quantity" value="${item.qty}" autocomplete="off" size="2">
                    <a class="cart_quantity_down" style="cursor: pointer;"> - </a>
                </div>
            </td>
            <td class="cart_total">
                <p class="cart_total_price">$${total}</p>
            </td>
            <td class="cart_delete">
                <a class="cart_quantity_delete" style="cursor: pointer;"><i class="fa fa-times"></i></a>
            </td>
        </tr>
        `
    }).join("");
    updateTotalPrice();
    
if (tbody) {
    tbody.addEventListener("click", function(e) {
        let tr = e.target.closest("tr");
        if(!tr) return;
        let productId = tr.id;
        let qtyInput = tr.querySelector(".cart_quantity_input");
        let priceText = tr.querySelector(".cart_price p").innerText;
        let totalText = tr.querySelector(".cart_total_price");

        let priceNum = parseFloat(priceText.replace(/[^0-9.-]+/g,"")) || 0;
        let currentQty = parseInt(qtyInput.value);

        if (e.target.classList.contains("cart_quantity_up")) {
            currentQty++;
            qtyInput.value = currentQty;
            totalText.innerText = "$" + (priceNum * currentQty);
            updateQtyInLocalStorage(productId, currentQty);
            updateTotalPrice();
        }

        if (e.target.classList.contains("cart_quantity_down")) {
            if (currentQty <= 1) {
                alert("Số lượng nhỏ hơn hoặc bằng 1 không thể xoá");
                return;
            }
            currentQty--;
            qtyInput.value = currentQty;
            totalText.innerText = "$" + (priceNum * currentQty);
            updateQtyInLocalStorage(productId, currentQty);
            updateTotalPrice();
        }

        if (e.target.closest(".cart_quantity_delete")) {
            tr.remove();
            deleteProductFromLocalStorage(productId);
            updateTotalPrice();
        }
    });
}}

function updateQtyInLocalStorage(id, newQty) {
    let getLocal = localStorage.getItem("gioHang");
    if (getLocal) {
        let gioHang = JSON.parse(getLocal);
        let sanPham = gioHang.find(item => item.id === id);
        if (sanPham) {
            sanPham.qty = newQty;
        }
        localStorage.setItem("gioHang", JSON.stringify(gioHang));
    }
}

function deleteProductFromLocalStorage(id) {
    let getLocal = localStorage.getItem("gioHang");
    if (getLocal) {
        let gioHang = JSON.parse(getLocal);
        gioHang = gioHang.filter(item => item.id !== id); //Giữ lại những sản phẩm có id khác với id cần xoá
        localStorage.setItem("gioHang", JSON.stringify(gioHang));
    }
}