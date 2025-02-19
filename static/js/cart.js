document.addEventListener("DOMContentLoaded", function() {
    console.log("✅ Cart Script Loaded Successfully!");

    function updateCartTotal() {
        let totalPrice = 0;
        let totalItems = 0;

        document.querySelectorAll(".cart-item").forEach(item => {
            let price = parseInt(item.getAttribute("data-price")) || 0;
            let quantityInput = item.querySelector(".cart-quantity");
            let quantity = parseInt(quantityInput.value) || 1;

            let total = price * quantity;
            item.querySelector(".total-price").textContent = total.toLocaleString() + "₫";
            totalPrice += total;
            totalItems += quantity;
        });

        document.getElementById("total-price").textContent = totalPrice.toLocaleString() + "₫";
        document.getElementById("cart-count").textContent = totalItems; // ✅ Update cart count
    }

    document.querySelectorAll(".remove-item").forEach(button => {
        button.addEventListener("click", function() {
            let cartId = this.getAttribute("data-id");
            let cartRow = this.closest("tr");  // 🔥 Lấy hàng chứa sản phẩm cần xóa
    
            fetch(`/cart/remove/${cartId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("input[name='csrfmiddlewaretoken']").value
                }
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                if (data.success) {
                    cartRow.remove();  // ✅ Xóa sản phẩm khỏi giao diện
                    window.location.reload();
                    updateCartTotal();  // ✅ Cập nhật tổng tiền
                }
            })
            .catch(error => console.error("❌ Lỗi khi xóa sản phẩm:", error));
        });
    });
    

    // ✅ Handle quantity change in cart
    document.querySelectorAll(".cart-quantity").forEach(input => {
        input.addEventListener("change", function() {
            let cartId = this.getAttribute("data-id");
            let newQuantity = this.value;

            if (newQuantity < 1) {
                alert("❌ Số lượng không hợp lệ!");
                return;
            }

            fetch(`/cart/update/${cartId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("input[name='csrfmiddlewaretoken']").value,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ quantity: newQuantity })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                if (data.success) {
                    updateCartTotal();
                }
            })
            .catch(error => console.error("❌ Lỗi khi cập nhật số lượng:", error));
        });
    });

    document.getElementById("checkout-btn").addEventListener("click", function() {
        let cartItems = [];
    
        document.querySelectorAll(".cart-item").forEach(item => {
            let bookId = item.getAttribute("data-book-id");  // ✅ Get book ID correctly
            let quantity = item.querySelector(".cart-quantity").value;
    
            cartItems.push({
                book_id: bookId,  // ✅ Send correct book_id
                quantity: quantity
            });
        });
    
        if (cartItems.length === 0) {
            alert("❌ Giỏ hàng của bạn đang trống!");
            return;
        }
    
        fetch("/order/place/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector("input[name='csrfmiddlewaretoken']").value
            },
            body: JSON.stringify({ items: cartItems })  // ✅ Send correct data
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(`✅ Đặt hàng thành công! Tổng tiền: ${data.total_price.toLocaleString()}₫`);
                
            } else {
                alert(`❌ Lỗi: ${data.message}`);
            }
        })
        .catch(error => console.error("❌ Lỗi khi thanh toán:", error));
    });
    

    updateCartTotal(); // ✅ Update total price on load
});
