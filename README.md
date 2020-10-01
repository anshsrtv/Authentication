# Authentication
## Setup and run
1. Clone this repository `git clone https://github.com/anshsrtv/Authentication.git`
1. Enter the main directory `cd Authentication/auth/`
1. Create a virtual environment with Python3: `python3 -m venv env `. If you dont have `python3` yet then you can install it with:
    1. linux(ubuntu/debian) - `sudo apt install python3`
    1. windows - Download installer from https://www.python.org/downloads/release/python-370/.
1. Activate the virutal environment: `source env/bin/activate`
1. Install all the dependencies in `requirements.txt` file: `pip install -r requirements.txt`
1. Set some global variables:
    1. `export SECRET_KEY= 'YOUR_SECRET_KEY'`
    1. `export EMAIL_ADDRESS = 'YOUR_EMAIL_ADDRESS'`
    1. `export EMAIL_PASSWORD = 'YOUR_EMAIL_PASSWORD'`
    
    **NOTE: Make sure the email address you use has `Less Secure App Access` and no `Two-Factor Authentication` to allow emails to be sent by the application.**
1. Make Migrations if needed `python manage.py makemigrations`
1. Migrate the migrations: `python manage.py migrate`
1. Run the app: `python manage.py runserver`
1. Navigate to http://localhost:8000 in your browser
1. When you are done using the app, deactivate the virtual environment: `deactivate`

  
