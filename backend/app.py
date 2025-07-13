import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from models import Todo, db
from config import Config
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 修改這裡：指定靜態文件夾為前端打包後的 dist 目錄
app = Flask(__name__, 
           static_folder='../frontend/dist', 
           static_url_path='/')

# 根據環境選擇配置
if os.environ.get('FLASK_ENV') == 'production':
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

# 修改 CORS 設定
if os.environ.get('FLASK_ENV') == 'production':
    # 生產環境 - 不需要 CORS，因為前後端同源
    # CORS(app, origins=[...])  # 註釋掉或刪除
    pass
else:
    # 開發環境 - 保持原設定
    CORS(app)

# 初始化資料庫
db.init_app(app)

@app.before_request
def create_tables():
    if not hasattr(create_tables, 'done'):
        with app.app_context():
            db.create_all()
        create_tables.done = True

# 健康檢查端點
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'API is running'}), 200

# 添加前端路由處理
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# 處理前端 SPA 路由
@app.route('/<path:path>')
def catch_all(path):
    # 如果是 API 路由，跳過
    if path.startswith('api/'):
        return jsonify({'error': 'API endpoint not found'}), 404
    
    # 如果是靜態文件存在，返回該文件
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    
    # 否則返回 index.html (SPA 路由)
    return send_from_directory(app.static_folder, 'index.html')

# 你的 API 路由 (保持不變)
@app.route('/api/todos', methods=['GET'])
def get_todos():
    try:
        todos = Todo.query.all()
        return jsonify([todo.to_dict() for todo in todos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/todos', methods=['POST'])
def create_todo():
    try:
        data = request.get_json()
        
        if not data or 'title' not in data:
            return jsonify({'error': 'Title is required'}), 400
        
        new_todo = Todo(
            title=data['title'],
            description=data.get('description', ''),
            completed=False
        )
        db.session.add(new_todo)
        db.session.commit()
        return jsonify(new_todo.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    try:
        todo = Todo.query.get_or_404(todo_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        todo.title = data.get('title', todo.title)
        todo.description = data.get('description', todo.description)
        todo.completed = data.get('completed', todo.completed)
        
        db.session.commit()
        return jsonify(todo.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        todo = Todo.query.get_or_404(todo_id)
        db.session.delete(todo)
        db.session.commit()
        return jsonify({'message': 'Todo deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 錯誤處理 (保持不變)
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(host='0.0.0.0', port=port, debug=debug)