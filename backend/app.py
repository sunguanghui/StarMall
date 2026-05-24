from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import os
import uuid
import subprocess
import glob as glob_module
from config import Config
import random
from models import db, User, ThumbsRecord, Product, ExchangeRecord, Wishlist, Task, TaskLog, SystemSettings
from speaker_client import speaker_client

# 盲盒奖池（可自定义扩展）
BLIND_BOX_PRIZES = [
    '神秘贴纸一套',
    '小零食大礼包',
    '定制书签',
    '荧光笔套装',
    '可爱橡皮擦',
    '星际主题笔记本',
    '迷你积木玩具',
]

app = Flask(__name__)
app.config.from_object(Config)

# 初始化扩展
CORS(app)
db.init_app(app)
jwt = JWTManager(app)

# 创建备份目录
BACKUP_DIR = app.config.get('BACKUP_DIR', os.path.join(os.path.dirname(__file__), 'backups'))
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# 创建上传目录
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ==================== 播报文案引擎 ====================

def _build_instant_broadcast_text(admin_name, admin_role, target_name, reason, amount, total):
    """构建即时发分播报文案（随机拼接）"""
    openers = [
        '叮咚！星际广播开启！',
        '哇哦！收到来自舰队指挥中心的最新战报！',
    ]
    events = [
        f'报告小宇航员 {target_name}！因为你{reason}，{admin_role} {admin_name} 亲自为你注入了 {amount} 个星辰币！',
        f'太棒啦！小宇航员 {target_name} 顺利完成{reason}，{admin_role} {admin_name} 奖励了 {amount} 个星辰币！',
    ]
    endings = [
        f'现在的总能量已经达到 {total} 啦，继续向宇宙深处出发吧！',
    ]
    return random.choice(openers) + random.choice(events) + random.choice(endings)


def _build_timed_broadcast_text(target_name, total, period, wish_name=None, energy_diff=None):
    """构建定时简报文案（含可选心愿追踪）"""
    if period == 'morning':
        base = (
            f'早上好，小宇航员 {target_name}！新一天的星际航行开始啦！'
            f'目前飞船总能量为 {total} 个星辰币。'
            f'昨天的表现非常棒，今天也要继续加油巡航哦！'
        )
    else:
        base = (
            f'夜幕降临，空间站广播开启。小宇航员 {target_name}，今天的航行辛苦啦！'
            f'目前总能量为 {total} 个星辰币。'
            f'快快开启睡眠舱模式，恢复体力，明天见！'
        )
    if wish_name and energy_diff is not None:
        wish_phrases = [
            f'星际雷达提示，距离你的心愿目标【{wish_name}】，只差最后 {energy_diff} 个星辰币啦，一鼓作气拿下它吧！',
            f'悄悄告诉你，再积攒 {energy_diff} 个星辰币，就能成功解锁【{wish_name}】了哦，继续努力！',
        ]
        base += random.choice(wish_phrases)
    return base


def _get_closest_wish(user):
    """查询目标能量大于当前能量且差值最小的 pending 心愿"""
    wish = (
        Wishlist.query
        .filter(
            Wishlist.user_id == user.id,
            Wishlist.status == 'pending',
            Wishlist.expected_points > user.available_points
        )
        .order_by((Wishlist.expected_points - user.available_points).asc())
        .first()
    )
    if wish:
        return wish.title, wish.expected_points - user.available_points
    return None, None


def _get_settings():
    """获取系统设置（若无则返回 None）"""
    return SystemSettings.query.first()


def _try_instant_broadcast(target_user, admin_user, reason, amount):
    """即时播报入口，失败静默"""
    try:
        settings = _get_settings()
        if not settings or not settings.enable_broadcast:
            return
        if not settings.speaker_ip:
            return
        admin_role = '舰长' if admin_user.is_super_admin else '领航员'
        text = _build_instant_broadcast_text(
            admin_name=admin_user.real_name,
            admin_role=admin_role,
            target_name=target_user.real_name,
            reason=reason,
            amount=amount,
            total=target_user.available_points
        )
        speaker_client.send_text(text)
    except Exception:
        pass


# ==================== 文件上传 API ====================

@app.route('/api/upload', methods=['POST'])
@jwt_required()
def upload_file():
    """上传文件"""
    if 'file' not in request.files:
        return jsonify({'code': 400, 'message': '没有文件'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'code': 400, 'message': '没有选择文件'}), 400

    if file and allowed_file(file.filename):
        # 生成唯一文件名
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        # 保存文件
        file.save(filepath)

        # 返回文件URL
        file_url = f"/api/uploads/{filename}"

        return jsonify({
            'code': 200,
            'message': '上传成功',
            'data': {
                'url': file_url,
                'filename': filename
            }
        })

    return jsonify({'code': 400, 'message': '不支持的文件类型'}), 400


@app.route('/api/uploads/<filename>')
def get_upload_file(filename):
    """获取上传的文件"""
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/api/upload/avatar', methods=['POST'])
@jwt_required()
def upload_avatar():
    """上传头像图片"""
    if 'file' not in request.files:
        return jsonify({'code': 400, 'message': '没有文件'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'code': 400, 'message': '没有选择文件'}), 400

    if file and allowed_file(file.filename):
        avatar_folder = os.path.join(UPLOAD_FOLDER, 'avatars')
        if not os.path.exists(avatar_folder):
            os.makedirs(avatar_folder)

        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(avatar_folder, filename)
        file.save(filepath)

        file_url = f"/api/uploads/avatars/{filename}"
        return jsonify({'code': 200, 'message': '上传成功', 'data': {'url': file_url}})

    return jsonify({'code': 400, 'message': '不支持的文件类型'}), 400


