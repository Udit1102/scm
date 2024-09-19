/*async function handleSubmit(event) {
	event.preventDefault(); // Prevents the default form submission
	try {
		const newPassword = document.getElementById("new_password").value;
		const confirmPassword = document.getElementById("confirm_new_password").value;
		const token = document.getElementById("token").value;

		if (newPassword !== confirmPassword) {
			alert("Passwords do not match!");
			return;
		}

		const payload = {
			token: token,
			new_password: newPassword
		};

		// Send the payload to the backend
		const response = await fetch('http://127.0.0.1:8000/create/newpassword/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(payload)
		});

		if (response.ok) {
			const data = await response.json();
			alert(data.message);
			window.location.href = '/login'; // Redirect to login page
		} else if (response.status === 401) {
			const errorData = await response.json();
			alert(errorData.detail);
		}
	} catch (error) {
		console.error('Error updating password:', error);
		alert('Error occurred while updating password.');
	}
}
*/

async function handleSubmit(event) {
	event.preventDefault(); // Prevents the default form submission

	try {
		const newPassword = document.getElementById("new_password").value;
		const confirmPassword = document.getElementById("confirm_new_password").value;
		const token = document.getElementById("token").value;

		if (newPassword !== confirmPassword) {
			alert("Passwords do not match!");
			return;
		}

		const payload = {
			token: token,
			new_password: newPassword
		};

		// Send the payload to the backend
		const response = await fetch('http://127.0.0.1:8000/create/newpassword/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(payload)
		});

		if (response.ok) {
			const data = await response.json();
			alert(data.message);
			window.location.href = '/login'; // Redirect to login page
		} else {
			// Check if the response has a JSON body
			let errorMessage = 'Something went wrong';
			try {
				const errorData = await response.json();
				errorMessage = errorData.detail || 'No detailed error provided';
			} catch (jsonError) {
				console.error('Error parsing JSON:', jsonError);
			}
			alert(`Error: ${errorMessage}`);
		}
	} catch (error) {
		console.error('Error updating password:', error);
		alert('Error occurred while updating password.');
	}
}
