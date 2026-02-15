# From SQLite to MySQL - Migration Guide

If you were using the old SQLite version and want to migrate data to MySQL, follow this guide.

## Backup Your Old Data

Before proceeding:

```bash
# Copy your old sqlite file (if it exists)
# farm_management.db (backup this first!)
```

## Option 1: Fresh Start (Recommended for Most Users)

If you don't have much data yet, simply:

1. Set up MySQL (see QUICKSTART_MYSQL.md)
2. Update `.env` with MySQL credentials
3. Run the application
4. Re-enter data through the web interface
5. All new data is stored in MySQL (safe!)

## Option 2: Export and Import Data

If you have significant data in SQLite and want to migrate it:

### Step 1: Export SQLite Data

```bash
# Export from old SQLite database to SQL file
sqlite3 farm_management.db .dump > sqlite_export.sql
```

### Step 2: Prepare MySQL Import

The SQL from SQLite needs adjustments for MySQL:

1. Open `sqlite_export.sql` file
2. Remove these lines (if present):
   - `PRAGMA foreign_keys=OFF;`
   - Any SQLite-specific PRAGMA statements
   - `AUTOINCREMENT` keywords

### Step 3: Create MySQL Database

```bash
mysql -u root -p
CREATE DATABASE fram_management;
EXIT;
```

### Step 4: Import into MySQL

```bash
# Import the modified SQL file
mysql -u root -p fram_management < sqlite_export.sql
```

### Step 5: Update .env and Run

Update your `.env` file with MySQL credentials:

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=fram_management
```

Run the application:

```bash
python run.py
```

## Option 3: Using MySQL Workbench for Data Transfer

### Using MySQL Workbench Data Migration Wizard:

1. Open MySQL Workbench
2. Go to **Database** → **Migrate...**  
3. Select SQLite as Source
4. Select MySQL as Target
5. Follow the wizard
6. Review and execute migration

## Data Integrity Checks

After migration, verify your data:

### Check Row Counts

```bash
# Connect to MySQL
mysql -u root -p fram_management

# Check tables
SELECT COUNT(*) as fields_count FROM field;
SELECT COUNT(*) as crops_count FROM crop;
SELECT COUNT(*) as labour_count FROM labour;
SELECT COUNT(*) as labour_records FROM labour_record;
SELECT COUNT(*) as costs_count FROM cost_record;
```

### Verify Relationships

```bash
# Check for orphaned records
SELECT crop.id FROM crop 
WHERE crop.field_id NOT IN (SELECT id FROM field);

SELECT labour_record.id FROM labour_record 
WHERE labour_record.crop_id NOT IN (SELECT id FROM crop);
```

## Troubleshooting Migration

### "Table already exists"

Drop existing tables first:

```bash
mysql -u root -p
USE fram_management;
DROP TABLE IF EXISTS labour_record;
DROP TABLE IF EXISTS cost_record;
DROP TABLE IF EXISTS labour;
DROP TABLE IF EXISTS crop;
DROP TABLE IF EXISTS field;
EXIT;

# Then re-import
mysql -u root -p fram_management < sqlite_export.sql
```

### "Foreign key constraint fails"

MySQL strict mode may reject invalid foreign keys:

```bash
mysql -u root -p
SET FOREIGN_KEY_CHECKS=0;
# Run import
SET FOREIGN_KEY_CHECKS=1;
```

### "Charset/Collation mismatch"

MySQL defaults to utf8mb4, SQLite uses UTF-8:

```bash
# This is usually automatic, but if issues:
# Recreate database with utf8mb4
DROP DATABASE fram_management;
CREATE DATABASE fram_management CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

## Delete Old SQLite File (Optional)

Once migration is complete and verified:

```bash
# Remove old SQLite database file
del farm_management.db

# Or
rm farm_management.db
```

⚠️ **Only delete after confirming all data is in MySQL!**

## Rollback to SQLite (If Needed)

If you want to go back to SQLite:

1. Keep backup of `.sql` export file
2. Restore from backup
3. Update `config.py` if changes were made

But **MySQL is recommended** for:
- Data safety
- Automatic backups
- Better performance
- Remote access capability

## Need Help?

1. Check MySQL is running
2. Verify credentials in `.env`
3. Check error messages in terminal
4. Review MySQL logs: `/var/log/mysql/error.log` (Linux/Mac)

---

**Status Check:**

✅ Old SQLite data exported  
✅ MySQL database created  
✅ Data imported to MySQL  
✅ `.env` configured with MySQL  
✅ Application running with MySQL  
✅ Old SQLite file deleted  

Your data is now safely in MySQL! 🎉
