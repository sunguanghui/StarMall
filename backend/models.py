from datetime import datetime, date, timezone, timedelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


def get_beijing_time():
    """返回当前北京时间（无 tzinfo，兼容 MySQL DATETIME 列）"""
    return datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None)

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    real_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    avatar = db.Column(db.String(255), default=None)
    role = db.Column(db.Enum('admin', 'user'), default='user')
    is_super_admin = db.Column(db.Boolean, nullable=False, default=False)
    total_points = db.Column(db.Integer, default=0)
    available_points = db.Column(db.Integer, default=0)
    fragments = db.Column(db.JSON, default=lambda: {'engine': 0, 'radar': 0, 'hull': 0})
    ship_level = db.Column(db.Integer, default=1)
    streak_days = db.Column(db.Integer, default=0)
    last_active_date = db.Column(db.Date, nullable=True)
    is_child = db.Column(db.Boolean, nullable=False, default=False)
    # B-14: 存储图形密码的哈希值，不再明文存 JSON 序列
    child_pattern = db.Column(db.String(255), nullable=True, default=None)
    created_at = db.Column(db.DateTime, default=get_beijing_time)
    updated_at = db.Column(db.DateTime, default=get_beijing_time, onupdate=get_beijing_time)

    thumbs_records = db.relationship('ThumbsRecord', foreign_keys='ThumbsRecord.user_id', backref='user', lazy='dynamic')
    exchange_records = db.relationship('ExchangeRecord', backref='user', lazy='dynamic')
    wishlists = db.relationship('Wishlist', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_pattern(self, pattern):
        """接收 list[int]，序列化后哈希存储"""
        serialized = ','.join(str(n) for n in pattern)
        self.child_pattern = generate_password_hash(serialized)

    def check_pattern(self, pattern):
        """接收 list[int]，序列化后与哈希比对"""
        if not self.child_pattern:
            return False
        serialized = ','.join(str(n) for n in pattern)
        return check_password_hash(self.child_pattern, serialized)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'real_name': self.real_name,
            'email': self.email,
            'phone': self.phone,
            'avatar': self.avatar,
            'role': self.role,
            'is_super_admin': self.is_super_admin,
            'total_points': self.total_points,
            'available_points': self.available_points,
            'fragments': self.fragments or {'engine': 0, 'radar': 0, 'hull': 0},
            'ship_level': self.ship_level or 1,
            'streak_days': self.streak_days or 0,
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
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=get_beijing_time)

    giver = db.relationship('User', foreign_keys=[given_by])
    admin = db.relationship('User', foreign_keys=[admin_id])

    def to_dict(self):
        type_name_map = {
            'single': '单星辰币 ⭐',
            'double': '双星辰币 🚀',
            'deduction': '红牌警告 ⚠️'
        }
        admin_name = None
        if self.admin:
            admin_name = self.admin.real_name
        elif self.giver:
            admin_name = self.giver.real_name
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
            'admin_id': self.admin_id,
            'admin_name': admin_name,
            'is_deleted': self.is_deleted,
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
    created_at = db.Column(db.DateTime, default=get_beijing_time)
    updated_at = db.Column(db.DateTime, default=get_beijing_time, onupdate=get_beijing_time)

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
    created_at = db.Column(db.DateTime, default=get_beijing_time)
    updated_at = db.Column(db.DateTime, default=get_beijing_time, onupdate=get_beijing_time)

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
    created_at = db.Column(db.DateTime, default=get_beijing_time)
    updated_at = db.Column(db.DateTime, default=get_beijing_time, onupdate=get_beijing_time)

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


class Task(db.Model):
    """任务模板"""
    __tablename__ = 'tasks'

    id            = db.Column(db.Integer, primary_key=True)
    title         = db.Column(db.String(100), nullable=False)
    type          = db.Column(db.Enum('daily', 'milestone'), nullable=False, default='daily')
    energy_reward = db.Column(db.Integer, nullable=False, default=1)
    is_active     = db.Column(db.Boolean, nullable=False, default=True)
    reviewer_id   = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_by    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at    = db.Column(db.DateTime, default=get_beijing_time)
    updated_at    = db.Column(db.DateTime, default=get_beijing_time, onupdate=get_beijing_time)

    logs     = db.relationship('TaskLog', backref='task', lazy='dynamic')
    reviewer = db.relationship('User', foreign_keys=[reviewer_id])
    creator  = db.relationship('User', foreign_keys=[created_by])

    def to_dict(self):
        return {
            'id':              self.id,
            'title':           self.title,
            'type':            self.type,
            'type_name':       '每日日常' if self.type == 'daily' else '阶段里程碑',
            'energy_reward':   self.energy_reward,
            'is_active':       self.is_active,
            'reviewer_id':     self.reviewer_id,
            'reviewer_name':   self.reviewer.real_name if self.reviewer else None,
            'created_by':      self.created_by,
            'created_by_name': self.creator.real_name if self.creator else None,
            'created_at':      self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
        }


class TaskLog(db.Model):
    """任务执行记录"""
    __tablename__ = 'task_logs'

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    task_id    = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    status     = db.Column(db.Enum('pending', 'approved', 'rejected'), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=get_beijing_time)
    updated_at = db.Column(db.DateTime, default=get_beijing_time, onupdate=get_beijing_time)

    user = db.relationship('User', backref=db.backref('task_logs', lazy='dynamic'))

    def to_dict(self):
        status_map = {'pending': '待审核', 'approved': '已批准', 'rejected': '已驳回'}
        return {
            'id':               self.id,
            'user_id':          self.user_id,
            'user_name':        self.user.real_name if self.user else None,
            'task_id':          self.task_id,
            'task_title':       self.task.title if self.task else None,
            'task_type':        self.task.type if self.task else None,
            'energy_reward':    self.task.energy_reward if self.task else 0,
            'reviewer_id':      self.task.reviewer_id if self.task else None,
            'reviewer_name':    self.task.reviewer.real_name if self.task and self.task.reviewer else None,
            'status':           self.status,
            'status_name':      status_map.get(self.status, self.status),
            'created_at':       self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at':       self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
        }


class SystemSettings(db.Model):
    """系统设置模型（单行配置表）"""
    __tablename__ = 'system_settings'

    id = db.Column(db.Integer, primary_key=True)
    speaker_ip = db.Column(db.String(64), default='')
    speaker_port = db.Column(db.Integer, default=18888)
    heartbeat_interval = db.Column(db.Integer, default=10)
    enable_broadcast = db.Column(db.Boolean, default=False)
    enable_timed_broadcast = db.Column(db.Boolean, default=False)
    morning_broadcast_time = db.Column(db.String(5), default='07:00')
    evening_broadcast_time = db.Column(db.String(5), default='21:00')
    broadcast_targets = db.Column(db.JSON, default=list)
    updated_at = db.Column(db.DateTime, default=get_beijing_time, onupdate=get_beijing_time)

    def to_dict(self):
        return {
            'id': self.id,
            'speaker_ip': self.speaker_ip or '',
            'speaker_port': self.speaker_port or 18888,
            'heartbeat_interval': self.heartbeat_interval or 10,
            'enable_broadcast': self.enable_broadcast or False,
            'enable_timed_broadcast': self.enable_timed_broadcast or False,
            'morning_broadcast_time': self.morning_broadcast_time or '07:00',
            'evening_broadcast_time': self.evening_broadcast_time or '21:00',
            'broadcast_targets': self.broadcast_targets or [],
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
