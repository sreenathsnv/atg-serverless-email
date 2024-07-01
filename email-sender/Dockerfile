FROM public.ecr.aws/lambda/python:3.9

# Copy application files
COPY app.py ./
COPY wsgi_handler.py ./
COPY requirements.txt ./

# Install dependencies
RUN pip install -r requirements.txt

# Set environment variable for Flask
ENV FLASK_APP=app.py

# Command to run the Lambda function handler
CMD ["wsgi_handler.handler"]
