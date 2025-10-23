-- 데이터베이스 생성
CREATE DATABASE ecommerce_db;
USE ecommerce_db;

-- 상품 테이블 생성
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10, 2) NOT NULL,
    stock INT DEFAULT 0,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 샘플 데이터 입력 (선택사항)
INSERT INTO products (name, category, price, stock, description) VALUES
('노트북', '전자제품', 1200000, 15, '고성능 업무용 노트북'),
('무선 마우스', '전자제품', 35000, 50, '인체공학적 디자인'),
('책상', '가구', 150000, 10, '원목 책상');