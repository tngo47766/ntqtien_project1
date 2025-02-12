document.addEventListener("DOMContentLoaded", function() {
    function updateCartTotal() {
        let totalPrice = 0;
        
        document.querySelectorAll(".cart-item").forEach(item => {
            let price = parseInt(item.getAttribute("data-price"));
            let quantity = parseInt(item.getAttribute("data-quantity"));
            let total = price * quantity;

            item.querySelector(".total-price").textContent = total.toLocaleString() + "₫";
            totalPrice += total;
        });

        document.getElementById("total-price").textContent = totalPrice.toLocaleString() + "₫";
    }

    function placeOrder() {
        let cartItems = [];

        document.querySelectorAll(".cart-item").forEach(item => {
            cartItems.push({
                book_id: item.getAttribute("data-id"),
                quantity: item.getAttribute("data-quantity")
            });
        });

        if (cartItems.length === 0) {
            alert("Giỏ hàng của bạn đang trống!");
            return;
        }

        fetch("/order/place/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector("input[name='csrfmiddlewaretoken']").value
            },
            body: JSON.stringify({ items: cartItems })
        })
        .then(response => response.json())
        .then(data => {
            alert(`Đặt hàng thành công! Tổng tiền: ${data.total_price.toLocaleString()}₫`);
            window.location.href = "/customer/main/";  
        })
        .catch(error => console.error("Lỗi khi đặt hàng:", error));
    }

    document.getElementById("checkout-btn").addEventListener("click", placeOrder);
    updateCartTotal();
});
