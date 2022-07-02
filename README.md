# Institute-Management-System-
Download the zip file.

First open vs code, Start MongodB

To run the project, open PowerShell as admin mode
Go to project location using cd
Then give below commands:
	set FLASK_APP=main.py
	$env:FLASK_APP = "main.py"
	$env:FLASK_DEBUG = 1
	Python -m flask run 
	or
	For custom port use : python -m flask run –port 3423
