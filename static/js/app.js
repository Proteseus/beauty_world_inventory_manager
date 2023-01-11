// Get the form, the 'Sale' button, and the overlay card
const form = document.querySelector('#item-sale-form');
const saleButton = document.getElementById('sale-button');
const overlayCard = document.getElementById('overlay-card');
const cancelButton = document.getElementById('cancel-button');

// Add an event listener to the 'Sale' button
saleButton.addEventListener('click', function(event) {
// Prevent the form from being submitted
    event.preventDefault();

    // Get the values from the form
    const name = document.getElementById('name-selector').value;
    const quantity = document.getElementById('quantity-input').value;
    const customer = document.getElementById('customer-input').value;

    // Update the text of the overlay card elements
    document.getElementById('name-display').textContent = name;
    document.getElementById('quantity-display').textContent = quantity;
    document.getElementById('customer-display').textContent = customer;

    // Show the overlay card
    overlayCard.style.display = 'flex';
});

cancelButton.addEventListener('click', function () {
    overlayCard.style.display = 'none'
});

// Add an event listener to the 'Confirm' button
document.getElementById('confirm-button').addEventListener('click', function() {
    // Submit the form
    form.submit();
});