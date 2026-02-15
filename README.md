# FRAM - Farm Crop Management System

A comprehensive web-based Farm Crop Management System built with Python Flask and SQLAlchemy. This system helps farmers manage crop details from seeding to harvesting, track labour costs, manage expenses, calculate revenue, and generate financial reports.

## Features

### 🌾 Crop Management
- Add, edit, and delete crop records
- Track crop from seeding to harvesting
- Monitor crop status (Growing, Harvested, Failed)
- Track expected vs actual yield
- Record crop variety and specific details

### 🌱 Field Management
- Manage multiple fields
- Track field area and location
- View all crops growing in each field
- Edit and delete field records

### 👷 Labour Management
- Add and manage labour records
- Set daily wages for workers
- Track work date, type, and hours
- Calculate labour costs automatically
- Maintain active/inactive labour status

### 💰 Cost Management
- Track all crop expenses
- Categorize costs (Seeds, Fertilizer, Pesticide, Equipment, etc.)
- Record amount and transaction date
- Maintain detailed cost records

### 📊 Financial Analysis
- Calculate total revenue based on yield and market price
- Track total expenses (materials + labour)
- Calculate gross profit per crop
- View profit margins
- Labour cost summary
- Crop-wise financial analysis

### 📈 Reports & Dashboard
- Comprehensive dashboard with key metrics
- Financial reports with revenue, costs, and profit
- Labour cost summary
- Crop-wise profit analysis
- Export capabilities for data analysis

## System Architecture

```
fram-project/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── models.py            # Database models
│   ├── routes.py            # Application routes
│   ├── templates/           # HTML templates
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── fields.html
│   │   ├── crops.html
│   │   ├── labours.html
│   │   └── ... (other templates)
│   └── static/
│       └── css/
│           └── style.css
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Technology Stack

- **Backend**: Python 3.7+, Flask 2.3.2
- **Database**: MySQL 5.7+ (Safe, persistent storage)
- **ORM**: SQLAlchemy
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Charts**: Chart.js (for data visualization)
- **DB Driver**: PyMySQL, Flask-MySQLdb

## Database Models

### Field
- Stores field information (name, area in acres, location)
- One-to-many relationship with crops

### Crop
- Tracks crop information (type, variety, dates, yield)
- References field
- One-to-many with labour and cost records

### Labour
- Worker information (name, designation, contact, daily wage)
- One-to-many with labour records

### LabourRecord
- Records of work performed (date, hours, type, cost calculation)
- References crop and labour

### CostRecord
- Expense tracking (category, amount, date, description)
- References crop

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- **MySQL Server 5.7+** (Download: https://dev.mysql.com/downloads/mysql/)
- Git (optional, for cloning)

### Step 1: Clone or Download the Project
```bash
# If using git
git clone <repository-url>
cd fram-project

# Or download the zip file and extract it
```

### Step 2: Set Up MySQL Database

**Quick Setup (Windows):**
```bash
# Run the setup script (creates .env and provides guidance)
setup.bat
```

**Manual Setup:**
```bash
# Connect to MySQL
mysql -u root -p

# Create database
CREATE DATABASE fram_management;

# Exit
EXIT;
```

See **QUICKSTART_MYSQL.md** for detailed MySQL setup instructions.

### Step 3: Create a Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Configure Database Connection

Copy and edit the `.env` file:
```bash
# Windows
copy .env.example .env
notepad .env

# macOS/Linux
cp .env.example .env
nano .env
```

Edit with your MySQL credentials:
```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=fram_management
MYSQL_PORT=3306
```

### Step 5: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 6: Run the Application
```bash
python run.py
```

The application will start on `http://localhost:5000`

## Usage Guide

### Dashboard
- View main statistics and metrics
- Quick access to all major functions
- See total revenue, costs, and profit

### Field Management
1. Go to **Fields** menu
2. Click **Add Field** to create a new field
3. Enter field name, area (in acres), and location
4. View, edit, or delete existing fields

### Crop Management
1. Go to **Crops** menu
2. Click **Add Crop** to create a new crop
3. Select field, enter crop type, variety, and dates
4. Track crop status as it grows
5. Update actual yield and harvest date when harvested
6. View detailed crop information with all associated records

### Labour Management
1. Go to **Labour** menu
2. Click **Add Labour** to register a new worker
3. Set designation and daily wage rate
4. Add labour records to track work done on specific crops
5. Each labour record calculates cost automatically based on hours worked

