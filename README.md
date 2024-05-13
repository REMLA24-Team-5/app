# app
This repository contains both the app frontend and app service for the URL phishing detection application. The user can enter a URL, after which a trained model is queried, which returns whether the URL is phishing or not. 

# Instructions
All instructions assume that you are currently in the working app directory.
To run the app, simply build the container using:
```
docker build -t <tag> .
docker run -p 5000:5000 <tag>
```
You can now access the app through your browser.

[UPDATE WITH SENSIBLE USE CASE].
[UPDATE ABOUT REPO SECTION (TOP RIGHT)]