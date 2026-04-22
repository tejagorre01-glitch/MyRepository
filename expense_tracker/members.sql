CREATE TABLE members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    member_name VARCHAR(100) NOT NULL,
    total_spent DECIMAL(10,2) DEFAULT 0
) ENGINE=InnoDB;
