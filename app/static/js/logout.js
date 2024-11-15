async function userLogout() {
	try {
		const response = await fetch('/logout', {
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
