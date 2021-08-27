# Full Stack app with Upload/Download API

This app uses python for back-end and a sqlite3 database. Front-end is written in HTML/CSS.


# Usage

```
git clone https://github.com/rajatagarwal457/TechM-Internship
cd TechM-Internship
python app.py
```
This will setup the application on localhost and will run with SSL context. Since this is a self signed certificate the user will need to accept the security risk in the browser.

## Endpoints
I have not made a landing page for this app as it was just for API testing purposes.

### /login
Here an already registered user can login with their credentials.

### /register
A new user can register here.

### /upload
This is the page the user is redirected to after login. You can upload an excel file which is written to the database. The entity and period has to be consistent throughout the excel sheet.
Note: Please use .xls files and not .xlsx as this is not supported yet.

### /download
Here the user specifies an entity and all records pertaining to the queried entity are written in a excel file and the file is downloaded.
