// Get all the elements with the specified classes
let rateElements = document.querySelectorAll('.rate');
let subtotalElements = document.querySelectorAll('.subtotal1');
let valueInputs = document.querySelectorAll('.value');
let minusButtons = document.querySelectorAll('.minus');
let plusButtons = document.querySelectorAll('.plus');

// Add event listeners to each button
for (let i = 0; i < minusButtons.length; i++) {
    minusButtons[i].addEventListener('click', () => decreaser(i));
}

for (let i = 0; i < plusButtons.length; i++) {
    plusButtons[i].addEventListener('click', () => increaser(i));
}

// Function to decrease value and update subtotal
function decreaser(index) {
    let price = parseFloat(rateElements[index].innerText.replace('₹', ''));
    let total = parseFloat(subtotalElements[index].innerText.replace('₹', ''));
    let inputValue = parseInt(valueInputs[index].value);

    if (inputValue > 1) {
        inputValue--;
        valueInputs[index].value = inputValue;
        total -= price;
        subtotalElements[index].innerText = '₹' + total.toFixed(2);
    }
}

// Function to increase value and update subtotal
function increaser(index) {
    let price = parseFloat(rateElements[index].innerText.replace('₹', ''));
    let total = parseFloat(subtotalElements[index].innerText.replace('₹', ''));
    let inputValue = parseInt(valueInputs[index].value);

    inputValue++;
    valueInputs[index].value = inputValue;
    total += price;
    subtotalElements[index].innerText = '₹' + total.toFixed(2);
}
