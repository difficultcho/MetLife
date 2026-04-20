-- 创建数据库
CREATE DATABASE IF NOT EXISTS metlife
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE metlife;

-- 商品表
CREATE TABLE IF NOT EXISTS products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(64) NOT NULL COMMENT '商品唯一编码',
  name VARCHAR(100) NOT NULL COMMENT '商品名称',
  image VARCHAR(255) NOT NULL COMMENT '商品图片文件名',
  description TEXT COMMENT '商品描述',
  sort_order INT NOT NULL DEFAULT 0 COMMENT '排序（升序）',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uk_code (code),
  INDEX idx_sort_order (sort_order)
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

-- 用户选择表（openid - product_code 关系）
CREATE TABLE IF NOT EXISTS user_selections (
  id INT AUTO_INCREMENT PRIMARY KEY,
  openid VARCHAR(64) NOT NULL COMMENT '微信用户openid',
  product_code VARCHAR(64) NOT NULL COMMENT '商品唯一编码',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uk_openid (openid),
  INDEX idx_product_code (product_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入示例商品（根据实际需求修改）
-- INSERT INTO products (code, name, image, description, sort_order) VALUES
--   ('P001', '商品A', 'product_a.png', '商品A描述', 1),
--   ('P002', '商品B', 'product_b.png', '商品B描述', 2);
