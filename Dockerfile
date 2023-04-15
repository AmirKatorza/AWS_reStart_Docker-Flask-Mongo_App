# Step 1 select default OS image
FROM alpine

# Step 2 tell what you want to do
RUN apk add --no-cache python3-dev && apk add py3-pip
RUN pip3 install --upgrade pip

# Step 3 Configure a software
# Defining working directory
WORKDIR /app

# Step 4 Install Dependencies
COPY /requirements.txt /app
RUN pip3 install -r requirements.txt

# Copy everything which is present in my docker directory to working (/app)
COPY ["mongo_tmdb_logic.py", "MongoDBAPI.py", "TMDB_Downloader.py", "/app/"]
RUN mkdir -p /app/posters_images/

# Exposing an internal port
EXPOSE 5001

# Step 4 set default commands
# These are permanent commands i.e even if user will provide some commands those will be considered as argunemts of this command
ENTRYPOINT [ "python3" ]

# These commands will be replaced if user provides any command by himself
CMD ["app.py"]