FROM python:3.11-slim
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /workspace
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000 8888
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--no-browser"]
