# QUICK START GUIDE - MySQL Configuration

## What Changed?

✅ **Switched from SQLite to MySQL** for safer, persistent data storage  
✅ **All data is now stored in a proper database** (not local file)  
✅ **Better security** with credentials in `.env` file  
✅ **Easy to backup** and restore  

---

## 3 QUICK STEPS TO GET STARTED

### Step 1: Install MySQL (If Not Already Installed)

**Download MySQL**: https://dev.mysql.com/downloads/mysql/

Choose your OS:
- **Windows**: MySQL Community Server MSI Installer
- **macOS**: DMG Archive
- **Linux**: Repository

**Installation Tips:**
- Default port: 3306 ✓
- Remember your root password! 📝
- Install MySQL Workbench (GUI tool) for easier management

---

### Step 2: Create Database and Update Configuration

**Option A: Using Command Line (2 minutes)**

```bash
# Open Command Prompt/Terminal

# Connect to MySQL
mysql -u root -p

# Enter your MySQL password

# Create the database
CREATE DATABASE fram_management;

# Exit MySQL
EXIT;
```

**Option B: Using MySQL Workbench (GUI)**

1. Open MySQL Workbench
2. Connect to your server
3. Execute query: `CREATE DATABASE fram_management;`

---

### Step 3: Run the Application

**Navigate to project folder:**

```bash
cd d:\fram-project
```

**Run setup script (Windows):**

```bash
setup.bat
```

This script will:
- Create virtual environment (if needed)
- Install all packages
- Create `.env` file
- Prompt you to enter MySQL credentials

**OR Manual Steps:**

```bash
# Activate virtual environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Edit .env file with your MySQL credentials
notepad .env

# Run application
python run.py
```

**Open in browser:** http://localhost:5000

---

## Configure .env File

Edit the `.env` file in project root with your MySQL details:

```env
MYSQL_HOST=localhost          # Your MySQL server address
MYSQL_USER=root               # Your MySQL username
MYSQL_PASSWORD=your_password  # Your MySQL password
MYSQL_DB=fram_management      # Database name (don't change)
MYSQL_PORT=3306               # MySQL port (don't change)
```

**Example with custom user:**

```env
MYSQL_HOST=localhost
MYSQL_USER=fram_user
MYSQL_PASSWORD=MySecurePass123
MYSQL_DB=fram_management
MYSQL_PORT=3306
```

---

## Verify It's Working

### Check in Application

1. Go to Dashboard (http://localhost:5000)
2. Add a Field
3. Add a Crop
4. Data should be saved

### Check in MySQL Workbench

1. Connect to your database
2. Go to `fram_management` database
3. You should see 5 tables:
   - `field`
   - `crop`
   - `labour`
   - `labour_record`
   - `cost_record`

---

## Common Issues & Solutions

### "Access Denied for user 'root'"
- Check password in `.env` is correct
- Test: `mysql -u root -p` (enters password in prompt)

### "Unknown database 'fram_management'"
- Create it: `mysql -u root -p -e "CREATE DATABASE fram_management;"`

### "Can't connect to MySQL server"
- MySQL not running? Start it:
  - Windows: Services → MySQL → Right-click → Start
  - macOS: `brew services start mysql`
  - Linux: `sudo systemctl start mysql`

### Module not found error
- Run: `pip install -r requirements.txt`

---

## Files You Need to Know

| File | Purpose |
|------|---------|
| `.env` | MySQL credentials (keep secret!) |
| `.env.example` | Template for `.env` |
| `config.py` | Database configuration |
| `requirements.txt` | Python packages needed |
| `MYSQL_SETUP.md` | Detailed MySQL guide |
| `setup.bat` | Windows setup script |

---

## Database Tables Structure

### field
```
- id (Primary Key)
- name (Field Name)
- area (in acres)
- location (Address)
- created_date (Timestamp)
```

### crop
```
- id (Primary Key)
- field_id (Foreign Key)
- crop_type (Rice, Wheat, etc.)
- variety (Name variety)
- seeding_date, harvest_date
- yield (kg)
- status (Growing/Harvested/Failed)
```

### labour
```
- id (Primary Key)
- name (Worker name)
- designation (Farmer/Labourer/Supervisor)
- contact (Phone)
- daily_wage (₹/day)
- status (Active/Inactive)
```

### labour_record
```
- id (Primary Key)
- crop_id, labour_id (Foreign Keys)
- work_date, hours_worked
- work_type (Seeding/Weeding/Harvesting, etc.)
```

### cost_record
```
- id (Primary Key)
- crop_id (Foreign Key)
- category (Seeds/Fertilizer/Pesticide, etc.)
- amount (₹)
- transaction_date
```

---

## Backing Up Your Data

### Backup Command

```bash
# Create backup file
mysqldump -u root -p fram_management > fram_backup.sql

# Restore from backup
mysql -u root -p fram_management < fram_backup.sql
```

### Using MySQL Workbench

1. Right-click `fram_management` database
2. Select "Dump SQL File..."
3. Choose save location
4. File saved with all data

---

## Security Notes

🔒 **Keep `.env` file safe - it contains your database password!**

- Don't commit `.env` to GitHub
- Don't share `.env` file
- Use strong passwords (12+ characters)
- Change default passwords
- For production, use dedicated database user (not root)

---

## Troubleshooting Step-by-Step

1. **Is MySQL running?**
   ```bash
   mysql -u root -p
   # If error: MySQL not running
   ```

2. **Does database exist?**
   ```bash
   mysql -u root -p
   SHOW DATABASES;
   # Look for 'fram_management'
   ```

3. **Are credentials correct in .env?**
   - Open `.env` file
   - Match MYSQL_USER, MYSQL_PASSWORD exactly

4. **Are packages installed?**
   ```bash
   pip install -r requirements.txt
   ```

5. **Try running application**
   ```bash
   python run.py
   ```

---

## Need Advanced MySQL?

For production or advanced setup, see: `MYSQL_SETUP.md`

Includes:
- Creating dedicated database user
- Security best practices
- Remote MySQL connections
- Backup strategies
- Performance tuning

---

## Quick Commands Reference

```bash
# Start MySQL service (Windows)
net start MySQL80

# Stop MySQL service (Windows)
net stop MySQL80

# Connect to MySQL
mysql -u root -p

# List databases
SHOW DATABASES;

# Use database
USE fram_management;

# Show tables
SHOW TABLES;

# Verify connection
SELECT DATABASE();
```

---

**Your data is now safely stored in MySQL! 🎉**

For questions: Check README.md or MYSQL_SETUP.md
