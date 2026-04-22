CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    amount FLOAT,
    category VARCHAR(100),
    date DATE,
    member_id INT,
    description TEXT,
    mode_of_payment VARCHAR(50),
    CONSTRAINT fk_member
        FOREIGN KEY (member_id)
        REFERENCES members(member_id)
		ON DELETE SET NULL
		ON UPDATE CASCADE
) ENGINE=InnoDB; 