### Cost Management
1. Go to **Costs** menu
2. Click **Add Cost** to record an expense
3. Select crop, category (Seeds, Fertilizer, etc.)
4. Enter amount and select date
5. All costs are automatically associated with crops

### Reports
1. Go to **Reports** menu
2. View comprehensive financial analysis
3. See crop-wise profit analysis
4. Review labour cost summary
5. Monitor overall farm profitability

## Default Market Price

By default, the system uses ₹25/kg as the market price for calculating revenue. You can modify this in:
- File: `app/routes.py`
- Function: `get_revenue()` in `app/models.py`
- Change: `market_price = 25` to your desired price

## Important Formulas

### Labour Cost Calculation
```
Hourly Rate = Daily Wage ÷ 8 (assuming 8-hour working day)
Labour Cost = Hours Worked × Hourly Rate
```

### Revenue Calculation
```
Revenue = Actual Yield (kg) × Market Price (₹/kg)
```

### Gross Profit Calculation
```
Gross Profit = Revenue - (Material Costs + Labour Costs)
```

### Profit Margin
```
Profit Margin = (Profit / Total Cost) × 100%
```

## Database

The application uses MySQL database which provides:
- **Persistent storage** - Data survives application restarts
- **Better security** - Encrypted connections possible
- **Scalability** - Can handle large datasets
- **Backup capabilities** - Easy database backups
- **Remote access** - Can connect to remote MySQL servers

**Database Configuration**: Set in `.env` file

To reset the database:
1. Delete all tables in MySQL: `mysql -u root -p fram_management < /dev/null`
2. Or drop and recreate: `DROP DATABASE fram_management; CREATE DATABASE fram_management;`
3. Restart the application (tables recreate automatically)

**Backup your data:**
```bash
mysqldump -u root -p fram_management > backup.sql
```

**Restore from backup:**
```bash
mysql -u root -p fram_management < backup.sql
```

## Configuration

The application uses environment variables for secure configuration.

### Files for Configuration

**`.env`** - Your actual configuration (keep secret!)
```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=fram_management
MYSQL_PORT=3306
SECRET_KEY=your-secret-key
FLASK_ENV=development
```

**`.env.example`** - Template for `.env` (safe to share)

**`config.py`** - Database configuration logic

### Modify Settings

To change configuration:
1. Edit `.env` file
2. Change values for MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, etc.
3. Restart the application

### For Production Deployment

1. Set `FLASK_ENV=production`
2. Use environment-specific `.env` file
3. Set strong `SECRET_KEY`
4. Use dedicated database user (not root)
5. Configure MySQL for remote access (if needed)

See **MYSQL_SETUP.md** for production security guidelines.

## Troubleshooting

### Port Already in Use
If port 5000 is busy, modify `run.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5001 to desired port
```

### Database Issues
1. Delete `farm_management.db`
2. Delete `__pycache__` folders
3. Restart the application

### Module Not Found Error
1. Ensure virtual environment is activated
2. Run `pip install -r requirements.txt` again
3. Check Python version (should be 3.7+)

## Future Enhancements

- Weather data integration
- IoT sensor integration for soil moisture
- Mobile application for field workers
- Advanced analytics and predictions
- Integration with agricultural markets for live prices
- Multi-user support with role-based access
- Offline mode for field operations
- Image gallery for crop stages
- Pest and disease tracking

## License

This project is open-source and available for educational and commercial use.

## Support

For issues or feature requests, please create an issue in the project repository.

---

**Happy Farming! 🌾**

---

## Quick Start Commands

```bash
# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python run.py

# Access the application
# Open browser and go to: http://localhost:5000
```

## REST API Endpoints (Currently Available for JSON Data)

- `GET /reports/api/crop-stats` - Get crop statistics in JSON format

## Browser Compatibility

- Chrome (Latest)
- Firefox (Latest)
- Safari (Latest)
- Edge (Latest)

## Data Backup

To backup your data:
1. Copy the `farm_management.db` file to a safe location
2. Store in cloud storage or external drive for safety

To restore:
1. Replace the existing `farm_management.db` with your backup
2. Restart the application

---

**Version**: 1.0.0 with MySQL  
**Last Updated**: February 2026

## 📚 Documentation Files

- **README.md** - This file, main documentation
- **QUICKSTART_MYSQL.md** - Quick setup guide for MySQL (Start here!)
- **MYSQL_SETUP.md** - Detailed MySQL setup and configuration
- **setup.bat** - Automated setup script for Windows
- **requirements.txt** - All Python packages needed
