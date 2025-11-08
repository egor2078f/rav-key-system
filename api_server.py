from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Разрешаем запросы из Roblox

KEYS_DB = "keys_db.json"

def load_keys():
    try:
        with open(KEYS_DB, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_keys(keys):
    with open(KEYS_DB, 'w', encoding='utf-8') as f:
        json.dump(keys, f, ensure_ascii=False, indent=2)

@app.route('/')
def home():
    """Главная страница"""
    return jsonify({
        'name': 'RAV Key Verification API',
        'version': '1.0',
        'status': 'online',
        'endpoints': {
            'verify': '/verify - POST/GET - Проверка ключа',
            'check': '/check - GET - Проверка без использования',
            'stats': '/stats - GET - Статистика',
            'health': '/health - GET - Статус API'
        }
    }), 200

@app.route('/verify', methods=['POST', 'GET'])
def verify_key():
    """Проверка и использование ключа"""
    try:
        # Получаем ключ
        if request.method == 'POST':
            data = request.get_json()
            key = data.get('key', '') if data else ''
        else:
            key = request.args.get('key', '')
        
        if not key:
            return jsonify({
                'success': False,
                'message': '❌ Ключ не предоставлен'
            }), 400
        
        # Загружаем базу
        keys = load_keys()
        
        # Проверяем существование
        if key not in keys:
            return jsonify({
                'success': False,
                'message': '❌ Неверный ключ'
            }), 401
        
        key_data = keys[key]
        
        # Проверяем использование
        if key_data.get('used', False):
            return jsonify({
                'success': False,
                'message': '❌ Ключ уже использован'
            }), 401
        
        # Проверяем срок
        expires = datetime.fromisoformat(key_data['expires'])
        if datetime.now() > expires:
            return jsonify({
                'success': False,
                'message': '❌ Ключ истек'
            }), 401
        
        # Отмечаем как использованный
        keys[key]['used'] = True
        keys[key]['used_at'] = datetime.now().isoformat()
        save_keys(keys)
        
        return jsonify({
            'success': True,
            'message': '✅ Ключ действителен!',
            'data': {
                'key': key,
                'user_id': key_data['user_id'],
                'expires': key_data['expires']
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'❌ Ошибка: {str(e)}'
        }), 500

@app.route('/check', methods=['GET'])
def check_key():
    """Проверка ключа без использования"""
    try:
        key = request.args.get('key', '')
        
        if not key:
            return jsonify({'valid': False, 'reason': 'no_key'}), 400
        
        keys = load_keys()
        
        if key not in keys:
            return jsonify({'valid': False, 'reason': 'not_found'}), 200
        
        key_data = keys[key]
        
        if key_data.get('used', False):
            return jsonify({'valid': False, 'reason': 'used'}), 200
        
        expires = datetime.fromisoformat(key_data['expires'])
        if datetime.now() > expires:
            return jsonify({'valid': False, 'reason': 'expired'}), 200
        
        return jsonify({
            'valid': True,
            'expires': key_data['expires'],
            'user_id': key_data['user_id']
        }), 200
        
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Статистика ключей"""
    try:
        keys = load_keys()
        
        total = len(keys)
        used = sum(1 for k in keys.values() if k.get('used', False))
        
        active = 0
        expired = 0
        for k in keys.values():
            if not k.get('used', False):
                expires = datetime.fromisoformat(k['expires'])
                if datetime.now() < expires:
                    active += 1
                else:
                    expired += 1
        
        return jsonify({
            'total_keys': total,
            'used_keys': used,
            'active_keys': active,
            'expired_keys': expired,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Проверка работы API"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'service': 'RAV Key API'
    }), 200

if __name__ == '__main__':
    print("=" * 60)
    print("🔥 RAV KEY VERIFICATION API SERVER")
    print("=" * 60)
    print("📡 Endpoints:")
    print("   🏠 /          - Home page")
    print("   ✅ /verify    - Verify and use key")
    print("   🔍 /check     - Check key without using")
    print("   📊 /stats     - Key statistics")
    print("   💚 /health    - Health check")
    print("=" * 60)
    print("🚀 Starting server...")
    print("=" * 60)
    
    # Для разработки
    app.run(host='0.0.0.0', port=5000, debug=True)
