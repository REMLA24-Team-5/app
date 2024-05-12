# app
The application has a frontend and a service, which can, but do not have to, be implemented separately. The application uses the model service in a sensible use case.


# Instructions
All instructions assume that you are currently in the working app directory.
To run the app, simply build the container using:
```
docker build -t <tag> .
docker run -p 5000:5000 <tag>
```
You can now access the app through your browser.
