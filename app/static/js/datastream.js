async function fetchData() {
	try {
		const response = await fetch('/datastream', {
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
			//document.getElementById('data-stream').innerText = JSON.stringify(data);
			populateDeviceDataTable(data);
		} else if (response.status === 401) {
			const errorData = await response.json();
			alert(errorData.detail);  // Alert unauthorized message
			console.log("Stopped fetchData execution due to 401 Unauthorized");
		} else {
			alert("Unable to fetch Data Stream, please try again");
		}
	} catch (error) {
		console.error("Something went wrong", error);
		alert("Something went wrong, please try again");
	}
}

// Function to populate the table with data
function populateDeviceDataTable(data) {
	const tableBody = document.querySelector("#device-data-table tbody");
	tableBody.innerHTML = ""; // Clear any existing rows

	data.forEach(item => {
		const row = document.createElement("tr");

		row.innerHTML = `
			<td>${item.Time}</td>
			<td>${item.Battery_Level}</td>
			<td>${item.Device_Id}</td>
			<td>${item.First_Sensor_temperature}</td>
			<td>${item.Route_From}</td>
			<td>${item.Route_To}</td>
		`;

		tableBody.appendChild(row);
	});
}

// Call the function to fetch data on page load
document.addEventListener('DOMContentLoaded', fetchData);
