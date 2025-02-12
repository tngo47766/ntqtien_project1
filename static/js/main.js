document.addEventListener("DOMContentLoaded", function() {
    console.log("JavaScript Loaded Successfully!");

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
            fetch(`/cart/add/${bookId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector("input[name='csrfmiddlewaretoken']").value,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ book_id: bookId, quantity: 1 })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
            })
            .catch(error => console.error("Error adding to cart:", error));
        }
    }

    // Attach functions to global window object for button clicks
    window.handleBuyNow = handleBuyNow;
    window.addToCart = addToCart;
});
