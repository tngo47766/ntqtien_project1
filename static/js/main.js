document.addEventListener("DOMContentLoaded", function() {
    console.log("✅ JavaScript Loaded Successfully!");

    // Function to handle Buy Now button
    function handleBuyNow(bookId) {
        let isLoggedIn = document.body.getAttribute("data-user-logged-in") === "true";

        if (!isLoggedIn) {
            document.getElementById("loginModal").classList.remove("hidden");
        } else {
            window.location.href = `/order/place/?book_id=${bookId}&quantity=1`;
        }
    }

    // Function to add book to cart via AJAX
    function addToCart(bookId) {
        let isLoggedIn = document.body.getAttribute("data-user-logged-in") === "true";

        if (!isLoggedIn) {
            document.getElementById("loginModal").classList.remove("hidden");
        } else {
            let csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']")?.value;
            if (!csrfToken) {
                alert("Lỗi bảo mật: Không tìm thấy CSRF Token.");
                return;
            }

            fetch(`/cart/add/${bookId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ quantity: 1 })
            })
            .then(response => response.json())
            .then(data => {
                if (data.cart_count !== undefined) {
                    document.getElementById("cart-count").textContent = data.cart_count;  // ✅ Fix: Update cart count dynamically
                }
                alert(data.message);
            })
            .catch(error => {
                console.error("Lỗi khi thêm vào giỏ hàng:", error);
                alert("Có lỗi xảy ra. Vui lòng thử lại.");
            });
        }
    }

    // Attach functions to global window object for inline `onclick` events
    window.handleBuyNow = handleBuyNow;
    window.addToCart = addToCart;  // ✅ Fix: Ensure addToCart is globally available
});
