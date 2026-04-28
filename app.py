from flask import Flask, request, jsonify, render_template
import psycopg2
import os

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
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
    try:
        data = request.get_json()
        pwm = data.get('pwm')

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE control SET pwm = %s WHERE id = 1",
            (pwm,)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"status": "ok", "pwm": pwm})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_pwm', methods=['GET'])
def get_pwm():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT pwm FROM control WHERE id = 1")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result is None:
            return jsonify({"error": "No hay datos"}), 404

        return jsonify({"pwm": result[0]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run()
