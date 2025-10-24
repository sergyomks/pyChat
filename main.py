from flask import Flask, render_template, request, jsonify
import pusher
from datetime import datetime

app = Flask(__name__)

# Configuración de Pusher - REEMPLAZA CON TUS CREDENCIALES
pusher_client = pusher.Pusher(
    app_id='2068334',
    key='31153268659b032b4c42',  # Tu key de Pusher
    secret='4d7138418ddc381f1cf9',
    cluster='us2',  # Tu cluster
    ssl=True
)

# Almacenar mensajes
messages = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        username = data.get('username')
        message = data.get('message')
        
        if not username or not message:
            return jsonify({'error': 'Username y mensaje son requeridos'}), 400
        
        # Crear objeto mensaje
        message_data = {
            'username': username,
            'message': message,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }
        
        # Guardar mensaje
        messages.append(message_data)
        
        # Enviar mensaje a través de Pusher - USANDO EL FORMATO SUGERIDO
        pusher_client.trigger('my-channel', 'my-event', message_data)
        
        return jsonify({'status': 'success', 'message': message_data})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_messages', methods=['GET'])
def get_messages():
    return jsonify({'messages': messages})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

