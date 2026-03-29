from flask import Flask, jsonify, request, session, render_template_string
from flask_cors import CORS
from flask_session import Session
import json
import os
import requests
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ff_secret_key_2024'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False

SESSION_DIR = '/tmp/flask_session'
if not os.path.exists(SESSION_DIR):
    os.makedirs(SESSION_DIR)
app.config['SESSION_FILE_DIR'] = SESSION_DIR

Session(app)
CORS(app, supports_credentials=True)

DATA_FILE = 'data.json'

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def init_data():
    if not os.path.exists(DATA_FILE):
        default_data = {
            "users": [
                {"id": 1, "email": "admin@gmail.com", "password": "VIP@@01", "name": "Admin", "isAdmin": True, "createdAt": datetime.now().isoformat()}
            ],
            "transactions": [],
            "diamonds": [
                {"id": 1, "diamonds": 100, "price": 59, "originalPrice": 80, "available": True},
                {"id": 2, "diamonds": 310, "price": 179, "originalPrice": 240, "available": True},
                {"id": 3, "diamonds": 520, "price": 299, "originalPrice": 400, "available": True},
                {"id": 4, "diamonds": 1060, "price": 599, "originalPrice": 800, "available": True},
                {"id": 5, "diamonds": 2180, "price": 1199, "originalPrice": 1600, "available": True},
                {"id": 6, "diamonds": 5600, "price": 2999, "originalPrice": 4000, "available": True}
            ],
            "memberships": [
                {"id": "weekly_lite", "name": "WEEKLY LITE", "price": 40, "originalPrice": 50, "instant": 20, "daily": 10, "duration": 7, "available": True},
                {"id": "weekly", "name": "WEEKLY", "price": 127, "originalPrice": 159, "instant": 200, "daily": 35, "duration": 7, "available": True},
                {"id": "monthly", "name": "MONTHLY", "price": 639, "originalPrice": 799, "instant": 1000, "daily": 50, "duration": 30, "available": True}
            ],
            "settings": {
                "upiId": "omkardipt@fam",
                "qrImage": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAANaSURBVHgB7ZsxbttAFEUPFZAunQtYV+kC3kqXyC3SVYr0qXUJF2lTp0ufPgW2yphjSI3Mn6FEDufNA1jCkJS55H/yzZtBEARBEARBEARBEARBEARBEARBEARBEARBEARBEARBEARBEARBEARBEARBEARBEARBEARBEARBEARBEARBEARBEARBEARBEARBEARBEARB+D9jGIbBm80OjA0zGPYH8Hl/F1u+W9uw3+1gPp/BcrEA0zRZEEVRIM/zR1mWcYQ8gSAIYHh/gOPmCF3XcZRlCUmSwGw2A9u2wXVdDsdxoGkayLIMQgjIsgxM04S2baFpGoiiCKIo4iiKAkRRhKqqoCgK2LYNnufBx8cHHI9HuF6vUFUVRFEEcRxzFEUhhBAAgDAMoW1bSJIEXNeFpmlgPp/DbrcDAKAoCsjn8wnbtuEwjuNIgiCQ4/EoPctZz+dT0jRNwjCMpCgKiaJItm0rlFKJjzMMA6mqiqyXSwnDMEKpSCm1cM5j2zZMaZomSdNUXq+qitR1LSmVEkVRtOo8SZJAuq4TQgiM47hUzjmU9fZtCwCw2WzgeDzCYrGQHvI8DyGE5P1+jxAKJpMJrNdr2Gw2EIZhz7MsC4wxGIYBwzCgrmu4Xq9wPB6hbVsYhiFSqS0hBJRSAADDMECpBNM0wbIsiOMYwjCEzWYjhRBCoG1beZ7L5QJt28LxeITj8SiFhBBQFAUwxmSzYRgGqqqCJEkQx7H0SqUJIQjDMHzf9yEMQ4jjGDzPgyiK4P39XQpRSmE+n0PTNBCO40Cj0Sg8Ho/w8/Mjn2maJhgGsFwuYb/fy1mU53kQx7F88zxPvjYajdK1XJzHhQIhhHzf96EsS7LdboUwDIVpmuS6LrFtWzYaDZlpmuS6LkmlkufzKX+2bVuapiGCICCO40hRFFKpFKVUCiGELMsSx3FkGIYwDENmWRbLsiyUUkIYhsKyLGGaJpmmKTNNE8uyhBBC4rqueG/LsohSStI0jWmahuM4TNM0pus6M00T0zSNKYoSxhjDNE2maRoDADFNEwAAiqJgmqYhAACGYUjTNBBCgKIoAgDANE1QFAVCCKiqCgAAFEUBAADLsqSXEAQhBADA8zwAAFAUBUIIAACGYQCEEAAAwzCEEEJ8fHwAwzAghAAAWJYFQggBAIDrugAAwLZt6SUEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQRD+kz8B2ZYMMrQ+KY0AAAAASUVORK5CYII="
            }
        }
        with open(DATA_FILE, 'w') as f:
            json.dump(default_data, f, indent=2)

