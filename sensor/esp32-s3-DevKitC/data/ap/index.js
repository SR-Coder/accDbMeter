console.log("Hello ESP!");

const currentUrl = window.location.href;
console.log(currentUrl);
const pl = document.getElementById('spinner')
const networkList = document.getElementById('networkList');
let isWaiting = true;
let stationList = {};

async function checkStations(){
    let data = {status: 'scanning'};
    while(!data || data.status === 'scanning') {
        const res = await fetch(currentUrl+"api/wifi/scan");
        data = await res.json();
        if(!data || data.status === 'scanning') {
            await new Promise(resolve => setTimeout(resolve, 1000)); // wait for 1 seconds and try again
        }
    }
    stationList = data;
    return data;
}

function displayWifiStations(data){
    // Clear the networkList first
    networkList.innerHTML = '';

    // Create a form
    const form = document.createElement('form');
    form.action = '/submit';
    form.method = 'POST';
    form.style.display = 'flex';
    form.style.flexDirection = 'column';
    // form.addEventListener('submit', (event) => {
    //     event.preventDefault();
    
    //     // Create a FormData object from the form
    //     const formData = new FormData(form);
    
    //     // Send a POST request to the /submit route
    //     fetch(form.action, {
    //         method: form.method,
    //         body: formData
    //     }).then(response => {
    //         if (!response.ok) {
    //             throw new Error('Network response was not ok');
    //         }
    //         return response.text();
    //     }).then(data => {
    //         console.log('Form submitted successfully:', data);
    //     }).catch(error => {
    //         console.error('Error:', error);
    //     });
    // });

    // Create a radio button for each station
    data.forEach((station, index) => {
        if (!station.ssid) return; // Skip if name is blank
        const div = document.createElement('div');
        div.style.display = 'flex';
        const label = document.createElement('label');
        label.textContent = station.ssid; // Replace with actual station name property

        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.name = 'ssid';
        radio.value = station.ssid;
        radio.id = index;

        div.appendChild(radio);
        div.appendChild(label);
        form.appendChild(div);
    });

    // Create a password input field
    const passwordLabel = document.createElement('label');
    passwordLabel.textContent = 'Password:';
    const passwordInput = document.createElement('input');
    passwordInput.type = 'password';
    passwordInput.name = 'password';

    passwordLabel.appendChild(passwordInput);
    form.appendChild(passwordLabel);

    // Create a submit button
    const submitButton = document.createElement('input');
    submitButton.type = 'submit';
    

    form.appendChild(submitButton);

    // Add the form to the networkList
    networkList.appendChild(form);

    // Hide the spinner
    pl.style.display = "none";
}

checkStations().then(data => {
    displayWifiStations(data);
});