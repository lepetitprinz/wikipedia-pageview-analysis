ARG IMAGE_VARIANT=slim-buster
ARG OPENJDK_VERSION=8
ARG PYTHON_VERSION=3.8

FROM python:${PYTHON_VERSION}-${IMAGE_VARIANT} AS py3
FROM openjdk:${OPENJDK_VERSION}-${IMAGE_VARIANT}

COPY --from=py3 / /

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip --no-cache-dir install pyspark==3.2.0

COPY wrangling_wiki_pageview.py .

# Run the Python script
CMD ["python", "wrangling_wiki_pageview.py"]