@app.route('/api/uploads/avatars/<filename>')
def get_avatar_file(filename):
    """获取头像文件"""
    avatar_folder = os.path.join(UPLOAD_FOLDER, 'avatars')
    return send_from_directory(avatar_folder, filename)


@app.route('/api/auth/avatar', methods=['POST'])
@jwt_required()
def update_avatar():
    """更新当前用户头像"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404

    data = request.get_json()
    avatar = data.get('avatar')
    if not avatar:
        return jsonify({'code': 400, 'message': '头像不能为空'}), 400

    user.avatar = avatar
    db.session.commit()

    return jsonify({'code': 200, 'message': '头像更新成功', 'data': user.to_dict()})


# ==================== 认证相关 API ====================

@app.route('/api/auth/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'code': 400, 'message': '用户名和密码不能为空'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'code': 401, 'message': '用户名或密码错误'}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        'code': 200,
        'message': '登录成功',
        'data': {
            'token': access_token,
            'user': user.to_dict()
        }
    })


@app.route('/api/auth/info', methods=['GET'])
@jwt_required()
def get_user_info():
    """获取当前用户信息"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404

    return jsonify({
        'code': 200,
        'data': user.to_dict()
    })


@app.route('/api/auth/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """修改当前用户密码"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404

    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not old_password or not new_password:
        return jsonify({'code': 400, 'message': '旧密码和新密码不能为空'}), 400

    # 验证旧密码
    if not user.check_password(old_password):
        return jsonify({'code': 400, 'message': '旧密码错误'}), 400

    # 设置新密码
    user.set_password(new_password)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '密码修改成功'
    })


@app.route('/api/auth/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    real_name = data.get('real_name')
    email = data.get('email')
    phone = data.get('phone')

    if not username or not password or not real_name:
        return jsonify({'code': 400, 'message': '用户名、密码和姓名不能为空'}), 400

    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({'code': 400, 'message': '用户名已存在'}), 400

    # 创建新用户
    user = User(
        username=username,
        real_name=real_name,
        email=email,
        phone=phone,
        role='user',
        total_points=0,
        available_points=0
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '注册成功',
        'data': user.to_dict()
    })


# ==================== 用户管理 API ====================

@app.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
    """获取用户列表（仅管理员）"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin':
        return jsonify({'code': 403, 'message': '无权限'}), 403

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    keyword = request.args.get('keyword', '')
    role_filter = request.args.get('role', '')

    query = User.query
    if keyword:
        query = query.filter(
            db.or_(
                User.username.like(f'%{keyword}%'),
                User.real_name.like(f'%{keyword}%')
            )
        )
    if role_filter:
        query = query.filter_by(role=role_filter)

    pagination = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'code': 200,
        'data': {
            'list': [user.to_dict() for user in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }
    })


@app.route('/api/users', methods=['POST'])
@jwt_required()
def create_user():
    """创建用户"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'code': 403, 'message': '无权限操作'}), 403

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    real_name = data.get('real_name')

    if not username or not password or not real_name:
        return jsonify({'code': 400, 'message': '必填字段不能为空'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'code': 400, 'message': '用户名已存在'}), 400

    user = User(
        username=username,
        real_name=real_name,
        email=data.get('email'),
        phone=data.get('phone'),
        role=data.get('role', 'user'),
        is_super_admin=data.get('is_super_admin', False) if current_user.is_super_admin else False
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '创建成功',
        'data': user.to_dict()
    })


@app.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """更新用户信息"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    # 只能修改自己的信息或管理员可以修改所有人
    if current_user.role != 'admin' and current_user_id != user_id:
        return jsonify({'code': 403, 'message': '无权限操作'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404

    data = request.get_json()

    if 'real_name' in data:
        user.real_name = data['real_name']
    if 'email' in data:
        user.email = data['email']
    if 'phone' in data:
        user.phone = data['phone']
    if 'avatar' in data:
        user.avatar = data['avatar']
    if 'password' in data and data['password']:
        user.set_password(data['password'])
    # 只有超级管理员可以修改 is_super_admin
    if 'is_super_admin' in data and current_user.is_super_admin:
        user.is_super_admin = data['is_super_admin']

    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '更新成功',
        'data': user.to_dict()
    })


@app.route('/api/users/<int:user_id>/reset-password', methods=['POST'])
@jwt_required()
def reset_user_password(user_id):
    """管理员重置用户密码"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    # 只有管理员可以重置密码
    if current_user.role != 'admin':
        return jsonify({'code': 403, 'message': '无权限操作'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404

    data = request.get_json()
    new_password = data.get('new_password')

    if not new_password:
        return jsonify({'code': 400, 'message': '新密码不能为空'}), 400

    # 设置新密码
    user.set_password(new_password)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '密码重置成功'
    })


# ==================== 星辰币管理 API ====================

