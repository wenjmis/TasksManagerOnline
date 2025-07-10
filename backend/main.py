import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import Todo, db
from config import Config
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

app = Flask(__name__)

# 根據環境選擇配置
if os.environ.get('FLASK_ENV') == 'production':
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

# 設定 CORS
if os.environ.get('FLASK_ENV') == 'production':
    # 生產環境 - 只允許特定來源
    CORS(app, origins=[
        'https://taskmanagerVueWeb.vercel.app',  
        'https://*.vercel.app'  # 允許所有 vercel 子域名
    ])
else:
    # 開發環境 - 允許所有來源
    CORS(app)

# 初始化資料庫
db.init_app(app)

# Flask 2.2+ 不再支援 @app.before_first_request
# 使用 app.before_request 代替
@app.before_request
def create_tables():
    # 只在第一次請求時建立表格
    if not hasattr(create_tables, 'done'):
        with app.app_context():
            db.create_all()
        create_tables.done = True

# 健康檢查端點
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'API is running'}), 200

# API 路由
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
        
        # 驗證必要欄位
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

# 錯誤處理
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # 確保在應用程式上下文中建立表格
    with app.app_context():
        db.create_all()
    
    # 根據環境設定運行參數
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(host='0.0.0.0', port=port, debug=debug)