PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE users (
	id INTEGER NOT NULL  
	email VARCHAR  
	hashed_password VARCHAR  
	is_active BOOLEAN  
	PRIMARY KEY (id)
);
INSERT INTO users VALUES(1 'satya5202@gmail.com' '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4' 1);
CREATE TABLE apps (
	id INTEGER NOT NULL  
	name VARCHAR  
	image VARCHAR  
	description VARCHAR  
	switch VARCHAR  
	volume VARCHAR  
	time_created DATETIME DEFAULT (CURRENT_TIMESTAMP)  
	owner_id INTEGER  
	PRIMARY KEY (id)  
	FOREIGN KEY(owner_id) REFERENCES users (id)
);
INSERT INTO apps VALUES(1 'nginx' 'nginx' '' 'on' '' '2023-07-16 18:32:15' 1);
CREATE TABLE ports (
	id INTEGER NOT NULL  
	pod_port INTEGER  
	user_port INTEGER  
	app_id INTEGER  
	PRIMARY KEY (id)  
	FOREIGN KEY(app_id) REFERENCES apps (id) ON DELETE CASCADE
);
INSERT INTO ports VALUES(1 80 80 1);
CREATE INDEX ix_users_id ON users (id);
CREATE UNIQUE INDEX ix_users_email ON users (email);
CREATE INDEX ix_apps_name ON apps (name);
CREATE INDEX ix_apps_id ON apps (id);
CREATE INDEX ix_ports_id ON ports (id);
COMMIT;