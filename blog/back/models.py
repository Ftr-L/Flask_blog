from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_name = db.Column(db.String(10), unique=True, nullable=False)
    u_password = db.Column(db.String(255), nullable=False)
    is_delete = db.Column(db.Boolean, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def save(self):
        db.session.add(self)
        db.session.commit()


# 分类表
class ArticleType(db.Model):
    __tablename__ = 'art_type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    t_name = db.Column(db.String(10), unique=True, nullable=False)
    arts = db.relationship('Article', backref='tp')


# 文章表
class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 文章名称
    title = db.Column(db.String(30), unique=True, nullable=False)
    # 文章描述
    desc = db.Column(db.String(100), nullable=False)
    # 文章内容
    content = db.Column(db.Text, nullable=False)
    # 创建文章时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    type = db.Column(db.Integer, db.ForeignKey('art_type.id'))

