document.getElementById('login-form').addEventListener('submit', async function(event) {
	event.preventDefault();

	// Get form data
	const username = document.getElementById('username').value;
	const password = document.getElementById('password').value;

	// Get reCAPTCHA response
	const recaptchaResponse = grecaptcha.getResponse();

	if (!recaptchaResponse) {
		alert('Please complete the reCAPTCHA verification.');
		return;
	}

	// Prepare data to be sent to the server
	const data = {
		username: username,
		password: password,
		g_recaptcha_response: recaptchaResponse
	};

	// Send a POST request to the server
	const response = await fetch('/token', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify(data),
	});

	const result = await response.json();
	if (response.ok) {
		// Redirect to a dashboard or another page
		window.location.href = `/dashboard?username=${encodeURIComponent(username)}`;
	} else {
		// Display error message from the server
		alert(result.detail)
		//document.getElementById('responseMessage').innerText = `Login failed: ${result.detail || 'Unknown error'}`;
	}

	// Reset reCAPTCHA
	grecaptcha.reset();
});
