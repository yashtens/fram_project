# MySQL Setup Guide for FRAM Farm Management System

## Prerequisites

Before you start, install MySQL Server on your system.

### Windows
**Download and Install MySQL**:
1. Download from: https://dev.mysql.com/downloads/mysql/
2. Run the installer and follow the setup wizard
3. Default: Install on localhost (127.0.0.1) with port 3306
4. Set root password during installation
5. MySQL Workbench will be installed for easier management

### macOS
```bash
# Using Homebrew
brew install mysql
brew services start mysql

# Secure installation
mysql_secure_installation
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install mysql-server

# Secure installation
sudo mysql_secure_installation
```

---

## Step 1: Create Database and User

### Option A: Using MySQL Workbench (GUI - Easiest)
1. Open MySQL Workbench
2. Connect to your MySQL server
3. Create a new database:
```sql
CREATE DATABASE fram_management;
```

### Option B: Using Command Line
```bash
# Connect to MySQL
mysql -u root -p

# Enter your password when prompted

# Create database
CREATE DATABASE fram_management;

# Create user with password (RECOMMENDED for security)
CREATE USER 'fram_user'@'localhost' IDENTIFIED BY 'fram_secure_password';

# Grant permissions
GRANT ALL PRIVILEGES ON fram_management.* TO 'fram_user'@'localhost';

# Flush privileges
FLUSH PRIVILEGES;

# Exit MySQL
EXIT;
```

---

## Step 2: Configure FRAM Application

### Edit `.env` file in project root

Located at: `d:\fram-project\.env`

```env
# MySQL Database Configuration
MYSQL_HOST=localhost
MYSQL_USER=root                    # Change to 'fram_user' if you created a new user
MYSQL_PASSWORD=your_password_here  # Enter your MySQL password
MYSQL_DB=fram_management
MYSQL_PORT=3306

# Flask Configuration
SECRET_KEY=your-secret-key-change-in-production
FLASK_ENV=development
```

**Example configurations:**

**Using root user:**
```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_root_password
MYSQL_DB=fram_management
MYSQL_PORT=3306
```

**Using dedicated user (Recommended):**
```env
MYSQL_HOST=localhost
MYSQL_USER=fram_user
MYSQL_PASSWORD=fram_secure_password
MYSQL_DB=fram_management
MYSQL_PORT=3306
```

---

## Step 3: Run the Application

### Activate Virtual Environment
```bash
cd d:\fram-project
.venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Application
```bash
python run.py
```

The application will automatically create all tables in your MySQL database!

---

## Step 4: Verify Database Connection

### Check in MySQL Workbench
1. Open MySQL Workbench
2. Connect to your database
3. Navigate to `fram_management` database
4. You should see these tables:
   - `field`
   - `crop`
   - `labour`
   - `labour_record`
   - `cost_record`

### Check via Command Line
```bash
mysql -u root -p fram_management
SHOW TABLES;
```

You should see 5 tables listed.

---

## Troubleshooting

### Error: "Access Denied"
- Check your username and password in `.env` file
- Verify MySQL is running
- Ensure user has required permissions

### Error: "Unknown Database"
- Create the database first:
```bash
mysql -u root -p
CREATE DATABASE fram_management;
EXIT;
```

### Error: "Can't connect to MySQL server"
- MySQL service not running
- Windows: Start MySQL service from Services
- macOS/Linux: Run `brew services start mysql` or `sudo systemctl start mysql`
- Check if MySQL is on correct host/port

### Error: "No module named 'MySQLdb'"
- Install dependencies:
```bash
pip install -r requirements.txt
```

### Application won't start
- Verify `.env` file exists in project root
- Check MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD values
- Ensure MySQL service is running
- Check database name is created

---

## Backing Up Your Data

### MySQL Command Line Backup
```bash
# Create backup
mysqldump -u root -p fram_management > fram_backup.sql

# Enter password when prompted
```

### Restore from Backup
```bash
# Restore backup
mysql -u root -p fram_management < fram_backup.sql

# Enter password when prompted
```

### Using MySQL Workbench
1. Connect to database
2. Right-click on `fram_management`
3. Select "Dump SQL File..."
4. Choose location to save backup

---

## Moving to Production

For production deployment:

1. Update `.env` with production credentials
2. Set `FLASK_ENV=production` in `.env`
3. Use strong passwords
4. Enable MySQL password for all users
5. Remove default user if exists
6. Use environment-specific `.env` files

---

## Security Best Practices

✅ **DO:**
- Set strong passwords (min 12 characters)
- Use dedicated database user (not root)
- Change default passwords
- Enable MySQL logging
- Regular database backups
- Use HTTPS in production
- Restrict database access to application server

❌ **DON'T:**
- Store passwords in code
- Use root user for application
- Share `.env` file or credentials
- Use default MySQL credentials
- Leave MySQL with no password

---

## Quick Reference: MySQL Commands

```bash
# Start MySQL service
# Windows: net start MySQL80
# macOS: brew services start mysql
# Linux: sudo systemctl start mysql

# Connect to MySQL
mysql -u root -p

# List all databases
SHOW DATABASES;

# Select a database
USE fram_management;

# Show tables
SHOW TABLES;

# Describe table structure
DESCRIBE field;

# See user statistics
SELECT * FROM user;

# Stop MySQL service
# Windows: net stop MySQL80
# macOS: brew services stop mysql
# Linux: sudo systemctl stop mysql
```

---

## Need Help?

1. Check MySQL is running
2. Verify credentials in `.env`
3. Ensure database exists: `CREATE DATABASE fram_management;`
4. Check user permissions
5. Review application logs
6. Test connection with: `mysql -u username -p -h localhost fram_management`

---

**Setup Complete! Your data is now safely stored in MySQL.** 🎉
