// Select all elements with the class "update_cart"
var updateElements = document.querySelectorAll('.update_cart');

// Add event listeners to each selected element
updateElements.forEach(element => {
    element.addEventListener('click', function(event) {
        // Prevent default action for <a> tags to avoid page navigation
        if (element.tagName === 'A') {
            event.preventDefault();
        }

        // Get productId and action from data attributes
        var productId = this.dataset.product;
        var action = this.dataset.action;

        // Log the productId and action
        console.log('Product ID:', productId, 'Action:', action);

        // Check user authentication and proceed accordingly
        if (user === 'AnonymousUser') {
            console.log('User is not authenticated');
            // You can add additional logic for guest users if needed
        } else {
            updateUserOrder(productId, action);
        }
    });
});

// Function to send the update to the server
function updateUserOrder(productId, action) {
    console.log('User is authenticated, sending data...');

    var url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken, // Ensure csrftoken is defined
        },
        body: JSON.stringify({ 'productId': productId, 'action': action }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Data received:', data);
        location.reload(); // Reload the page to reflect cart updates
    });
}
document.addEventListener("DOMContentLoaded", function () {
    let cartButtons = document.querySelectorAll(".update_cart");
  
    cartButtons.forEach((button) => {
      button.addEventListener("click", function () {
        let userAuthenticated = "{{ user.is_authenticated }}"; // Django Template Variable
        if (userAuthenticated === "False") {
          window.location.href = "{% url 'login' %}"; // Redirect to login
        } else {
          let productId = this.dataset.product;
          let action = this.dataset.action;
          updateCart(productId, action); // Call your existing cart update function
        }
      });
    });
  });
  