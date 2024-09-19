async function fetchShipments() {
	try {
		// Fetch shipments from backend
		const response = await fetch('http://127.0.0.1:8000/users/shipments/', {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json'
			},
			credentials: 'include'
		});

		if (response.ok) {
			const shipments = await response.json();
			populateShipmentsTable(shipments); // Populate the table with shipments
		}else if (response.status === 401) {
			const ErrorData = await response.json();
			alert(ErrorData.detail)
			window.location.href = '/login'
		} else if (response.status === 404){
			const error = await response.json();
			alert(error.detail);
		}
		else {
			alert("Failed to fetch shipments- Not found");
		}
	} catch (error) {
		console.error('Error fetching shipments:', error);
		alert('Error occurred while fetching shipments.');
	}
}

function populateShipmentsTable(shipments) {
	const tableBody = document.querySelector("#shipments-table tbody");
	tableBody.innerHTML = ""; // Clear any existing rows

	shipments.forEach((shipment) => {
		const row = document.createElement("tr");

		row.innerHTML = `
			<td>${shipment.shipment_no || ''}</td>
			<td>${shipment.container_no || ''}</td>
			<td>${shipment.route || ''}</td>
			<td>${shipment.goods_type || ''}</td>
			<td>${shipment.expected_delivery_date || ''}</td>
			<td>${shipment.po_no || ''}</td>
			<td>${shipment.device || ''}</td>
			<td>${shipment.delivery_no || ''}</td>
			<td>${shipment.ndc_no || ''}</td>
			<td>${shipment.batch_id || ''}</td>
			<td>${shipment.serial_no || ''}</td>
			<td>${shipment.shipment_description || ''}</td>
		`;

		tableBody.appendChild(row);
	});
}

// Fetch shipments on page load
document.addEventListener('DOMContentLoaded', fetchShipments);
