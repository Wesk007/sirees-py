#!/usr/bin/env python3
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/registro', methods=['POST'])
def registro():
    # Asegurarnos de que venga JSON
    if not request.is_json:
        return jsonify({
            'status': 'error',
            'message': 'JSON inválido'
        }), 400

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({
            'status': 'error',
            'message': 'JSON inválido'
        }), 400

    uid = data.get('uid')
    if not uid:
        return jsonify({
            'status': 'error',
            'message': 'Falta el UID'
        }), 422

    # Aquí podrías insertar en BD, validar, etc. jajajaj

    return jsonify({
        'status': 'ok',
        'rfid': uid
    }), 200

if __name__ == '__main__':
    # Ejecuta el servidor en 0.0.0.0:5000
    app.run(host='0.0.0.0', port=5001)
