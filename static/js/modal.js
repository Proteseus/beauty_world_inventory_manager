// Config
const isOpenClass = 'modal-is-open';
const openingClass = 'modal-is-opening';
const closingClass = 'modal-is-closing';
const animationDuration = 400; // ms
let visibleModal = null;
const modal = document.getElementById('modal-example');

// Get the form, the 'Sale' button, and the overlay card
const form = document.querySelector('#item-sale-form');
const saleButton = document.getElementById('sale-button');
const overlayCard = document.getElementById('overlay-card');
const cancelButton = document.getElementById('cancel-button');

// Open modal
const openModal = modal => {
  document.documentElement.classList.add(isOpenClass, openingClass);
  setTimeout(() => {
    visibleModal = modal;
    document.documentElement.classList.remove(openingClass);
  }, animationDuration);
  modal.setAttribute('open', true);
}

// Close modal
const closeModal = modal => {
  visibleModal = null;
  document.documentElement.classList.add(closingClass);
  setTimeout(() => {
    document.documentElement.classList.remove(closingClass, isOpenClass);
    document.documentElement.style.removeProperty('--scrollbar-width');
    modal.removeAttribute('open');
  }, animationDuration);
}
// Add an event listener to the 'Sale' button
saleButton.addEventListener('click', function(event) {
// Prevent the form from being submitted
    event.preventDefault();
    openModal(modal)

    // Get the values from the form
    const name = document.getElementById('name-selector').value;
    const quantity = document.getElementById('quantity-input').value;
    const customer = document.getElementById('customer-input').value;

    // Update the text of the overlay card elements
    document.getElementById('name-display').textContent = name;
    document.getElementById('quantity-display').textContent = quantity;
    document.getElementById('customer-display').textContent = customer;
});

cancelButton.addEventListener('click', function () {
  closeModal(modal)
});

// Add an event listener to the 'Confirm' button
document.getElementById('confirm-button').addEventListener('click', function() {
    // Submit the form
    form.submit();
});
