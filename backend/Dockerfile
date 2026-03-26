# Use the official Python image
FROM python:3.10

# Set the working directory
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY ./requirements.txt /code/requirements.txt

# Install requirements
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the app files
COPY . .

# Set permissions for SQLite DB (required for HF Spaces)
RUN chmod 777 /code
RUN touch /code/users.db
RUN chmod 777 /code/users.db

# Expose port (HF Spaces use 7860)
EXPOSE 7860

# Command to run the app
CMD ["gunicorn", "-b", "0.0.0.0:7860", "--timeout", "120", "--workers", "2", "app:app"]
