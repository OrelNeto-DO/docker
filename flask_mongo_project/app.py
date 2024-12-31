from flask import Flask, render_template
from sqlalchemy import create_engine, text
import os
import random
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# קריאת משתני הסביבה
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "mysql")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "mydatabase")

# כתובת חיבור ל-MySQL
DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL)

@app.route("/")
def index():
    try:
        with engine.connect() as connection:
            # שליפת כל התמונות מהמסד
            result = connection.execute(text("SELECT id, image_url, counter FROM images"))
            images = [{"id": row["id"], "url": row["image_url"], "counter": row["counter"]} for row in result]

            # בחירת תמונה אקראית
            selected_image = random.choice(images)
            selected_image_id = selected_image["id"]
            selected_image_url = selected_image["url"]
            selected_image_counter = selected_image["counter"]

            # עדכון הקאונטר במסד הנתונים
            connection.execute(
                text("UPDATE images SET counter = counter + 1 WHERE id = :id"),
                {"id": selected_image_id}
            )

        # שליחת ה-URL והקאונטר לתבנית
        return render_template("index.html", url=selected_image_url, counter=selected_image_counter)
    except Exception as e:
        print(f"Error: {e}")
        return "Error connecting to the database."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
