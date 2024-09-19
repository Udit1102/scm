async function userLogout() {
	try {
		const response = await fetch('http://127.0.0.1:8000/logout', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			credentials: 'include'
		});
		if (response.ok) {
			alert('Logout successful');
			window.location.href = '/login'; // Redirect to login page 
			return;
		} else {
			alert("something went wrong");
		}
	}

	catch (error) {
		console.error('Error fetching the shipments:', error);
	}
}
async function fetchShipment() {
	try {
		/*const token = localStorage.getItem('access_token');
		if (!token) {
			alert('You are not logged in, please login again.');
			return;
		}*/

		const response = await fetch('http://127.0.0.1:8000/users/shipments/', {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json'
			},
			credentials: 'include'
		});
		if (!response.ok) {
			alert('Unable to fetch shipments');
			return;
		}
	}

	catch (error) {
		console.error('Error fetching the shipments:', error);
	}
}