@app.route('/api/thumbs', methods=['POST'])
@jwt_required()
def give_thumbs():
    """发放星辰币 / 扣除能量"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'code': 403, 'message': '只有管理员可以操作'}), 403

    data = request.get_json()
    user_id = data.get('user_id')
    thumb_type = data.get('thumb_type')  # 'single', 'double', 'deduction'
    reason = data.get('reason', '')
    parent_message = data.get('parent_message', '')

    if not user_id or not thumb_type:
        return jsonify({'code': 400, 'message': '参数不完整'}), 400

    if thumb_type not in ['single', 'double', 'deduction']:
        return jsonify({'code': 400, 'message': '奖励类型错误'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404

    # 计算能量值
    if thumb_type == 'single':
        points = 1
    elif thumb_type == 'double':
        points = 5
    else:  # deduction：允许前端传入自定义负整数
        custom_points = data.get('points')
        if custom_points is not None:
            if not isinstance(custom_points, int) or custom_points >= 0:
                return jsonify({'code': 400, 'message': '自定义扣分值必须为负整数'}), 400
            points = custom_points
        else:
            points = -1

    # 扣分时：扣到 0 为止，不拒绝操作
    if points < 0:
        actual_deduction = max(points, -user.available_points)
        user.available_points = max(0, user.available_points + points)
        user.total_points += actual_deduction
    else:
        user.total_points += points
        user.available_points += points

    record = ThumbsRecord(
        user_id=user_id,
        thumb_type=thumb_type,
        points=points,
        reason=reason,
        parent_message=parent_message if parent_message else None,
        given_by=current_user_id,
        admin_id=current_user_id
    )

    db.session.add(record)
    db.session.commit()

    # 即时播报（仅正向发分）
    if points > 0:
        _try_instant_broadcast(
            target_user=user,
            admin_user=current_user,
            reason=reason or '表现出色',
            amount=points
        )

    type_label = {'single': '单星辰币', 'double': '双星辰币', 'deduction': '红牌警告'}
    return jsonify({
        'code': 200,
        'message': f'已发放{type_label[thumb_type]}',
        'data': record.to_dict()
    })


@app.route('/api/thumbs', methods=['GET'])
@jwt_required()
def get_thumbs_records():
    """获取星辰币记录"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    user_id = request.args.get('user_id', type=int)
    given_by = request.args.get('given_by', type=int)

    query = ThumbsRecord.query.filter_by(is_deleted=False)

    if current_user.role != 'admin':
        # 普通用户只能看自己收到的记录
        query = query.filter_by(user_id=current_user_id)
    else:
        # 管理员可按 user_id 或 given_by 过滤
        if user_id:
            query = query.filter_by(user_id=user_id)
        if given_by:
            query = query.filter_by(given_by=given_by)

    pagination = query.order_by(ThumbsRecord.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'code': 200,
        'data': {
            'list': [record.to_dict() for record in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }
    })


@app.route('/api/thumbs/stats', methods=['GET'])
@jwt_required()
def get_thumbs_stats():
    """获取星辰币统计"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    requested_user_id = request.args.get('user_id', type=int)

    # 普通用户只能查自己；管理员可指定 user_id，不指定则查自己
    if current_user.role != 'admin':
        user_id = current_user_id
    else:
        user_id = requested_user_id if requested_user_id else current_user_id

    user = User.query.get(user_id)
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404

    # 统计单双星辰币数量
    single_count = ThumbsRecord.query.filter_by(user_id=user_id, thumb_type='single').count()
    double_count = ThumbsRecord.query.filter_by(user_id=user_id, thumb_type='double').count()

    return jsonify({
        'code': 200,
        'data': {
            'user_id': user_id,
            'user_name': user.real_name,
            'total_points': user.total_points,
            'available_points': user.available_points,
            'used_points': user.total_points - user.available_points,
            'single_thumbs': single_count,
            'double_thumbs': double_count,
            'total_thumbs': single_count + double_count
        }
    })


# ==================== 商品管理 API ====================

@app.route('/api/products', methods=['GET'])
def get_products():
    """获取商品列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')  # 'on_shelf' or 'off_shelf'
    keyword = request.args.get('keyword', '')

    query = Product.query

    # 如果指定了状态则过滤
    if status:
        query = query.filter_by(status=status)

    # 关键词搜索
    if keyword:
        query = query.filter(Product.name.like(f'%{keyword}%'))

    pagination = query.order_by(Product.sort_order.asc(), Product.id.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'code': 200,
        'data': {
            'list': [product.to_dict() for product in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }
    })


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """获取商品详情"""
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'code': 404, 'message': '商品不存在'}), 404

    return jsonify({
        'code': 200,
        'data': product.to_dict()
    })


@app.route('/api/products', methods=['POST'])
@jwt_required()
def create_product():
    """创建商品"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'code': 403, 'message': '无权限操作'}), 403

    data = request.get_json()
    name = data.get('name')
    points_required = data.get('points_required')

    if not name or not points_required:
        return jsonify({'code': 400, 'message': '商品名称和积分不能为空'}), 400

    product = Product(
        name=name,
        description=data.get('description'),
        image_url=data.get('image_url'),
        points_required=points_required,
        stock=data.get('stock', 0),
        status=data.get('status', 'off_shelf'),
        sort_order=data.get('sort_order', 0),
        is_blind_box=data.get('is_blind_box', False)
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '创建成功',
        'data': product.to_dict()
    })


@app.route('/api/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    """更新商品信息"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'code': 403, 'message': '无权限操作'}), 403

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'code': 404, 'message': '商品不存在'}), 404

    data = request.get_json()

    if 'name' in data:
        product.name = data['name']
    if 'description' in data:
        product.description = data['description']
    if 'image_url' in data:
        product.image_url = data['image_url']
    if 'points_required' in data:
        product.points_required = data['points_required']
    if 'stock' in data:
        product.stock = data['stock']
    if 'status' in data:
        product.status = data['status']
    if 'sort_order' in data:
        product.sort_order = data['sort_order']
    if 'is_blind_box' in data:
        product.is_blind_box = data['is_blind_box']

    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '更新成功',
        'data': product.to_dict()
    })


@app.route('/api/products/<int:product_id>/toggle-status', methods=['POST'])
@jwt_required()
def toggle_product_status(product_id):
    """切换商品上下架状态"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'code': 403, 'message': '无权限操作'}), 403

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'code': 404, 'message': '商品不存在'}), 404

    # 切换状态
    product.status = 'off_shelf' if product.status == 'on_shelf' else 'on_shelf'
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': f'商品已{"上架" if product.status == "on_shelf" else "下架"}',
        'data': product.to_dict()
    })


@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    """删除商品"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'code': 403, 'message': '无权限操作'}), 403

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'code': 404, 'message': '商品不存在'}), 404

    # 检查是否有兑换记录
    if ExchangeRecord.query.filter_by(product_id=product_id).first():
        return jsonify({'code': 400, 'message': '该商品有兑换记录，不能删除'}), 400

    db.session.delete(product)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '删除成功'
    })