def read_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

init_data()

# ==================== API ROUTES ====================

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/data')
def get_data():
    data = read_data()
    return jsonify({
        'success': True,
        'diamonds': data['diamonds'],
        'memberships': data['memberships'],
        'settings': data['settings'],
        'user': session.get('user')
    })

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    db = read_data()
    for u in db['users']:
        if u['email'] == data['email'] and u['password'] == data['password']:
            session['user'] = {
                'id': u['id'],
                'email': u['email'],
                'name': u['name'],
                'isAdmin': u['isAdmin']
            }
            return jsonify({'success': True, 'user': session['user']})
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    db = read_data()
    for u in db['users']:
        if u['email'] == data['email']:
            return jsonify({'success': False, 'message': 'Email already exists'}), 400
    new_user = {
        'id': len(db['users']) + 1,
        'email': data['email'],
        'password': data['password'],
        'name': data.get('name', data['email'].split('@')[0]),
        'isAdmin': False,
        'createdAt': datetime.now().isoformat()
    }
    db['users'].append(new_user)
    write_data(db)
    session['user'] = {
        'id': new_user['id'],
        'email': new_user['email'],
        'name': new_user['name'],
        'isAdmin': False
    }
    return jsonify({'success': True, 'user': session['user']})

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

@app.route('/api/me')
def me():
    return jsonify({'success': True, 'user': session.get('user')})

@app.route('/api/transactions-by-uid/<uid>')
def get_transactions_by_uid(uid):
    db = read_data()
    user_transactions = [t for t in db['transactions'] if t['playerId'] == uid]
    return jsonify({'success': True, 'data': user_transactions})

@app.route('/api/diamonds/<int:diamond_id>', methods=['PUT'])
def update_diamond(diamond_id):
    if not session.get('user', {}).get('isAdmin'):
        return jsonify({'success': False}), 403
    db = read_data()
    for d in db['diamonds']:
        if d['id'] == diamond_id:
            d.update(request.json)
            write_data(db)
            return jsonify({'success': True})
    return jsonify({'success': False}), 404

@app.route('/api/memberships/<membership_id>', methods=['PUT'])
def update_membership(membership_id):
    if not session.get('user', {}).get('isAdmin'):
        return jsonify({'success': False}), 403
    db = read_data()
    for m in db['memberships']:
        if m['id'] == membership_id:
            m.update(request.json)
            write_data(db)
            return jsonify({'success': True})
    return jsonify({'success': False}), 404

@app.route('/api/settings', methods=['PUT'])
def update_settings():
    if not session.get('user', {}).get('isAdmin'):
        return jsonify({'success': False}), 403
    db = read_data()
    db['settings'].update(request.json)
    write_data(db)
    return jsonify({'success': True})

@app.route('/api/upload-qr', methods=['POST'])
def upload_qr():
    if not session.get('user', {}).get('isAdmin'):
        return jsonify({'success': False}), 403
    if 'qr' not in request.files:
        return jsonify({'success': False, 'message': 'No file'}), 400
    file = request.files['qr']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file'}), 400
    
    # Convert to base64 for storage
    import base64
    file_data = file.read()
    base64_qr = base64.b64encode(file_data).decode('utf-8')
    data_url = f"data:image/png;base64,{base64_qr}"
    
    db = read_data()
    db['settings']['qrImage'] = data_url
    write_data(db)
    return jsonify({'success': True, 'qrImage': data_url})

@app.route('/api/submit-payment', methods=['POST'])
def submit_payment():
    data = request.json
    if not data.get('utrNumber') or len(data['utrNumber']) != 12 or not data['utrNumber'].isdigit():
        return jsonify({'success': False, 'message': 'UTR must be 12 digits'}), 400
    db = read_data()
    transaction = {
        'id': int(datetime.now().timestamp() * 1000),
        'playerId': data['playerId'],
        'playerName': data.get('playerName', 'Unknown'),
        'itemType': data['itemType'],
        'itemName': data['itemName'],
        'amount': data['amount'],
        'utrNumber': data['utrNumber'],
        'status': 'pending',
        'createdAt': datetime.now().isoformat()
    }
    db['transactions'].insert(0, transaction)
    write_data(db)
    return jsonify({'success': True})

@app.route('/api/transactions')
def get_transactions():
    if not session.get('user', {}).get('isAdmin'):
        return jsonify({'success': False}), 403
    db = read_data()
    return jsonify({'success': True, 'data': db['transactions']})

@app.route('/api/transactions/<int:tx_id>/status', methods=['PUT'])
def update_transaction_status(tx_id):
    if not session.get('user', {}).get('isAdmin'):
        return jsonify({'success': False}), 403
    db = read_data()
    for tx in db['transactions']:
        if tx['id'] == tx_id:
            tx['status'] = request.json['status']
            write_data(db)
            return jsonify({'success': True})
    return jsonify({'success': False}), 404

