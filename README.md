# APJournaling 
 
Secure Application Programming Project  
Author: Alexandra Phelan (x20245823)

## Overview

APJournaling is a simple journaling web application built using Python Flask and SQLite3.  

The project includes two versions

Insecure Version: intentionally vulnerable  
Secure Version: mitigations applied following OWASP guidelines  

The purpose of the project is to show the understanding of:

- SQL Injection  
- Reflected XSS  
- Stored XSS  
- DOM-Based XSS  
- Sensitive Data Exposure  

The secure branch also implements:

- Password hashing  
- Parameterised queries  
- CSRF protection  
- Secure session management  
- Security headers  
- Logging and monitoring  

---

## Features Insecure Version

- SQL Injection vulnerability  
- Stored XSS in journal entries  
- Reflected XSS in search  
- DOM-Based XSS  
- Plaintext password storage  
- No security headers  
- No CSRF protection  

---

## Features Secure Version

- Password hashing using Werkzeug  
- Parameterised SQL queries  
- Jinja2 autoescaping for XSS protection  
- Replaced innerHTM with innerText (prevents DOM XSS)  
- CSRF tokens (forms protected)  
- Secure session cookies  
- Logging of login attempts and actions  
- Security headers:
  - X-Content-Type-Options
  - X-Frame-Options
  - X-XSS-Protection  
- Removed plaintext passwords  
- Improved architecture and separation of services  


## Branches

### insecure
Contains the vulnerable application used to demonstrate attacks such as SQL Injection and XSS.

### secure
Contains the fully patched version using OWASP recommendations.

In VS Code (bottom-left corner), click the branch name and select:

- secure
- insecure

git checkout insecure
git checkout secure


## Installation & Running the App

1. Install dependencies:

pip install -r requirements.txt


2. Run the Flask application:

python app.py


3. Open browser:

http://127.0.0.1:5000


The database is automatically created on first run.



## Running Selenium Tests

To run the automated login test:

python test.py


This test:

- Opens Chrome  
- Enters credentials  
- Logs in  
- Confirms the dashboard loads  

---

## Tools Used

- Python Flask  
- SQLite3  
- Selenium WebDriver  
- WebDriver Manager  
- OWASP ZAP (DAST testing)  
- Chrome Lighthouse (NFR testing)  


## Notes

This project is for educational purposes to demonstrate insecure coding patterns and how to fix them using secure development practices.

