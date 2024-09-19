document.getElementById("shipment-form").addEventListener("submit", async function(event) {
	event.preventDefault(); // Prevent the default form submission

	// Get form data
	const shipmentData = {
		shipment_no: document.getElementById('shipment_no').value,
		container_no: document.getElementById('container_no').value,
		route: document.getElementById('route').value,
		goods_type: document.getElementById('goods_type').value,
		expected_delivery_date: document.getElementById('expected_delivery_date').value,
		po_no: document.getElementById('po_no').value,
		device: document.getElementById('device').value,
		delivery_no: document.getElementById('delivery_no').value,
		ndc_no: document.getElementById('ndc_no').value,
		batch_id: document.getElementById('batch_id').value,
		serial_no: document.getElementById('serial_no').value,
		shipment_description: document.getElementById('shipment_description').value
	};

	// Log the request body before sending
	console.log("Request Body:", shipmentData);

	// Make the request and await the response
	const response = await fetch('http://127.0.0.1:8000/users/create/shipment/', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		credentials: 'include',
		body: JSON.stringify(shipmentData)
	});

	// Check if the response was successful
	if (response.ok) {
		const result = await response.json(); // Await the JSON data
		alert(result.message);
	} else if (response.status === 401) {
		const ErrorData = await response.json();
		alert(ErrorData.detail);
		window.location.href = '/login';  
	} else {
		const errorData = await response.json(); // Log error details from backend
		console.error('Failed to create shipment:', errorData);
		alert('Failed to create shipment. Please try again.');
	}
});
