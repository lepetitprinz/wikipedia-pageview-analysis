FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

COPY ingest_wiki_pageview.py .

# Run the Python script
CMD ["python", "ingest_wiki_pageview.py"]