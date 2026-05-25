SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

CREATE DATABASE IF NOT EXISTS star_mall CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE star_mall;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id              INT PRIMARY KEY AUTO_INCREMENT,
    username        VARCHAR(50) UNIQUE NOT NULL,
    password        VARCHAR(255) NOT NULL,
    real_name       VARCHAR(50) NOT NULL,
    email           VARCHAR(100),
    phone           VARCHAR(20),
    avatar          VARCHAR(255) DEFAULT NULL COMMENT '头像（预设标识或上传路径）',
    role            ENUM('admin', 'user') DEFAULT 'user',
    is_super_admin  TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否超级管理员',
    total_points     INT DEFAULT 0 COMMENT '总能量',
    available_points INT DEFAULT 0 COMMENT '可用能量',
    fragments        JSON DEFAULT (JSON_OBJECT('engine', 0, 'radar', 0, 'hull', 0)) COMMENT '飞船碎片',
    ship_level       INT DEFAULT 1 COMMENT '飞船等级',
    streak_days      INT DEFAULT 0 COMMENT '连续打卡天数',
    last_active_date DATE DEFAULT NULL COMMENT '最后活跃日期',
    is_child         TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否儿童账号',
    child_pattern    VARCHAR(255) DEFAULT NULL COMMENT '儿童图案解锁密码（哈希）',
    status           VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '账号状态：active/pending',
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
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
    admin_id       INT COMMENT '操作管理员ID（审计用）',
    is_deleted     TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否已撤销',
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (given_by) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE SET NULL,
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

-- 任务模板表
CREATE TABLE IF NOT EXISTS tasks (
    id            INT PRIMARY KEY AUTO_INCREMENT,
    title         VARCHAR(100) NOT NULL COMMENT '任务名称',
    type          ENUM('daily', 'milestone') NOT NULL DEFAULT 'daily' COMMENT '每日日常/阶段里程碑',
    energy_reward INT NOT NULL DEFAULT 1 COMMENT '奖励能量值',
    is_active     TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否启用',
    reviewer_id   INT DEFAULT NULL COMMENT '专属审批人（NULL=所有管理员可审批）',
    created_by    INT DEFAULT NULL COMMENT '任务创建者',
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (reviewer_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (created_by)  REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='任务模板表';

-- 任务执行记录表
CREATE TABLE IF NOT EXISTS task_logs (
    id         INT PRIMARY KEY AUTO_INCREMENT,
    user_id    INT NOT NULL,
    task_id    INT NOT NULL,
    status     ENUM('pending', 'approved', 'rejected') NOT NULL DEFAULT 'pending' COMMENT '待审核/已批准/已驳回',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
    INDEX idx_user_task (user_id, task_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='任务执行记录表';

-- ==========================================
-- 🚀 初始乘员编制写入 (默认密码已保留)
-- ==========================================

-- 1. 舰长 (密码: admin123)，超级管理员
INSERT INTO users (username, password, real_name, role, is_super_admin, total_points, available_points, ship_level, streak_days) VALUES
('admin', 'scrypt:32768:8:1$i0kfF5rTSvoYIK8w$f3a64acc3231e2ae09726f8ec928b75a5617105889add4813756d6adb6ed2ded6b5e8f4102732f34f40e3e48aec18baff3128f974d6933ea77eb71f7e3abadfd', '舰长', 'admin', 1, 0, 0, 1, 0);

-- 2. 领航员 - 方老师 (密码: user123)，普通管理员（审批任务、发分）
INSERT INTO users (username, password, real_name, role, is_super_admin, total_points, available_points, ship_level, streak_days) VALUES
('fang', 'scrypt:32768:8:1$RYUIJQhxyh2NrIZM$bbdd6fa8eb3a1d72ae2c1eb347bb8363b61fd16951791512dcb7c2371ed97a32d9ee6edf95d1da739d1745492cc1cbddc53285cfd4b909c38f21dbebb531c4d6', '方老师', 'admin', 0, 0, 0, 1, 0);

-- 3. 探索者 - 乔伊 (密码: user123)，初始自带 50 能量新兵津贴
INSERT INTO users (username, password, real_name, role, is_super_admin, total_points, available_points, ship_level, streak_days) VALUES
('joy', 'scrypt:32768:8:1$kbt6ZfAICQTlL1fX$fafbc667c308f90851d4e833757c558b4b79d1dc4a03addb9fe1c5a547faf1a4407e30bcf00fc99ee157b9031f59ad8977deb05ad4abe235b28ee2821586f673', '乔伊', 'user', 0, 50, 50, 1, 0);


-- ==========================================
-- 🎯 初始任务大厅数据 (全部归属舰长创建，所有领航员可审批)
-- ==========================================

INSERT INTO tasks (title, type, energy_reward, is_active, created_by) VALUES
-- 晨间任务
('早起', 'daily', 1, 1, 1),
('主动洗漱刷牙', 'daily', 1, 1, 1),
('快速吃完早餐', 'daily', 2, 1, 1),
('不看电视手机（早上）', 'daily', 1, 1, 1),
('情绪稳定开心（早上）', 'daily', 1, 1, 1),
-- 学校任务
('早上主动收拾书包去上学', 'daily', 1, 1, 1),
('每天举手回答问题次数超过3次', 'daily', 2, 1, 1),
('听写全对（学校）', 'daily', 1, 1, 1),
('计算练习全对（学校）', 'daily', 1, 1, 1),
-- 托管班与作业
('规定时间内写完作业', 'daily', 2, 1, 1),
('听写全对（托管班）', 'daily', 1, 1, 1),
('计算练习全对（托管班）', 'daily', 1, 1, 1),
-- 晚间休整
('书写工整美观', 'daily', 1, 1, 1),
('主动收拾书包（晚上）', 'daily', 1, 1, 1),
('主动整理文具、削笔', 'daily', 1, 1, 1),
('不看电视手机（晚上）', 'daily', 1, 1, 1),
('情绪稳定（晚上）', 'daily', 1, 1, 1),
('主动洗漱、上床休息', 'daily', 2, 1, 1),
-- 阶段里程碑
('语文/数学大练习任意一科超过98分', 'milestone', 15, 1, 1),
('语文/数学大练习两科满分', 'milestone', 40, 1, 1),
('期末考试满分', 'milestone', 150, 1, 1);


-- ==========================================
-- 🛒 初始补给物资库房数据 (上架状态)
-- ==========================================

INSERT INTO products (name, description, points_required, stock, status, sort_order, is_blind_box) VALUES
('免阅读一晚 (30分钟)', '豁免今晚的30分钟常规阅读，好好放松一下！', 35, 999, 'on_shelf', 1, 0),
('免运动一晚 (跳绳+体前屈)', '豁免今晚的体能训练指标，缓解肌肉疲劳。', 40, 999, 'on_shelf', 2, 0),
('小玩具 (空投盲盒)', '神秘的星际盲盒！里面可能是扭蛋、精美贴纸或小拼图。', 120, 10, 'on_shelf', 3, 1),
('滑板', '一款酷炫的反重力滑行器，培养平衡力与勇气的最佳装备。', 800, 1, 'on_shelf', 4, 0),
('头戴式耳机', '高保真声波沉浸头盔，畅游音乐宇宙的利器。', 1500, 1, 'on_shelf', 5, 0),
('宠物玉米蛇', '外星系共生体幼崽。需要极度的自律与长期的责任心才能换取的终极奖励。', 3000, 1, 'on_shelf', 6, 0);