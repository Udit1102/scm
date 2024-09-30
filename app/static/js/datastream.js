let intervalId;  // Declare a variable to store the interval ID

async function fetchData() {
    console.log("fetchData called at: " + new Date().toLocaleTimeString()); // Log each time the function is called
    try {
        const response = await fetch('http://127.0.0.1:8000/datastream', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: "include"
        });

        // Check if the response is successful
        if (response.ok) {
            const data = await response.json();  // Await and parse the JSON data
            // Update the DOM with the fetched data
            document.getElementById('data-stream').innerText = JSON.stringify(data);
        } else if (response.status === 401) {
            const errorData = await response.json();
            alert(errorData.detail);  // Alert unauthorized message
            clearInterval(intervalId);  // Stop further execution of fetchData
            console.log("Stopped fetchData execution due to 401 Unauthorized");
        } else {
            alert("Unable to fetch Data Stream, please try again");
        }
    } catch (error) {
        console.error("Something went wrong", error);
        alert("Something went wrong, please try again");
    }
}

async function stopData(){
    clearInterval(intervalId);  // Stop further execution of fetchData
    const response = await fetch('http://127.0.0.1:8000/stopdatastream', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: "include"
    });

    alert("Live data streaming stopped");            
}
// Call the API every 100seconds
intervalId = setInterval(fetchData, 100000);

// Call it once immediately when the page loads
fetchData();
