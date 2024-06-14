FROM python:3.12.4-bookworm

WORKDIR /app
RUN mkdir -p /logs && touch /logs/memesearch.log

COPY ./requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
ENV PYTHONPATH=/app
RUN python trigger_file_download.py

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]
