async function fetchProfile() {
	try {
		const response = await fetch('/users/me/', {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json'
			},
			credentials: 'include'  
		});

		if (response.ok) {
			const userData = await response.json();
			alert(`User Profile:\nUsername: ${userData.username}\nFirst Name: ${userData.first_name}\nLast Name: ${userData.last_name}`);
		}
		else if (response.status === 401){
			const errorData = await response.json();
			alert(errorData.detail);
			window.location.href = '/login';  
		}
		else {
			alert('Failed to fetch profile. Please try again.');
		}
	} catch (error) {
		console.error('Error fetching profile:', error);
		alert('Error occurred while fetching profile.');
	}
}