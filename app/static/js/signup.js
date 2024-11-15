document.getElementById('signup-form').addEventListener('submit', async function(event) {
	event.preventDefault();

	const username = document.getElementById('username').value;
	const firstName = document.getElementById('first_name').value;
	const lastName = document.getElementById('last_name').value;
	const password = document.getElementById('password').value;
	const confirmPassword = document.getElementById('confirm_password').value;
	const passwordCriteria = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$/;
	if (!passwordCriteria.test(password)) {
		alert("Password must be at least 8 characters, include an uppercase letter, a number, and a special character.");
		return;
	}
	if (password !== confirmPassword) {
		alert("Passwords do not match!");
		return;
	}

	const response = await fetch('/register', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({
			username: username,
			first_name: firstName,
			last_name: lastName,
			hashed_password: password
		}),
	});

	const result = await response.json();
	if (response.ok) {
		alert('Sign-up successful!');
		window.location.href = '/login';
	} else {
		if (Array.isArray(result.detail)) {
			const messages = result.detail.map(error => error.msg || JSON.stringify(error));
			alert('Sign-up failed: ' + messages.join(', '));
		} else {
			alert('Sign-up failed: ' + (result.detail || JSON.stringify(result)));
		}
	}
});

