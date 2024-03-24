console.log("Hello ESP!");

const currentUrl = window.location.href;
console.log(currentUrl);
const pl = document.getElementById('spinner')
let isWaiting = true;
let stationList = {};

async function checkStations(){
    const res = await fetch(currentUrl+"api/wifi/scan");
    const data = await res.json();
    stationList = await data;
    return await data;
}

function displayWifiStations(data){
    console.log("Add some cool code here");
    pl.style.display = "none"
}

for(let i=0; i<3; i++){
    setTimeout(async () => {
        stationList =  await checkStations();
        console.log(stationList);
    }, 5000);
}




