document.getElementById('newpassword-form').addEventListener('submit', async function(event) {
	event.preventDefault();
	try {
		const newPassword = document.getElementById("new_password").value;
		const confirmPassword = document.getElementById("confirm_new_password").value;
		const token = document.getElementById("token").value;
		const passwordCriteria = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$/;

		if (!passwordCriteria.test(newPassword)) {
			alert("Password must be at least 8 characters, include an uppercase letter, a number, and a special character.");
			return;
		}

		if (newPassword !== confirmPassword) {
			alert("Passwords do not match!");
			return;
		}

		const payload = {
			token: token,
			new_password: newPassword
		};

		// Send the payload to the backend
		const response = await fetch('/create/newpassword/', {
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
});

