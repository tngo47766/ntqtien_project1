document.addEventListener("DOMContentLoaded", function() {
    let selectedBookId = null;

    // ✅ Ensure function is globally accessible
    window.openBuyNowModal = function(bookId, bookName) {
        selectedBookId = bookId;
        document.getElementById("selectedBookName").textContent = bookName;
        document.getElementById("buyNowModal").classList.remove("hidden");
    };

    window.closeBuyNowModal = function() {
        document.getElementById("buyNowModal").classList.add("hidden");
    };

    window.confirmBuyNow = function() {
        let quantity = document.getElementById("quantity").value;
        if (quantity < 1) {
            alert("Số lượng phải lớn hơn 0!");
            return;
        }

        // ✅ Fetch CSRF token from the meta tag for security
        let csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']")?.value;
        if (!csrfToken) {
            alert("Lỗi bảo mật: Không tìm thấy CSRF Token.");
            return;
        }

        fetch("/order/place/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                items: [{ book_id: selectedBookId, quantity: quantity }]
            })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            if (data.success) {
                window.location.href = "/customer/main/";  // ✅ Redirect after purchase
            }
        })
        .catch(error => {
            console.error("Lỗi khi đặt hàng:", error);
            alert("Có lỗi xảy ra khi đặt hàng. Vui lòng thử lại.");
        });
    };
});
