document.addEventListener("DOMContentLoaded", function() {
    let selectedBookId = null;

    function openBuyNowModal(bookId, bookName) {
        selectedBookId = bookId;
        document.getElementById("selectedBookName").textContent = bookName;
        document.getElementById("buyNowModal").classList.remove("hidden");
    }

    function closeBuyNowModal() {
        document.getElementById("buyNowModal").classList.add("hidden");
    }

    function confirmBuyNow() {
        let quantity = document.getElementById("quantity").value;
        if (quantity < 1) {
            alert("Số lượng phải lớn hơn 0!");
            return;
        }

        fetch("/order/place/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector("input[name='csrfmiddlewaretoken']").value
            },
            body: JSON.stringify({
                items: [{ book_id: selectedBookId, quantity: quantity }]
            })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            if (data.success) {
                window.location.href = "/customer/main/";  // ✅ Chuyển đến trang chính sau khi mua hàng
            }
        })
        .catch(error => console.error("Lỗi khi đặt hàng:", error));
    }

    // Expose functions globally for button events
    window.openBuyNowModal = openBuyNowModal;
    window.closeBuyNowModal = closeBuyNowModal;
    window.confirmBuyNow = confirmBuyNow;
});
