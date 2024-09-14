# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any necessary packages
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for Snowflake credentials (these can be overridden at runtime)
ENV SNOWFLAKE_USER=user
ENV SNOWFLAKE_PASSWORD=password
ENV SNOWFLAKE_ACCOUNT=account
ENV SNOWFLAKE_WAREHOUSE=warehouse
ENV SNOWFLAKE_DATABASE=database
ENV SNOWFLAKE_SCHEMA=schema

# Set environment variable for Python path
ENV PYTHONPATH=/app

# List files for debugging
RUN ls -R /app

# Run the ETL function when the container launches
CMD ["python", "dags/dags.py"]
