from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    real_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    role = db.Column(db.Enum('admin', 'user'), default='user')
    total_points = db.Column(db.Integer, default=0)
    available_points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    thumbs_records = db.relationship('ThumbsRecord', foreign_keys='ThumbsRecord.user_id', backref='user', lazy='dynamic')
    exchange_records = db.relationship('ExchangeRecord', backref='user', lazy='dynamic')
    wishlists = db.relationship('Wishlist', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'real_name': self.real_name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'total_points': self.total_points,
            'available_points': self.available_points,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }


class ThumbsRecord(db.Model):
    """星辰币记录模型"""
    __tablename__ = 'thumbs_records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    thumb_type = db.Column(db.Enum('single', 'double', 'deduction'), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(255))
    parent_message = db.Column(db.Text)
    given_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    giver = db.relationship('User', foreign_keys=[given_by])

    def to_dict(self):
        type_name_map = {
            'single': '单星辰币 ⭐',
            'double': '双星辰币 🚀',
            'deduction': '红牌警告 ⚠️'
        }
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.real_name if self.user else None,
            'thumb_type': self.thumb_type,
            'thumb_type_name': type_name_map.get(self.thumb_type, self.thumb_type),
            'points': self.points,
            'reason': self.reason,
            'parent_message': self.parent_message,
            'given_by': self.given_by,
            'given_by_name': self.giver.real_name if self.giver else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }


class Product(db.Model):
    """商品模型"""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    points_required = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, default=0)
    status = db.Column(db.Enum('on_shelf', 'off_shelf'), default='off_shelf')
    sort_order = db.Column(db.Integer, default=0)
    is_blind_box = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    exchange_records = db.relationship('ExchangeRecord', backref='product', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image_url': self.image_url,
            'points_required': self.points_required,
            'stock': self.stock,
            'status': self.status,
            'status_name': '已上架' if self.status == 'on_shelf' else '已下架',
            'sort_order': self.sort_order,
            'is_blind_box': self.is_blind_box or False,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }


class ExchangeRecord(db.Model):
    """兑换记录模型"""
    __tablename__ = 'exchange_records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    points_spent = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    status = db.Column(db.Enum('pending', 'completed', 'cancelled'), default='pending')
    remark = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.real_name if self.user else None,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'points_spent': self.points_spent,
            'quantity': self.quantity,
            'status': self.status,
            'status_name': {'pending': '待处理', 'completed': '已完成', 'cancelled': '已取消'}.get(self.status),
            'remark': self.remark,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }


class Wishlist(db.Model):
    """星际心愿单模型"""
    __tablename__ = 'wishlists'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    expected_points = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.Enum('pending', 'approved', 'rejected'), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        status_name_map = {'pending': '待审核', 'approved': '已批准', 'rejected': '已拒绝'}
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.real_name if self.user else None,
            'title': self.title,
            'expected_points': self.expected_points,
            'status': self.status,
            'status_name': status_name_map.get(self.status, self.status),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
