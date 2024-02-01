// app.js

function searchZipCode() {
    const searchInput = document.getElementById('searchInput');
    const resultDiv = document.getElementById('result');

    const searchTerm = searchInput.value.trim().toLowerCase();

    // Use an AJAX request to the Flask API endpoint
    const xhr = new XMLHttpRequest();
    xhr.open('GET', `http://127.0.0.1:5000/search/${searchTerm}`, true);

    xhr.onload = function () {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            displayResult(response);
        } else {
            displayResult({ error: 'Error fetching data' });
        }
    };

    xhr.onerror = function () {
        displayResult({ error: 'Request failed' });
    };

    xhr.send();
}

function displayResult(data) {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '';

    if (data.error) {
        resultDiv.innerHTML = `<p>${data.error}</p>`;
    } else {
        for (const [zipCode, city] of Object.entries(data)) {
            resultDiv.innerHTML += `<p>${city}: ${zipCode}</p>`;
        }
    }
}

function changeEntriesPerPage() {
const selectedValue = document.getElementById("entriesPerPage").value;
// Implement logic to update the display based on selected entries per page
// You may use AJAX to fetch and display the appropriate subset of results
console.log("Selected entries per page:", selectedValue);
}