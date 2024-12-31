FROM python:3.9-slim

WORKDIR /app

# העתקת קבצי requirements
COPY requirements.txt .

# התקנת תלויות
RUN pip install --no-cache-dir -r requirements.txt

# העתקת קוד האפליקציה
COPY app.py .

# חשיפת הפורט
EXPOSE 5000

# הרצת האפליקציה
CMD ["python", "app.py"]
