from flask import Flask, request, jsonify, render_template
import psycopg2
import os

app = Flask(__name__)

# Conexión a Supabase (PostgreSQL)
conn = psycopg2.connect(
    host=os.environ.get("DB_HOST"),
    database=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    port=os.environ.get("DB_PORT")
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_pwm', methods=['POST'])
def set_pwm():
    data = request.json
    pwm = data['pwm']

    cursor = conn.cursor()
    cursor.execute("UPDATE control SET pwm = %s WHERE id = 1", (pwm,))
    conn.commit()

    return jsonify({"status": "ok", "pwm": pwm})

@app.route('/get_pwm', methods=['GET'])
def get_pwm():
    cursor = conn.cursor()
    cursor.execute("SELECT pwm FROM control WHERE id = 1")
    pwm = cursor.fetchone()[0]

    return jsonify({"pwm": pwm})

if __name__ == '__main__':
    app.run()
