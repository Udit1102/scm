document.getElementById('forgotpassword-form').addEventListener('submit', async function(event) {
	event.preventDefault();

	const username = document.getElementById('username').value;

	const response = await fetch('/reset_password', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({"email": username})
	});

	const result = await response.json();
	if (response.ok) {
		alert(result.message);
	} else if (response.status === 404){
		alert(result.detail)
	}
	 else {
		alert("something went wrong, please try again");
	}
});
