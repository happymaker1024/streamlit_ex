CREATE DATABASE finance_db;
USE finance_db;

-- 거래내역 테이블 생성
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    category VARCHAR(50),
    description VARCHAR(200),
    amount INT NOT NULL,
    type VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 샘플 데이터
INSERT INTO transactions (date, category, description, amount, type) VALUES
('2025-01-10', '월급', '1월 급여', 3000000, '수입'),
('2025-01-12', '식비', '편의점', 5000, '지출'),
('2025-01-15', '교통', '지하철', 2500, '지출');