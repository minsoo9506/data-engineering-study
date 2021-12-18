FROM python:3

# set a directory for the app
# WORKDIR /app

# copy all the files to the container
COPY ./ ./

# install flask
RUN pip install -r requirements.txt

# tell the port number the container should expose
# EXPOSE 5000

# run the command
CMD ["python", "app.py"]