@app.route('/api/stats')
def get_stats():
    if not session.get('user', {}).get('isAdmin'):
        return jsonify({'success': False}), 403
    db = read_data()
    revenue = sum(t['amount'] for t in db['transactions'] if t['status'] == 'completed')
    pending = len([t for t in db['transactions'] if t['status'] == 'pending'])
    return jsonify({
        'success': True,
        'data': {
            'totalRevenue': revenue,
            'pendingOrders': pending,
            'totalUsers': len(db['users'])
        }
    })

@app.route('/api/player-info/<uid>')
def player_info(uid):
    try:
        response = requests.get(f'https://info-api-production.up.railway.app/player-info?uid={uid}')
        data = response.json()
        if data and data.get('basicInfo'):
            return jsonify({
                'success': True,
                'data': {
                    'accountId': data['basicInfo']['accountId'],
                    'nickname': data['basicInfo']['nickname'],
                    'region': data['basicInfo']['region'],
                    'level': data['basicInfo']['level'],
                    'rank': data['basicInfo']['rank'],
                    'creditScore': data.get('creditScoreInfo', {}).get('creditScore', 100)
                }
            })
        return jsonify({'success': False}), 404
    except:
        return jsonify({'success': False}), 500

# ==================== HTML TEMPLATE ====================

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FF Top-Up Center</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
        }
        body {
            background: #0a0c15;
            color: #fff;
        }
        .container {
            max-width: 1300px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 1px solid #2a2f3f;
        }
        .logo h1 {
            font-size: 1.8rem;
            background: linear-gradient(135deg, #FFD966, #FF8C42);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        .logo p {
            font-size: 0.75rem;
            color: #8e9aaf;
        }
        .btn {
            padding: 8px 20px;
            border-radius: 30px;
            cursor: pointer;
            font-weight: 600;
            border: none;
            transition: 0.2s;
        }
        .btn-primary {
            background: #ff8c42;
            color: white;
        }
        .btn-outline {
            background: transparent;
            border: 1px solid #ff8c42;
            color: #ff8c42;
        }
        .player-card {
            background: #111725;
            border-radius: 24px;
            padding: 24px;
            margin-bottom: 30px;
            border: 1px solid #ff8c4233;
        }
        .player-header {
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 20px;
        }
        .avatar {
            width: 70px;
            height: 70px;
            background: linear-gradient(135deg, #ff8c42, #ff6b2c);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
        }
        .player-id-input {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-top: 15px;
        }
        .player-id-input input {
            flex: 1;
            padding: 12px 18px;
            background: #1e2538;
            border: 1px solid #2e364e;
            border-radius: 40px;
            color: white;
            font-size: 1rem;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(90px, 1fr));
            gap: 12px;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #2a2f3f;
        }
        .stat {
            text-align: center;
        }
        .stat-value {
            font-size: 1.2rem;
            font-weight: bold;
            color: #ff8c42;
        }
        .stat-label {
            font-size: 0.7rem;
            color: #8e9aaf;
        }
        .section-title {
            font-size: 1.3rem;
            margin: 30px 0 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .section-title i {
            color: #ff8c42;
        }
        .diamond-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
            gap: 16px;
            margin-bottom: 30px;
        }
        .diamond-card {
            background: #131a2c;
            border-radius: 24px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            border: 1px solid #2a314a;
            transition: 0.2s;
            position: relative;
        }
        .diamond-card:hover {
            border-color: #ff8c42;
            transform: translateY(-3px);
        }
        .diamond-card.sold-out {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .badge {
            position: absolute;
            top: -10px;
            right: 10px;
            background: #ff4444;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: bold;
        }
        .diamond-amount {
            font-size: 1.6rem;
            font-weight: bold;
            color: #ffb347;
        }
        .price {
            font-size: 1.4rem;
            font-weight: bold;
            color: #ffb347;
            margin: 8px 0;
        }
        .old-price {
            font-size: 0.75rem;
            text-decoration: line-through;
            color: #6c757d;
        }
        .membership-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .membership-card {
            background: #131a2c;
            border-radius: 24px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            border: 1px solid #2a314a;
            transition: 0.2s;
            position: relative;
        }
        .membership-card:hover {
            border-color: #ff8c42;
            transform: translateY(-3px);
        }
        .membership-card.sold-out {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .reward-item {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            margin: 8px 0;
            color: #a0a8c0;
        }
        .total-reward {
            margin-top: 12px;
            padding-top: 8px;
            border-top: 1px solid #2a2f3f;
            color: #ff8c42;
            font-weight: bold;
        }
        .admin-panel {
            background: #0c0f1c;
            border-radius: 28px;
            padding: 24px;
            margin-top: 30px;
            border: 1px solid #ff8c42;
        }
        .price-row {
            background: #1e253f;
            padding: 12px;
            border-radius: 20px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 10px;
        }
        .price-row input {
            width: 100px;
            padding: 6px 10px;
            background: #0b0e1a;
            border: 1px solid #ff8c42;
            border-radius: 30px;
            color: white;
        }
        .price-row select {
            padding: 6px 10px;
            background: #0b0e1a;
            border: 1px solid #ff8c42;
            border-radius: 30px;
            color: white;
        }
        .modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.95);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            visibility: hidden;
            opacity: 0;
            transition: 0.2s;
        }
        .modal.show {
            visibility: visible;
            opacity: 1;
        }
        .modal-content {
            background: #12182e;
            max-width: 450px;
            width: 90%;
            border-radius: 32px;
            padding: 28px;
            border: 1px solid #ff8c42;
        }
        .qr-img {
            background: white;
            padding: 20px;
            border-radius: 16px;
            text-align: center;
            margin: 15px 0;
        }
        .qr-img img {
            max-width: 200px;
            width: 100%;
            border-radius: 8px;
        }
        .upi-id {
            background: #1e2538;
            padding: 12px;
            border-radius: 12px;
            text-align: center;
            margin: 12px 0;
            font-family: monospace;
            font-size: 1.1rem;
        }
        input {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            background: #1e2538;
            border: 1px solid #334155;
            border-radius: 40px;
            color: white;
        }
        .toast {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #28a745;
            color: #fff;
            padding: 12px 24px;
            border-radius: 50px;
            z-index: 2000;
            font-weight: 500;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            display: flex;
            align-items: center;
            gap: 12px;
            min-width: 280px;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
        }
        .toast.show {
            opacity: 1;
            visibility: visible;
        }
        .toast.error {
            background: #dc3545;
        }
        .toast.warning {
            background: #ffc107;
            color: #333;
        }
        .transaction-item {
            background: #1a1f2e;
            padding: 12px;
            margin: 8px 0;
            border-radius: 12px;
        }
        .qr-upload-area {
            border: 2px dashed #ff8c42;
            border-radius: 20px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            margin: 10px 0;
        }
        .history-item {
            background: #1a1f2e;
            padding: 15px;
            margin: 10px 0;
            border-radius: 16px;
            border-left: 3px solid #ff8c42;
        }
        .status-pending {
            color: #ffc107;
        }
        .status-completed {
            color: #28a745;
        }
        .status-failed {
            color: #dc3545;
        }
        .view-history-btn {
            margin-left: 15px;
            background: #1e2538;
            border: 1px solid #ff8c42;
            color: #ff8c42;
        }
        @media (max-width: 700px) {
            .container {
                padding: 12px;
            }
            .diamond-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            .toast {
                bottom: 20px;
                right: 20px;
                left: 20px;
                text-align: center;
            }
        }
    </style>
</head>
<body>
{% raw %}
<div id="app">
    <div class="container">
        <!-- Header -->
        <div class="header">
            <div class="logo">
                <h1><i class="fas fa-diamond"></i> FF TOP-UP</h1>
                <p>Official Partner • 25% OFF</p>
            </div>
            <div>
                <span v-if="currentUser" style="background:#1a1f2e;padding:8px 16px;border-radius:30px;margin-right:12px">
                    <i class="fas fa-user-circle"></i> {{ currentUser.name }}
                    <span v-if="currentUser.isAdmin" style="color:#ffaa53">(Admin)</span>
                </span>
                <button v-if="!currentUser" class="btn btn-outline" @click="showLoginModal = true">Login</button>
                <button v-if="currentUser" class="btn btn-outline" @click="logout">Logout</button>
            </div>
        </div>

        <!-- Player Info Card -->
        <div class="player-card">
            <div class="player-header">
                <div class="avatar"><i class="fas fa-user-ninja"></i></div>
                <div>
                    <h2 v-if="playerInfo">
                        {{ playerInfo.nickname }}
                        <span style="background:#28a745;padding:2px 10px;border-radius:20px;font-size:0.7rem">
                            <i class="fas fa-check-circle"></i> Verified
                        </span>
                    </h2>
                    <h2 v-else>Enter Player ID</h2>
                    <p style="color:#8e9aaf">Free Fire Account</p>
                </div>
            </div>
            <div class="player-id-input">
                <input type="text" v-model="uidInput" placeholder="Enter Player ID" @keyup.enter="fetchPlayerInfo">
                <button class="btn btn-primary" @click="fetchPlayerInfo" :disabled="loadingPlayer">
                    <i class="fas fa-search"></i>
                    <span v-if="loadingPlayer">Verifying...</span>
                    <span v-else>Verify Account</span>
                </button>
                <button v-if="playerInfo" class="btn btn-outline view-history-btn" @click="showHistoryModal = true">
                    <i class="fas fa-history"></i> View My History
                </button>
            </div>
            <div v-if="playerInfo" class="stats-grid">
                <div class="stat"><div class="stat-value">Lv.{{ playerInfo.level }}</div><div class="stat-label">Level</div></div>
                <div class="stat"><div class="stat-value">{{ playerInfo.rank }}</div><div class="stat-label">Rank</div></div>
                <div class="stat"><div class="stat-value">{{ playerInfo.region }}</div><div class="stat-label">Region</div></div>
                <div class="stat"><div class="stat-value">{{ playerInfo.creditScore }}%</div><div class="stat-label">Credit Score</div></div>
            </div>
        </div>

        <!-- Diamond Packs -->
        <div class="section-title"><i class="fas fa-gem"></i> Diamond Packs (25% OFF)</div>
        <div class="diamond-grid">
            <div v-for="item in diamonds" :key="item.id" class="diamond-card" :class="{ 'sold-out': !item.available }" @click="initiatePayment('diamond', item)">
                <div class="badge" v-if="item.available">SAVE ₹{{ item.originalPrice - item.price }}</div>
                <div class="badge" v-else style="background:#6c757d">SOLD OUT</div>
                <div class="diamond-amount">{{ item.diamonds }} 💎</div>
                <div class="price">₹{{ item.price }}</div>
                <div class="old-price">Official: ₹{{ item.originalPrice }}</div>
            </div>
        </div>

        <!-- Membership Plans -->
        <div class="section-title"><i class="fas fa-crown"></i> Membership Plans</div>
        <div class="membership-grid">
            <div v-for="deal in memberships" :key="deal.id" class="membership-card" :class="{ 'sold-out': !deal.available }" @click="initiatePayment('membership', deal)">
                <div class="badge" v-if="deal.available" style="background:#ff8c42">SAVE ₹{{ deal.originalPrice - deal.price }}</div>
                <div class="badge" v-else style="background:#6c757d">SOLD OUT</div>
                <div class="diamond-amount">{{ deal.name }}</div>
                <div class="price">₹{{ deal.price }}</div>
                <div class="old-price">Regular: ₹{{ deal.originalPrice }}</div>
                <div class="reward-item"><span>✨ Instant:</span><span>{{ deal.instant }} 💎</span></div>
                <div class="reward-item"><span>📅 Daily ({{ deal.duration }} days):</span><span>{{ deal.daily }} 💎</span></div>
                <div class="total-reward">🎁 TOTAL: {{ deal.instant + (deal.daily * deal.duration) }} 💎</div>
            </div>
        </div>

        <!-- Admin Panel -->
        <div v-if="currentUser && currentUser.isAdmin" class="admin-panel">
            <h3 style="margin-bottom:16px"><i class="fas fa-shield-alt"></i> Admin Panel</h3>
            <div style="display:flex; gap:15px; margin-bottom:20px; flex-wrap:wrap">
                <div style="background:#1a1f2e; padding:12px; border-radius:16px"><div style="color:#ff8c42; font-size:1.3rem">₹{{ stats.totalRevenue }}</div><div>Revenue</div></div>
                <div style="background:#1a1f2e; padding:12px; border-radius:16px"><div style="color:#ff8c42; font-size:1.3rem">{{ stats.pendingOrders }}</div><div>Pending</div></div>
                <div style="background:#1a1f2e; padding:12px; border-radius:16px"><div style="color:#ff8c42; font-size:1.3rem">{{ stats.totalUsers }}</div><div>Users</div></div>
            </div>

            <h4><i class="fas fa-edit"></i> Edit UPI Settings</h4>
            <div class="price-row">
                <span>UPI ID:</span>
                <input type="text" v-model="settings.upiId" style="width:200px">
                <button class="btn btn-primary" @click="updateSettings">Save</button>
            </div>

            <h4><i class="fas fa-qrcode"></i> Update QR Code</h4>
            <div class="price-row">
                <div style="width:100%">
                    <div class="qr-upload-area" @click="triggerFileUpload">
                        <i class="fas fa-upload"></i> Click to Upload QR Code
                        <input type="file" ref="qrFile" @change="handleQRUpload" accept="image/*" style="display:none">
                    </div>
                    <div v-if="settings.qrImage" style="text-align:center; margin-top:10px">
                        <img :src="settings.qrImage" style="max-width:100px; border-radius:10px; border:1px solid #ff8c42">
                        <p style="font-size:0.7rem; margin-top:5px">Current QR Code</p>
                    </div>
                </div>
            </div>

            <h4><i class="fas fa-gem"></i> Edit Diamond Prices</h4>
            <div v-for="item in diamonds" :key="'edit' + item.id" class="price-row">
                <span><strong>{{ item.diamonds }} 💎</strong> | Official: ₹{{ item.originalPrice }}</span>
                <span>Our Price: ₹<input type="number" v-model.number="item.price" step="5"></span>
                <span>Status: 
                    <select v-model="item.available">
                        <option :value="true">Available</option>
                        <option :value="false">Sold Out</option>
                    </select>
                </span>
                <button class="btn btn-primary" @click="updateDiamond(item)">Update</button>
            </div>

            <h4><i class="fas fa-crown"></i> Edit Membership Prices</h4>
            <div v-for="deal in memberships" :key="'edit' + deal.id" class="price-row">
                <span><strong>{{ deal.name }}</strong> | Official: ₹{{ deal.originalPrice }}</span>
                <span>Our Price: ₹<input type="number" v-model.number="deal.price" step="10"></span>
                <span>Status: 
                    <select v-model="deal.available">
                        <option :value="true">Available</option>
                        <option :value="false">Sold Out</option>
                    </select>
                </span>
                <button class="btn btn-primary" @click="updateMembership(deal)">Update</button>
            </div>

            <h4><i class="fas fa-history"></i> Recent Transactions</h4>
            <div v-for="tx in transactions.slice(0,10)" :key="tx.id" class="transaction-item">
                <div><strong>{{ tx.playerName }}</strong> | {{ tx.itemName }} | ₹{{ tx.amount }} | UTR: {{ tx.utrNumber }}</div>
                <div>Status: 
                    <select :value="tx.status" @change="updateStatus(tx.id, $event.target.value)">
                        <option value="pending">⏳ Pending</option>
                        <option value="completed">✅ Completed</option>
                        <option value="failed">❌ Failed</option>
                    </select>
                </div>
            </div>
        </div>

        <!-- Transaction History Modal -->
        <div class="modal" :class="{ show: showHistoryModal }">
            <div class="modal-content" style="max-width: 600px;">
                <h3 style="text-align:center; margin-bottom:20px"><i class="fas fa-history"></i> Transaction History</h3>
                <div v-if="historyLoading" style="text-align:center; padding:40px"><i class="fas fa-spinner fa-spin"></i> Loading...</div>
                <div v-else-if="myTransactions.length === 0" style="text-align:center; padding:40px; color:#8e9aaf"><i class="fas fa-inbox"></i> No transactions found</div>
                <div v-else>
                    <div v-for="tx in myTransactions" :key="tx.id" class="history-item">
                        <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px">
                            <div><strong>{{ tx.itemName }}</strong><br><small>{{ formatDate(tx.createdAt) }}</small></div>
                            <div style="text-align:right"><div class="price" style="font-size:1.2rem">₹{{ tx.amount }}</div><div :class="'status-' + tx.status">{{ capitalize(tx.status) }}</div></div>
                        </div>
                        <div style="margin-top:8px; font-size:0.8rem; color:#8e9aaf">UTR: {{ tx.utrNumber }}</div>
                    </div>
                </div>
                <button class="btn btn-outline" style="width:100%; margin-top:20px" @click="showHistoryModal = false">Close</button>
            </div>
        </div>
    </div>

    <!-- Payment Modal -->
    <div class="modal" :class="{ show: showPaymentModal }">
        <div class="modal-content">
            <h3 style="text-align:center"><i class="fas fa-qrcode"></i> Pay via UPI</h3>
            <div class="qr-img">
                <img :src="settings.qrImage" alt="QR Code">
            </div>
            <div class="upi-id">
                <i class="fas fa-phone-alt"></i> {{ settings.upiId }}
            </div>
            <div class="price" style="text-align:center; font-size:1.8rem">₹{{ paymentAmount }}</div>
            <input type="text" v-model="utrNumber" placeholder="12-digit UTR Number" maxlength="12" @input="utrNumber = utrNumber.replace(/[^0-9]/g, '').slice(0,12)">
            <div style="font-size:0.7rem; color:#8e9aaf; text-align:center">UTR must be exactly 12 digits (numbers only)</div>
            <button class="btn btn-primary" style="width:100%" @click="submitPayment" :disabled="utrNumber.length !== 12">Submit Payment</button>
            <button class="btn btn-outline" style="width:100%; margin-top:10px" @click="closeModal">Cancel</button>
            <div v-if="paymentSuccess" style="background:#28a745; padding:10px; border-radius:12px; margin-top:12px; text-align:center">
                <i class="fas fa-check-circle"></i> Payment Submitted!
            </div>
        </div>
    </div>

    <!-- Login Modal -->
    <div class="modal" :class="{ show: showLoginModal }">
        <div class="modal-content">
            <h3 style="text-align:center"><i class="fas fa-user-circle"></i> Login / Register</h3>
            <input type="email" v-model="loginEmail" placeholder="Email">
            <input type="password" v-model="loginPassword" placeholder="Password">
            <input type="text" v-model="registerName" placeholder="Name (optional)">
            <button class="btn btn-primary" style="width:100%" @click="login">Login</button>
            <button class="btn btn-outline" style="width:100%; margin-top:10px" @click="register">Register</button>
            <button class="btn btn-outline" style="width:100%; margin-top:10px" @click="showLoginModal = false">Close</button>
            <div style="font-size:0.7rem; text-align:center; margin-top:12px; color:#ffaa66">
                <i class="fas fa-info-circle"></i> Admin: ADMIN LOGIN USER REGISTER FIRST
            </div>
        </div>
    </div>

    <!-- Toast Message -->
    <div class="toast" :class="{ show: toastMsg != '', error: toastType == 'error', warning: toastType == 'warning' }">
        <i :class="'fas ' + toastIcon"></i>
        <span>{{ toastMsg }}</span>
    </div>
</div>
{% endraw %}

<script src="https://cdn.jsdelivr.net/npm/vue@2.7.14/dist/vue.js"></script>
<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
<script>
    axios.defaults.baseURL = window.location.origin;
    axios.defaults.withCredentials = true;

    new Vue({
        el: '#app',
        data: {
            uidInput: '',
            playerInfo: null,
            loadingPlayer: false,
            diamonds: [],
            memberships: [],
            settings: {},
            currentUser: null,
            transactions: [],
            myTransactions: [],
            historyLoading: false,
            showHistoryModal: false,
            stats: { totalRevenue: 0, pendingOrders: 0, totalUsers: 0 },
            showPaymentModal: false,
            showLoginModal: false,
            paymentAmount: 0,
            paymentItem: null,
            paymentType: null,
            utrNumber: '',
            paymentSuccess: false,
            loginEmail: '',
            loginPassword: '',
            registerName: '',
            toastMsg: '',
            toastType: 'success',
            toastTimer: null
        },
        computed: {
            toastIcon: function() {
                if (this.toastType === 'error') return 'fa-exclamation-circle';
                if (this.toastType === 'warning') return 'fa-exclamation-triangle';
                return 'fa-check-circle';
            }
        },
        watch: {
            showHistoryModal: function(val) {
                if (val && this.playerInfo) {
                    this.loadTransactionHistory();
                }
            }
        },
        mounted: function() {
            this.fetchData();
            this.checkSession();
        },
        methods: {
            formatDate: function(dateStr) {
                return new Date(dateStr).toLocaleString();
            },
            capitalize: function(str) {
                if (!str) return '';
                return str.charAt(0).toUpperCase() + str.slice(1);
            },
            showToast: function(msg, type) {
                if (this.toastTimer) clearTimeout(this.toastTimer);
                this.toastMsg = msg;
                this.toastType = type || 'success';
                var self = this;
                this.toastTimer = setTimeout(function() {
                    self.toastMsg = '';
                }, 3000);
            },
            loadTransactionHistory: async function() {
                if (!this.playerInfo) return;
                this.historyLoading = true;
                try {
                    var res = await axios.get('/api/transactions-by-uid/' + this.playerInfo.accountId);
                    if (res.data.success) {
                        this.myTransactions = res.data.data;
                    }
                } catch(e) {
                    this.showToast('Failed to load history', 'error');
                }
                this.historyLoading = false;
            },
            fetchData: async function() {
                try {
                    var res = await axios.get('/api/data');
                    if (res.data.success) {
                        this.diamonds = res.data.diamonds;
                        this.memberships = res.data.memberships;
                        this.settings = res.data.settings;
                        if (res.data.user) this.currentUser = res.data.user;
                    }
                } catch(e) {
                    this.showToast('Failed to load data', 'error');
                }
            },
            checkSession: async function() {
                try {
                    var res = await axios.get('/api/me');
                    if (res.data.user) {
                        this.currentUser = res.data.user;
                        if (this.currentUser.isAdmin) this.fetchAdminData();
                    }
                } catch(e) {}
            },
            fetchAdminData: async function() {
                try {
                    var transRes = await axios.get('/api/transactions');
                    var statsRes = await axios.get('/api/stats');
                    if (transRes.data.success) this.transactions = transRes.data.data;
                    if (statsRes.data.success) this.stats = statsRes.data.data;
                } catch(e) {}
            },
            fetchPlayerInfo: async function() {
                if (!this.uidInput || !/^\\d+$/.test(this.uidInput)) {
                    this.showToast('Enter valid Player ID (numbers only)', 'warning');
                    return;
                }
                this.loadingPlayer = true;
                try {
                    var res = await axios.get('/api/player-info/' + this.uidInput);
                    if (res.data.success) {
                        this.playerInfo = res.data.data;
                        this.showToast('Account Verified! Welcome ' + this.playerInfo.nickname, 'success');
                    } else {
                        this.showToast('Player not found', 'error');
                        this.playerInfo = null;
                    }
                } catch(e) {
                    this.showToast('Failed to fetch player info', 'error');
                    this.playerInfo = null;
                }
                this.loadingPlayer = false;
            },
            initiatePayment: function(type, item) {
                if (!item.available) {
                    this.showToast('This item is sold out', 'warning');
                    return;
                }
                if (!this.playerInfo) {
                    this.showToast('Please verify your Player ID first', 'warning');
                    return;
                }
                this.paymentType = type;
                this.paymentItem = item;
                this.paymentAmount = item.price;
                this.utrNumber = '';
                this.paymentSuccess = false;
                this.showPaymentModal = true;
            },
            submitPayment: async function() {
                if (this.utrNumber.length !== 12) {
                    this.showToast('UTR must be 12 digits only', 'warning');
                    return;
                }
                try {
                    var itemName = '';
                    if (this.paymentType === 'diamond') {
                        itemName = this.paymentItem.diamonds + ' Diamonds';
                    } else {
                        itemName = this.paymentItem.name;
                    }
                    await axios.post('/api/submit-payment', {
                        playerId: this.playerInfo.accountId,
                        playerName: this.playerInfo.nickname,
                        itemType: this.paymentType,
                        itemName: itemName,
                        amount: this.paymentAmount,
                        utrNumber: this.utrNumber
                    });
                    this.paymentSuccess = true;
                    this.showToast('Payment submitted! UTR: ' + this.utrNumber, 'success');
                    var self = this;
                    setTimeout(function() {
                        self.closeModal();
                    }, 2000);
                } catch(e) {
                    this.showToast('Submission failed', 'error');
                }
            },
            closeModal: function() {
                this.showPaymentModal = false;
                this.paymentSuccess = false;
                this.utrNumber = '';
            },
            triggerFileUpload: function() {
                this.$refs.qrFile.click();
            },
            handleQRUpload: async function(event) {
                var file = event.target.files[0];
                if (file) {
                    var formData = new FormData();
                    formData.append('qr', file);
                    try {
                        var res = await axios.post('/api/upload-qr', formData);
                        if (res.data.success) {
                            this.settings.qrImage = res.data.qrImage;
                            this.showToast('QR Code updated successfully!', 'success');
                        }
                    } catch(e) {
                        this.showToast('Upload failed', 'error');
                    }
                }
            },
            login: async function() {
                try {
                    var res = await axios.post('/api/login', {
                        email: this.loginEmail,
                        password: this.loginPassword
                    });
                    if (res.data.success) {
                        this.currentUser = res.data.user;
                        this.showLoginModal = false;
                        this.showToast('Welcome ' + this.currentUser.name, 'success');
                        if (this.currentUser.isAdmin) this.fetchAdminData();
                        this.loginEmail = '';
                        this.loginPassword = '';
                    } else {
                        this.showToast('Invalid credentials', 'error');
                    }
                } catch(e) {
                    this.showToast('Login failed', 'error');
                }
            },
            register: async function() {
                if (!this.loginEmail || !this.loginPassword) {
                    this.showToast('Email and password required', 'warning');
                    return;
                }
                try {
                    var res = await axios.post('/api/register', {
                        email: this.loginEmail,
                        password: this.loginPassword,
                        name: this.registerName
                    });
                    if (res.data.success) {
                        this.currentUser = res.data.user;
                        this.showLoginModal = false;
                        this.showToast('Registration successful!', 'success');
                        this.loginEmail = '';
                        this.loginPassword = '';
                        this.registerName = '';
                    }
                } catch(e) {
                    var msg = 'Registration failed';
                    if (e.response && e.response.data && e.response.data.message) {
                        msg = e.response.data.message;
                    }
                    this.showToast(msg, 'error');
                }
            },
            logout: async function() {
                await axios.post('/api/logout');
                this.currentUser = null;
                this.playerInfo = null;
                this.showToast('Logged out', 'success');
            },
            updateDiamond: async function(item) {
                try {
                    await axios.put('/api/diamonds/' + item.id, {
                        price: item.price,
                        available: item.available
                    });
                    this.showToast(item.diamonds + ' Diamonds price updated', 'success');
                } catch(e) {
                    this.showToast('Update failed', 'error');
                }
            },
            updateMembership: async function(deal) {
                try {
                    await axios.put('/api/memberships/' + deal.id, {
                        price: deal.price,
                        available: deal.available
                    });
                    this.showToast(deal.name + ' price updated', 'success');
                } catch(e) {
                    this.showToast('Update failed', 'error');
                }
            },
            updateSettings: async function() {
                try {
                    await axios.put('/api/settings', {
                        upiId: this.settings.upiId
                    });
                    this.showToast('Settings updated', 'success');
                } catch(e) {
                    this.showToast('Update failed', 'error');
                }
            },
            updateStatus: async function(id, status) {
                try {
                    await axios.put('/api/transactions/' + id + '/status', {
                        status: status
                    });
                    this.showToast('Transaction status updated', 'success');
                    this.fetchAdminData();
                } catch(e) {
                    this.showToast('Update failed', 'error');
                }
            }
        }
    });
</script>
</body>
</html>
'''

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 3000))
    app.run(debug=False, host='0.0.0.0', port=port)