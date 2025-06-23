from flask import Flask, request, jsonify
from logger import get_logger
from DBconnection import get_connection
from exceptions import DatabaseConnectionError

app = Flask(__name__)
logger = get_logger("ChatbotAPI")

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get("message")
        logger.info(f"Received input: {user_input}")

        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        # Dummy response — replace with model or DB logic
        response = f"Echo: {user_input}"

        return jsonify({"reply": response})

    except DatabaseConnectionError:
        logger.error("Database error occurred.")
        return jsonify({"error": "Internal database error"}), 500

    except Exception as e:
        logger.exception("Unhandled exception occurred")
        return jsonify({"error": "Something went wrong"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
