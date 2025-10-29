from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 🔒 Твой Telegram бот
TELEGRAM_BOT_TOKEN = "8310007182:AAFzFIpy2TxzIOhJrT7hmovZh2tW6nu13XY"
TELEGRAM_CHAT_ID = "-5084363669"

# 🔐 Секрет для безопасности (тот же нужно указать в Roblox скрипте)
SECRET_KEY = "super_secret_key"

@app.route('/report', methods=['POST'])
def receive_report():
    data = request.get_json()
    
    # Проверка наличия данных
    if not data:
        return jsonify({'status': 'error', 'message': 'No JSON received'}), 400

    # Проверка секрета (чтобы никто чужой не мог слать запросы)
    if data.get('secret') != SECRET_KEY:
        return jsonify({'status': 'error', 'message': 'Invalid secret'}), 403
    
    player_name = data.get('player', 'Unknown')
    message = data.get('message', 'No message')
    report_type = data.get('type', 'Unknown')

    telegram_message = f"🔔 New {report_type}\n\n👤 Player: {player_name}\n📝 Message:\n{message}"

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': telegram_message,
        'parse_mode': 'HTML'
    }

    try:
        response = requests.post(telegram_url, json=payload, timeout=10)
        if response.status_code == 200:
            return jsonify({'status': 'success', 'message': 'Report sent to Telegram'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Telegram error', 'code': response.status_code}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/')
def index():
    return "✅ Flask report bot is running!", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
