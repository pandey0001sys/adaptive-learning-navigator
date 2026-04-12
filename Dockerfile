FROM python:3.10

WORKDIR /app

# requirements पहले copy करो (cache fast होगा)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# बाकी project files copy करो
COPY . .

# port expose
EXPOSE 7860

# app run करो
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