# ==================== 兑换管理 API ====================

@app.route('/api/exchanges', methods=['POST'])
@jwt_required()
def create_exchange():
    """创建兑换记录"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if not product_id:
        return jsonify({'code': 400, 'message': '商品ID不能为空'}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'code': 404, 'message': '商品不存在'}), 404

    if product.status != 'on_shelf':
        return jsonify({'code': 400, 'message': '商品已下架，无法兑换'}), 400

    if product.stock < quantity:
        return jsonify({'code': 400, 'message': '商品库存不足'}), 400

    points_needed = product.points_required * quantity
    if user.available_points < points_needed:
        return jsonify({'code': 400, 'message': '积分不足'}), 400

    # 创建兑换记录（盲盒随机抽奖）
    blind_box_result = None
    if product.is_blind_box:
        blind_box_result = random.choice(BLIND_BOX_PRIZES)

    record = ExchangeRecord(
        user_id=current_user_id,
        product_id=product_id,
        product_name=product.name,
        points_spent=points_needed,
        quantity=quantity,
        status='completed',
        remark=f'盲盒抽奖结果：{blind_box_result}' if blind_box_result else None
    )

    # 扣除积分和库存
    user.available_points -= points_needed
    product.stock -= quantity

    db.session.add(record)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': f'兑换成功！获得：{blind_box_result}' if blind_box_result else '兑换成功',
        'data': record.to_dict()
    })


@app.route('/api/exchanges', methods=['GET'])
@jwt_required()
def get_exchanges():
    """获取兑换记录"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    user_id = request.args.get('user_id', type=int)
    status = request.args.get('status')

    query = ExchangeRecord.query

    # 普通用户只能查看自己的记录
    if current_user.role != 'admin':
        query = query.filter_by(user_id=current_user_id)
    elif user_id:
        query = query.filter_by(user_id=user_id)

    if status:
        query = query.filter_by(status=status)

    pagination = query.order_by(ExchangeRecord.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'code': 200,
        'data': {
            'list': [record.to_dict() for record in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }
    })


@app.route('/api/exchanges/<int:record_id>/complete', methods=['POST'])
@jwt_required()
def complete_exchange(record_id):
    """确认交付（将 pending 兑换标记为 completed）"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin':
        return jsonify({'code': 403, 'message': '无权限操作'}), 403

    record = ExchangeRecord.query.get(record_id)
    if not record:
        return jsonify({'code': 404, 'message': '兑换记录不存在'}), 404
    if record.status != 'pending':
        return jsonify({'code': 400, 'message': '只能确认待处理的兑换'}), 400

    record.status = 'completed'
    db.session.commit()
    return jsonify({'code': 200, 'message': '已确认交付', 'data': record.to_dict()})


@app.route('/api/exchanges/<int:record_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_exchange(record_id):
    """取消兑换（退回积分和库存）"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    record = ExchangeRecord.query.get(record_id)
    if not record:
        return jsonify({'code': 404, 'message': '兑换记录不存在'}), 404

    # 只有管理员或本人可以取消
    if current_user.role != 'admin' and record.user_id != current_user_id:
        return jsonify({'code': 403, 'message': '无权限操作'}), 403

    if record.status != 'completed':
        return jsonify({'code': 400, 'message': '只能取消已完成的兑换'}), 400

    # 退回积分
    user = User.query.get(record.user_id)
    user.available_points += record.points_spent

    # 退回库存
    product = Product.query.get(record.product_id)
    if product:
        product.stock += record.quantity

    record.status = 'cancelled'
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '兑换已取消，积分已退回',
        'data': record.to_dict()
    })


# ==================== 统计 API ====================

