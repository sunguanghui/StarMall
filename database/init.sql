SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

CREATE DATABASE IF NOT EXISTS thumbs_mall CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE thumbs_mall;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id              INT PRIMARY KEY AUTO_INCREMENT,
    username        VARCHAR(50) UNIQUE NOT NULL,
    password        VARCHAR(255) NOT NULL,
    real_name       VARCHAR(50) NOT NULL,
    email           VARCHAR(100),
    phone           VARCHAR(20),
    role            ENUM('admin', 'user') DEFAULT 'user',
    total_points    INT DEFAULT 0 COMMENT '总能量',
    available_points INT DEFAULT 0 COMMENT '可用能量',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 星辰币记录表
CREATE TABLE IF NOT EXISTS thumbs_records (
    id             INT PRIMARY KEY AUTO_INCREMENT,
    user_id        INT NOT NULL,
    thumb_type     ENUM('single', 'double', 'deduction') NOT NULL COMMENT '单星辰币/双星辰币/扣除能量',
    points         INT NOT NULL COMMENT '能量变化值（负数为扣除）',
    reason         VARCHAR(255) COMMENT '原因',
    parent_message TEXT COMMENT '舰长寄语',
    given_by       INT COMMENT '发放人ID',
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (given_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='星辰币记录表';

-- 商品表
CREATE TABLE IF NOT EXISTS products (
    id              INT PRIMARY KEY AUTO_INCREMENT,
    name            VARCHAR(100) NOT NULL,
    description     TEXT,
    image_url       VARCHAR(255),
    points_required INT NOT NULL COMMENT '所需能量',
    stock           INT DEFAULT 0 COMMENT '库存数量',
    status          ENUM('on_shelf', 'off_shelf') DEFAULT 'off_shelf' COMMENT '上架/下架状态',
    sort_order      INT DEFAULT 0 COMMENT '排序顺序',
    is_blind_box    TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否盲盒',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_sort_order (sort_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='商品表';

-- 兑换记录表
CREATE TABLE IF NOT EXISTS exchange_records (
    id           INT PRIMARY KEY AUTO_INCREMENT,
    user_id      INT NOT NULL,
    product_id   INT NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    points_spent INT NOT NULL COMMENT '消耗能量',
    quantity     INT DEFAULT 1 COMMENT '兑换数量',
    status       ENUM('pending', 'completed', 'cancelled') DEFAULT 'pending' COMMENT '兑换状态',
    remark       VARCHAR(255),
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='兑换记录表';

-- 星际心愿单表
CREATE TABLE IF NOT EXISTS wishlists (
    id              INT PRIMARY KEY AUTO_INCREMENT,
    user_id         INT NOT NULL,
    title           VARCHAR(200) NOT NULL COMMENT '心愿名称',
    expected_points INT NOT NULL DEFAULT 0 COMMENT '期望能量值',
    status          ENUM('pending', 'approved', 'rejected') NOT NULL DEFAULT 'pending' COMMENT '审核状态',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_id (user_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='星际心愿单表';

-- 默认管理员账号 (密码: admin123)
INSERT INTO users (username, password, real_name, role, total_points, available_points) VALUES
('admin', 'scrypt:32768:8:1$i0kfF5rTSvoYIK8w$f3a64acc3231e2ae09726f8ec928b75a5617105889add4813756d6adb6ed2ded6b5e8f4102732f34f40e3e48aec18baff3128f974d6933ea77eb71f7e3abadfd', '系统管理员', 'admin', 0, 0);

-- 测试用户 (密码: user123)
INSERT INTO users (username, password, real_name, email, total_points, available_points) VALUES
('zhangsan', 'scrypt:32768:8:1$RYUIJQhxyh2NrIZM$bbdd6fa8eb3a1d72ae2c1eb347bb8363b61fd16951791512dcb7c2371ed97a32d9ee6edf95d1da739d1745492cc1cbddc53285cfd4b909c38f21dbebb531c4d6', '张三', 'zhangsan@example.com', 100, 100),
('lisi', 'scrypt:32768:8:1$kbt6ZfAICQTlL1fX$fafbc667c308f90851d4e833757c558b4b79d1dc4a03addb9fe1c5a547faf1a4407e30bcf00fc99ee157b9031f59ad8977deb05ad4abe235b28ee2821586f673', '李四', 'lisi@example.com', 50, 50);

-- 测试商品
INSERT INTO products (name, description, points_required, stock, status, sort_order) VALUES
('小米充电宝', '10000mAh 快充移动电源', 50, 10, 'on_shelf', 1),
('星巴克咖啡券', '中杯任意饮品兑换券', 30, 20, 'on_shelf', 2),
('定制水杯', '公司logo定制保温杯', 80, 5, 'on_shelf', 3),
('京东卡100元', '京东购物卡100元面额', 100, 8, 'on_shelf', 4),
('无线鼠标', '罗技无线办公鼠标', 60, 0, 'off_shelf', 5);

-- 测试星辰币记录
INSERT INTO thumbs_records (user_id, thumb_type, points, reason, given_by) VALUES
(2, 'double', 5, '项目按时交付，表现优秀', 1),
(2, 'single', 1, '积极参与团队活动', 1),
(3, 'single', 1, '帮助同事解决技术问题', 1);
