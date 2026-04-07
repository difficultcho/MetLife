-- 创建数据库
CREATE DATABASE IF NOT EXISTS metlife
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE metlife;

-- 商品表
CREATE TABLE IF NOT EXISTS products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL COMMENT '商品名称',
  image VARCHAR(255) NOT NULL COMMENT '商品图片文件名',
  description TEXT COMMENT '商品描述',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 用户信息表
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  openid VARCHAR(64) NOT NULL COMMENT '微信用户openid',
  nickname VARCHAR(100) NOT NULL COMMENT '微信昵称',
  phone VARCHAR(20) NOT NULL COMMENT '手机号',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uk_openid (openid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 用户选择表
CREATE TABLE IF NOT EXISTS user_selections (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL COMMENT '用户ID',
  product_id INT NOT NULL COMMENT '选择的商品ID',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uk_user_id (user_id),
  INDEX idx_product_id (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入示例商品（根据实际需求修改）
-- INSERT INTO products (name, image, description) VALUES
--   ('商品A', 'product_a.png', '商品A描述'),
--   ('商品B', 'product_b.png', '商品B描述');