@app.route('/api/stats/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """获取仪表板统计数据"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role == 'admin':
        # 管理员看全局统计
        total_users = User.query.filter_by(role='user').count()
        total_thumbs = ThumbsRecord.query.count()
        total_exchanges = ExchangeRecord.query.filter_by(status='completed').count()
        total_products = Product.query.filter_by(status='on_shelf').count()

        return jsonify({
            'code': 200,
            'data': {
                'total_users': total_users,
                'total_thumbs': total_thumbs,
                'total_exchanges': total_exchanges,
                'total_products': total_products
            }
        })
    else:
        # 普通用户看个人统计
        return jsonify({
            'code': 200,
            'data': {
                'total_points': current_user.total_points,
                'available_points': current_user.available_points,
                'used_points': current_user.total_points - current_user.available_points,
                'total_thumbs': ThumbsRecord.query.filter_by(user_id=current_user_id).count(),
                'total_exchanges': ExchangeRecord.query.filter_by(user_id=current_user_id, status='completed').count(),
                'fragments': current_user.fragments or {'engine': 0, 'radar': 0, 'hull': 0},
                'ship_level': current_user.ship_level or 1,
                'streak_days': current_user.streak_days or 0,
            }
        })


# ==================== 心愿单 API ====================

@app.route('/api/wishlists', methods=['GET'])
@jwt_required()
def get_wishlists():
    """获取心愿单列表"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')

    query = Wishlist.query
    if current_user.role != 'admin':
        query = query.filter_by(user_id=current_user_id)
    if status:
        query = query.filter_by(status=status)

    pagination = query.order_by(Wishlist.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'code': 200,
        'data': {
            'list': [w.to_dict() for w in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }
    })


@app.route('/api/wishlists', methods=['POST'])
@jwt_required()
def create_wishlist():
    """提交心愿单"""
    current_user_id = get_jwt_identity()

    data = request.get_json()
    title = data.get('title', '').strip()
    expected_points = data.get('expected_points', 0)

    if not title:
        return jsonify({'code': 400, 'message': '心愿名称不能为空'}), 400
    if not isinstance(expected_points, int) or expected_points < 0:
        return jsonify({'code': 400, 'message': '期望能量值无效'}), 400

    wishlist = Wishlist(
        user_id=current_user_id,
        title=title,
        expected_points=expected_points
    )
    db.session.add(wishlist)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '心愿提交成功，等待舰长审核',
        'data': wishlist.to_dict()
    })


@app.route('/api/wishlists/<int:wishlist_id>/approve', methods=['POST'])
@jwt_required()
def approve_wishlist(wishlist_id):
    """管理员批准心愿，自动创建商品"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'code': 403, 'message': '无权限操作'}), 403

    wishlist = Wishlist.query.get(wishlist_id)
    if not wishlist:
        return jsonify({'code': 404, 'message': '心愿不存在'}), 404
    if wishlist.status != 'pending':
        return jsonify({'code': 400, 'message': '该心愿已处理'}), 400

    # 自动写入商品表（下架状态，待管理员手动上架）
    product = Product(
        name=wishlist.title,
        description=f'来自 {wishlist.user.real_name} 的星际心愿',
        points_required=wishlist.expected_points,
        stock=1,
        status='off_shelf',
        sort_order=0,
        is_blind_box=False
    )
    wishlist.status = 'approved'

    db.session.add(product)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '心愿已批准，商品已创建（当前为下架状态，请前往商品管理上架）',
        'data': wishlist.to_dict()
    })


@app.route('/api/wishlists/<int:wishlist_id>/reject', methods=['POST'])
@jwt_required()
def reject_wishlist(wishlist_id):
    """管理员拒绝心愿"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != 'admin':
        return jsonify({'code': 403, 'message': '无权限操作'}), 403

    wishlist = Wishlist.query.get(wishlist_id)
    if not wishlist:
        return jsonify({'code': 404, 'message': '心愿不存在'}), 404
    if wishlist.status != 'pending':
        return jsonify({'code': 400, 'message': '该心愿已处理'}), 400

    wishlist.status = 'rejected'
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '已拒绝该心愿',
        'data': wishlist.to_dict()
    })


# ==================== 任务大厅 API ====================

@app.route('/api/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    """获取任务列表（附带今日提交状态）"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    include_inactive = request.args.get('include_inactive', 'false') == 'true'

    query = Task.query
    if not include_inactive:
        query = query.filter_by(is_active=True)

    # 普通管理员只能看自己创建的任务
    if current_user.role == 'admin' and not current_user.is_super_admin:
        query = query.filter_by(created_by=current_user_id)

    tasks = query.order_by(Task.type.asc(), Task.id.asc()).all()

    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)

    result = []
    for task in tasks:
        d = task.to_dict()
        today_log = TaskLog.query.filter(
            TaskLog.user_id == current_user_id,
            TaskLog.task_id == task.id,
            TaskLog.created_at >= today_start,
            TaskLog.created_at <= today_end
        ).first()
        d['today_log'] = today_log.to_dict() if today_log else None
        result.append(d)

    return jsonify({'code': 200, 'data': result})


