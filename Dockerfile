FROM ubuntu:latest
LABEL authors="ayanat"
FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir \
    streamlit \
    pandas \
    plotly \
    requests \
    python-dotenv \
    apscheduler

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]

ENTRYPOINT ["top", "-b"]