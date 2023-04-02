# Use an official Python runtime as a parent image
FROM python:3.9-slim

# RUN echo "hello world"

# # Set the working directory to /app
WORKDIR /smartgen

# RUN pwd
# # Copy the current directory contents into the container at /app
COPY . ./smartgen

# # # Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r ./smartgen/requirements.txt

# # # Make port 80 available to the world outside this container
EXPOSE 8081
# # # Define environment variable
ENV NAME World

RUN mkdir water_cons
RUN mkdir gen_dem

# RUN touch water_cons/command.txt

# RUN touch water_cons/results.txt

# # # Run app.py when the container launches
CMD ["python", "./smartgen/main.py"]