@app.route('/api/admins', methods=['GET'])
@jwt_required()
def get_admins():
    """获取管理员列表（用于前端选择审批人）"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin':
        return jsonify({'code': 403, 'message': '无权限'}), 403

    admins = User.query.filter_by(role='admin').order_by(User.id.asc()).all()
    return jsonify({'code': 200, 'data': [{'id': u.id, 'real_name': u.real_name, 'is_super_admin': u.is_super_admin} for u in admins]})


@app.route('/api/tasks', methods=['POST'])
@jwt_required()
def create_task():
    """管理员创建任务"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin':
        return jsonify({'code': 403, 'message': '无权限操作'}), 403

    data = request.get_json()
    title = data.get('title', '').strip()
    if not title:
        return jsonify({'code': 400, 'message': '任务名称不能为空'}), 400

    if current_user.is_super_admin:
        reviewer_id = data.get('reviewer_id') or None
        created_by = current_user_id
    else:
        # 普通管理员强制自己为创建者和审批人
        reviewer_id = current_user_id
        created_by = current_user_id

    task = Task(
        title=title,
        type=data.get('type', 'daily'),
        energy_reward=data.get('energy_reward', 1),
        is_active=data.get('is_active', True),
        reviewer_id=reviewer_id,
        created_by=created_by
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({'code': 200, 'message': '创建成功', 'data': task.to_dict()})


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """管理员编辑任务"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin':
        return jsonify({'code': 403, 'message': '无权限操作'}), 403

    task = Task.query.get(task_id)
    if not task:
        return jsonify({'code': 404, 'message': '任务不存在'}), 404

    # 普通管理员只能编辑自己创建的任务
    if not current_user.is_super_admin and task.created_by != int(current_user_id):
        return jsonify({'code': 403, 'message': '只能编辑自己创建的任务'}), 403

    data = request.get_json()
    if 'title' in data:
        task.title = data['title'].strip()
    if 'type' in data:
        task.type = data['type']
    if 'energy_reward' in data:
        task.energy_reward = data['energy_reward']
    if 'is_active' in data:
        task.is_active = data['is_active']
    if 'reviewer_id' in data and current_user.is_super_admin:
        task.reviewer_id = data['reviewer_id'] or None

    db.session.commit()
    return jsonify({'code': 200, 'message': '更新成功', 'data': task.to_dict()})


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """管理员删除/停用任务"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin':
        return jsonify({'code': 403, 'message': '无权限操作'}), 403

    task = Task.query.get(task_id)
    if not task:
        return jsonify({'code': 404, 'message': '任务不存在'}), 404

    # 普通管理员只能停用自己创建的任务
    if not current_user.is_super_admin and task.created_by != int(current_user_id):
        return jsonify({'code': 403, 'message': '只能停用自己创建的任务'}), 403

    task.is_active = False
    db.session.commit()
    return jsonify({'code': 200, 'message': '任务已停用'})


@app.route('/api/task-logs', methods=['POST'])
@jwt_required()
def submit_task_log():
    """用户提交任务打卡"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    task_id = data.get('task_id')

    if not task_id:
        return jsonify({'code': 400, 'message': '任务ID不能为空'}), 400

    task = Task.query.get(task_id)
    if not task or not task.is_active:
        return jsonify({'code': 404, 'message': '任务不存在或已停用'}), 404

    # daily 任务每天只能提交一次
    if task.type == 'daily':
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        existing = TaskLog.query.filter(
            TaskLog.user_id == current_user_id,
            TaskLog.task_id == task_id,
            TaskLog.created_at >= today_start,
            TaskLog.created_at <= today_end
        ).first()
        if existing:
            return jsonify({'code': 400, 'message': '今天已提交过该任务，明天再来吧'}), 400

    log = TaskLog(user_id=current_user_id, task_id=task_id, status='pending')
    db.session.add(log)
    db.session.commit()
    return jsonify({'code': 200, 'message': '打卡成功，等待舰长审核', 'data': log.to_dict()})


@app.route('/api/task-logs', methods=['GET'])
@jwt_required()
def get_task_logs():
    """获取任务打卡记录"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    user_id = request.args.get('user_id', type=int)

    query = TaskLog.query
    if current_user.role != 'admin':
        query = query.filter_by(user_id=current_user_id)
    else:
        if not current_user.is_super_admin:
            # 普通管理员只看 reviewer_id=自己 或 reviewer_id=NULL 的任务打卡
            query = query.join(Task, TaskLog.task_id == Task.id).filter(
                db.or_(Task.reviewer_id == int(current_user_id), Task.reviewer_id == None)
            )
        if user_id:
            query = query.filter(TaskLog.user_id == user_id)

    if status:
        query = query.filter(TaskLog.status == status)

    pagination = query.order_by(TaskLog.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return jsonify({
        'code': 200,
        'data': {
            'list': [log.to_dict() for log in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }
    })


@app.route('/api/task-logs/<int:log_id>/approve', methods=['POST'])
@jwt_required()
def approve_task_log(log_id):
    """管理员审批通过，自动发放能量"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin':
        return jsonify({'code': 403, 'message': '无权限操作'}), 403

    log = TaskLog.query.get(log_id)
    if not log:
        return jsonify({'code': 404, 'message': '记录不存在'}), 404
    if log.status != 'pending':
        return jsonify({'code': 400, 'message': '该记录已处理'}), 400

    task = Task.query.get(log.task_id)
    # 普通管理员只能审批自己负责的任务
    if not current_user.is_super_admin:
        if task.reviewer_id is not None and task.reviewer_id != int(current_user_id):
            return jsonify({'code': 403, 'message': '该任务不在您的审批范围内'}), 403

    user = User.query.get(log.user_id)

    log.status = 'approved'
    user.total_points += task.energy_reward
    user.available_points += task.energy_reward

    # 连击追踪
    today = datetime.utcnow().date()
    if user.last_active_date == today:
        pass  # 同一天多次完成任务，不重复计算连击
    elif user.last_active_date == today - timedelta(days=1):
        user.streak_days = (user.streak_days or 0) + 1
    else:
        user.streak_days = 1
    user.last_active_date = today

    # 7天连击奖励：星云爆发 +10 能量
    streak_bonus = 0
    if user.streak_days > 0 and user.streak_days % 7 == 0:
        streak_bonus = 10
        user.total_points += streak_bonus
        user.available_points += streak_bonus
        bonus_record = ThumbsRecord(
            user_id=log.user_id,
            thumb_type='double',
            points=streak_bonus,
            reason=f'星云爆发！连续完成任务 {user.streak_days} 天',
            given_by=current_user_id,
            admin_id=current_user_id
        )
        db.session.add(bonus_record)

    # 30%概率掉落飞船碎片
    fragment_drop = None
    if random.random() < 0.3:
        parts = ['engine', 'radar', 'hull']
        fragment_drop = random.choice(parts)
        frags = user.fragments or {'engine': 0, 'radar': 0, 'hull': 0}
        frags[fragment_drop] = frags.get(fragment_drop, 0) + 1
        user.fragments = frags

    thumb_record = ThumbsRecord(
        user_id=log.user_id,
        thumb_type='single' if task.energy_reward <= 1 else 'double',
        points=task.energy_reward,
        reason=f'完成任务：{task.title}',
        given_by=current_user_id,
        admin_id=current_user_id
    )
    db.session.add(thumb_record)
    db.session.commit()

    # 即时播报
    _try_instant_broadcast(
        target_user=user,
        admin_user=current_user,
        reason=f'完成任务：{task.title}',
        amount=task.energy_reward
    )

    msg = f'已批准，已发放 {task.energy_reward} 点能量'
    if streak_bonus:
        msg += f'，星云爆发额外奖励 {streak_bonus} 点'
    if fragment_drop:
        names = {'engine': '引擎碎片', 'radar': '雷达碎片', 'hull': '船体碎片'}
        msg += f'，掉落了「{names[fragment_drop]}」'
    return jsonify({'code': 200, 'message': msg, 'data': log.to_dict()})


@app.route('/api/task-logs/<int:log_id>/reject', methods=['POST'])
@jwt_required()
def reject_task_log(log_id):
    """管理员驳回打卡"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin':
        return jsonify({'code': 403, 'message': '无权限操作'}), 403

    log = TaskLog.query.get(log_id)
    if not log:
        return jsonify({'code': 404, 'message': '记录不存在'}), 404
    if log.status != 'pending':
        return jsonify({'code': 400, 'message': '该记录已处理'}), 400

    task = Task.query.get(log.task_id)
    if not current_user.is_super_admin:
        if task.reviewer_id is not None and task.reviewer_id != int(current_user_id):
            return jsonify({'code': 403, 'message': '该任务不在您的审批范围内'}), 403

    log.status = 'rejected'
    db.session.commit()
    return jsonify({'code': 200, 'message': '已驳回', 'data': log.to_dict()})


# ==================== 后悔药撤销 API ====================

@app.route('/api/thumbs/<int:record_id>/undo', methods=['POST'])
@jwt_required()
def undo_thumbs(record_id):
    """撤销星辰币记录（15分钟内）"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin':
        return jsonify({'code': 403, 'message': '无权限操作'}), 403

    record = ThumbsRecord.query.get(record_id)
    if not record:
        return jsonify({'code': 404, 'message': '记录不存在'}), 404
    if record.is_deleted:
        return jsonify({'code': 400, 'message': '该记录已撤销'}), 400

    age = datetime.utcnow() - record.created_at
    if age > timedelta(minutes=15):
        return jsonify({'code': 400, 'message': '超过15分钟，无法撤销'}), 400

    user = User.query.get(record.user_id)
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404

    try:
        record.is_deleted = True
        if record.points > 0:
            user.total_points -= record.points
            user.available_points -= record.points
            if user.available_points < 0:
                user.available_points = 0
        else:
            user.total_points -= record.points
            user.available_points -= record.points
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({'code': 500, 'message': '撤销失败，请重试'}), 500

    return jsonify({'code': 200, 'message': '已撤销该记录，能量已恢复'})


# ==================== 飞船升级 API ====================

@app.route('/api/users/<int:user_id>/upgrade-ship', methods=['POST'])
@jwt_required()
def upgrade_ship(user_id):
    """消耗碎片升级飞船"""
    current_user_id = get_jwt_identity()
    if int(current_user_id) != user_id:
        return jsonify({'code': 403, 'message': '只能升级自己的飞船'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404

    fragments = user.fragments or {'engine': 0, 'radar': 0, 'hull': 0}
    if fragments.get('engine', 0) < 1 or fragments.get('radar', 0) < 1 or fragments.get('hull', 0) < 1:
        return jsonify({'code': 400, 'message': '碎片不足，需要各部件碎片至少1个'}), 400

    fragments['engine'] -= 1
    fragments['radar'] -= 1
    fragments['hull'] -= 1
    user.fragments = fragments
    user.ship_level = (user.ship_level or 1) + 1
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': f'飞船升级成功！当前等级：{user.ship_level}',
        'data': {'ship_level': user.ship_level, 'fragments': user.fragments}
    })


# ==================== 系统设置 API ====================

@app.route('/api/settings', methods=['GET'])
@jwt_required()
def get_settings():
    """获取系统设置"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin' or not current_user.is_super_admin:
        return jsonify({'code': 403, 'message': '无权限操作'}), 403

    settings = SystemSettings.query.first()
    if not settings:
        settings = SystemSettings()
        db.session.add(settings)
        db.session.commit()

    return jsonify({'code': 200, 'data': settings.to_dict()})


@app.route('/api/settings', methods=['PUT'])
@jwt_required()
def update_settings():
    """更新系统设置"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin' or not current_user.is_super_admin:
        return jsonify({'code': 403, 'message': '无权限操作'}), 403

    settings = SystemSettings.query.first()
    if not settings:
        settings = SystemSettings()
        db.session.add(settings)

    data = request.get_json()

    if 'speaker_ip' in data:
        settings.speaker_ip = data['speaker_ip'].strip()
    if 'heartbeat_interval' in data:
        settings.heartbeat_interval = max(1, int(data['heartbeat_interval']))
    if 'enable_broadcast' in data:
        settings.enable_broadcast = bool(data['enable_broadcast'])
    if 'enable_timed_broadcast' in data:
        settings.enable_timed_broadcast = bool(data['enable_timed_broadcast'])
    if 'morning_broadcast_time' in data:
        settings.morning_broadcast_time = data['morning_broadcast_time']
    if 'evening_broadcast_time' in data:
        settings.evening_broadcast_time = data['evening_broadcast_time']
    if 'broadcast_targets' in data:
        settings.broadcast_targets = data['broadcast_targets']

    db.session.commit()

    # 重新配置音箱客户端
    speaker_client.configure(
        speaker_ip=settings.speaker_ip,
        heartbeat_interval=settings.heartbeat_interval
    )

    # 动态刷新定时播报任务
    _reschedule_broadcast_jobs(settings)

    return jsonify({'code': 200, 'message': '设置已保存', 'data': settings.to_dict()})


@app.route('/api/settings/test-broadcast', methods=['POST'])
@jwt_required()
def test_broadcast():
    """发送测试广播"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role != 'admin' or not current_user.is_super_admin:
        return jsonify({'code': 403, 'message': '无权限操作'}), 403

    settings = SystemSettings.query.first()
    if not settings or not settings.speaker_ip:
        return jsonify({'code': 400, 'message': '请先配置音箱 IP 地址'}), 400

    ok = speaker_client.send_text('叮咚！这是来自星途补给站的测试广播，音箱连接正常，一切就绪！')
    if ok:
        return jsonify({'code': 200, 'message': '测试广播已发送'})
    else:
        return jsonify({'code': 503, 'message': '音箱未连接，请检查 IP 和网络'}), 503


# ==================== 定时任务 ====================

def energy_decay_job():
    """每日检查：连续3天未活跃的用户扣除1点能量"""
    with app.app_context():
        cutoff = datetime.utcnow().date() - timedelta(days=3)
        inactive_users = User.query.filter(
            User.role == 'user',
            db.or_(
                User.last_active_date == None,
                User.last_active_date < cutoff
            )
        ).all()
        for user in inactive_users:
            if user.available_points > 0:
                user.available_points -= 1
                user.total_points -= 1
                record = ThumbsRecord(
                    user_id=user.id,
                    thumb_type='deduction',
                    points=-1,
                    reason='连续3天未完成任务，能量自动衰减',
                    given_by=None,
                    admin_id=None
                )
                db.session.add(record)
        db.session.commit()


def db_backup_job():
    """每日凌晨3点备份数据库，保留最近7份"""
    with app.app_context():
        cfg = app.config
        host = cfg.get('MYSQL_HOST', 'localhost')
        port = cfg.get('MYSQL_PORT', 3306)
        user = cfg.get('MYSQL_USER', 'root')
        password = cfg.get('MYSQL_PASSWORD', 'root')
        database = cfg.get('MYSQL_DATABASE', 'thumbs_mall')

        filename = datetime.now().strftime('%Y-%m-%d') + '.sql'
        filepath = os.path.join(BACKUP_DIR, filename)

        env = os.environ.copy()
        env['MYSQL_PWD'] = password
        result = subprocess.run(
            ['mysqldump', '-h', host, '-P', str(port), '-u', user, database],
            capture_output=True, env=env
        )
        if result.returncode == 0:
            with open(filepath, 'wb') as f:
                f.write(result.stdout)
            # 清理超过7天的备份
            backups = sorted(glob_module.glob(os.path.join(BACKUP_DIR, '*.sql')))
            for old in backups[:-7]:
                os.remove(old)


def do_morning_broadcast():
    """早上定时简报"""
    with app.app_context():
        settings = SystemSettings.query.first()
        if not settings or not settings.enable_timed_broadcast or not settings.speaker_ip:
            return
        target_ids = settings.broadcast_targets or []
        if not target_ids:
            target_ids = [u.id for u in User.query.filter_by(role='user').all()]
        for uid in target_ids:
            user = User.query.get(uid)
            if not user:
                continue
            wish_name, energy_diff = _get_closest_wish(user)
            text = _build_timed_broadcast_text(
                target_name=user.real_name,
                total=user.available_points,
                period='morning',
                wish_name=wish_name,
                energy_diff=energy_diff
            )
            speaker_client.send_text(text)


def do_evening_broadcast():
    """晚上定时简报"""
    with app.app_context():
        settings = SystemSettings.query.first()
        if not settings or not settings.enable_timed_broadcast or not settings.speaker_ip:
            return
        target_ids = settings.broadcast_targets or []
        if not target_ids:
            target_ids = [u.id for u in User.query.filter_by(role='user').all()]
        for uid in target_ids:
            user = User.query.get(uid)
            if not user:
                continue
            wish_name, energy_diff = _get_closest_wish(user)
            text = _build_timed_broadcast_text(
                target_name=user.real_name,
                total=user.available_points,
                period='evening',
                wish_name=wish_name,
                energy_diff=energy_diff
            )
            speaker_client.send_text(text)


def _reschedule_broadcast_jobs(settings):
    """根据最新配置动态更新早晚广播的 APScheduler job"""
    for job_id in ('morning_broadcast', 'evening_broadcast'):
        if scheduler.get_job(job_id):
            scheduler.remove_job(job_id)

    if not settings.enable_timed_broadcast:
        return

    if settings.morning_broadcast_time:
        try:
            h, m = settings.morning_broadcast_time.split(':')
            scheduler.add_job(
                do_morning_broadcast, 'cron',
                hour=int(h), minute=int(m),
                id='morning_broadcast',
                replace_existing=True
            )
        except Exception:
            pass

    if settings.evening_broadcast_time:
        try:
            h, m = settings.evening_broadcast_time.split(':')
            scheduler.add_job(
                do_evening_broadcast, 'cron',
                hour=int(h), minute=int(m),
                id='evening_broadcast',
                replace_existing=True
            )
        except Exception:
            pass


scheduler = BackgroundScheduler()
scheduler.add_job(energy_decay_job, 'cron', hour=0, minute=5)
scheduler.add_job(db_backup_job, 'cron', hour=3, minute=0)


# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'code': 404, 'message': '资源不存在'}), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'code': 500, 'message': '服务器内部错误'}), 500


# ==================== 主程序 ====================

if __name__ == '__main__':
    with app.app_context():
        # 创建所有表
        db.create_all()

        # 检查是否存在管理员，如果不存在则创建
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                real_name='系统管理员',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('已创建默认管理员账号: admin / admin123')

        # 初始化系统设置（若无记录则写入默认值）
        if not SystemSettings.query.first():
            db.session.add(SystemSettings())
            db.session.commit()

        # 从数据库加载音箱配置
        settings = SystemSettings.query.first()
        if settings and settings.speaker_ip:
            speaker_client.configure(
                speaker_ip=settings.speaker_ip,
                heartbeat_interval=settings.heartbeat_interval or 10
            )
            speaker_client.start()

        # 注册定时播报任务
        _reschedule_broadcast_jobs(settings) if settings else None

    scheduler.start()
    app.run(host='0.0.0.0', port=28001, debug=True)
