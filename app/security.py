from app.models import TokenData, NewPassword
from app.functions import get_user
from app.database import db
from datetime import datetime, timedelta, timezone
from typing import Union

from jwt import InvalidTokenError
import jwt

from fastapi import Depends, FastAPI, HTTPException, status, Request, Response
from urllib.parse import urljoin
from dotenv import load_dotenv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email_validator import validate_email, EmailNotValidError

#importing mail app password
app_password = os.getenv("app_password")

#fetching secret key info
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def send_mail_for_reset_password(base_url, receiver_mail: str, reset_token: str):
	try:
		#validating user email
		valid = validate_email(receiver_mail)
		receiver_mail = valid.email
		#server config
		smtp_server = "smtp.gmail.com"
		smtp_port = 587
		sender_mail = "ud.agrawal112@gmail.com"
		sender_password = app_password
		#mail content
		subject = "reset password request"
		reset_url = urljoin(base_url,f"/newpassword/page/?token={reset_token}")
		body = f"""
<html>
		<body>
			<p>Hi,</p>
			<p>Click the following link to reset your password: 
				<a href="{reset_url}">click here</a>
			</p>
			<p>Note: This link is valid only for the next 30 minutes.</p>
			<p>If you did not request this, please ignore the email.</p>
		</body>
</html>
"""
		#mail creation
		message = MIMEMultipart()
		message["From"] = sender_mail
		message["To"] = receiver_mail
		message["Subject"] = subject
		message.attach(MIMEText(body, "html"))
		#sending mail
		with smtplib.SMTP(smtp_server, smtp_port) as server:
			server.starttls()
			server.login(sender_mail, sender_password)
			server.send_message(message)
			#print(f"reset mail sent successfully to mail ending with {receiver_mail.split('@')[0]}")
			return {"message": "reset mail sent successfully"}
	except EmailNotValidError as e:
		return {"message": f"Invalid email address: {str(e)}"}
	except Exception as e:
		return {"message": f"Failed to send email: {str(e)}"}

#create access token

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.now(timezone.utc) + expires_delta
	else:
		expire = datetime.now(timezone.utc) + timedelta(minutes=15)
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt

async def get_current_user(request: Request):
	token = request.cookies.get("access_token")  # Extract the token from the cookie
	if not token:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Not authenticated, Please login",
		)
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Could not validate credentials",
	)
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		exp = payload.get("exp")
		if datetime.utcnow().timestamp() > exp:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Token expired, please login",
			)
		username: str = payload.get("sub")
		if username is None:
			raise credentials_exception
		token_data = TokenData(username=username)
	except InvalidTokenError:
		raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Invalid token, please login again",
			)
	user = await get_user(db, username=token_data.username)
	if user is None:
		raise credentials_exception
	return user

async def verify_reset_password_token(token: str):
	if not token:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Not authenticated",
		)
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Could not validate credentials",
	)
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		exp = payload.get("exp")
		if datetime.utcnow().timestamp() > exp:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Token expired",
			)
		username: str = payload.get("sub")
		if username is None:
			raise credentials_exception
		token_data = TokenData(username=username)
	except InvalidTokenError:
		raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Invalid token",
			)
	user = await get_user(db, username=token_data.username)
	if user is None:
		raise credentials_exception
	return user
