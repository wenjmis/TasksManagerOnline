import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """基礎配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JSON 配置
    JSON_AS_ASCII = False
    JSONIFY_PRETTYPRINT_REGULAR = True

class DevelopmentConfig(Config):
    """開發環境配置"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///todos.db'
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    DEBUG = False
    # 生產環境必須使用 PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL environment variable is required for production")
    
    # 修正 Heroku/Render 的 postgres:// 前綴問題
    if SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)


class TestConfig(Config):
    """測試環境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig,
    'default': DevelopmentConfig
}