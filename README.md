A web app to view logs of a remote file on a server in real time.

## Installation guidelines
```
virtualenv venv
```
```
source venv/bin/activate
```
```
pip3 install -r requirements.txt
```
### To run
```
python3 application.py
```
### To use
Hit http://localhost:5000 in the browser
### To append data in the log file on the server use
http://localhost:5000/append/<text> endpoint
