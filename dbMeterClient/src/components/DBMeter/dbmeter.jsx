import { useState } from "react";

function Dbmeter() {
    const title = "Front";
    const [decibel, setDecibel] = useState(0);

    let number = 0;

    const intervalId = setInterval(() => {
    number += 5;
    console.log(number); // You can replace this with your desired logic or action.
    setDecibel(number);

    if (number >= 95) {
        clearInterval(intervalId); // Stop the interval when the number reaches 95.
    }
    }, getRandomDelay());

    function getRandomDelay() {
    // Generate a random delay between 3 to 5 seconds (in milliseconds).
    return Math.floor(Math.random() * (5000 - 3000 + 1) + 3000);
    }


    const getDecibelLevel = () => {
        setDecibel(5);
    }

    getDecibelLevel()
    
    return (
        <div className='meter'>
            <h1 className="meter-name">
                { title }
            </h1>
            <div className="meter-output">
                <p>
                    { decibel }
                </p>
            </div>
        </div>
    )
}

export default Dbmeter

