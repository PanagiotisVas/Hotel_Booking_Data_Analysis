# Hotel Booking Data Analysis
A full-stack desktop application that analyzes hotel booking data, visualizes business KPIs and persists results into a MySQL database.

# 📊 Hotel Booking Analysis & ETL Dashboard

**An end-to-end data analysis tool developed to derive actionable insights from over 119,000 hotel booking records.**

Unlike standard analysis scripts, this is a fully interactive **Desktop Application** built with **Tkinter**. It functions as a complete **ETL (Extract, Transform, Load)** pipeline.

---

## 🎯 Project Overview

This application manages the full data lifecycle:

1.  **Extract:** Ingests raw CSV data (`hotel_booking.csv`).
2.  **Transform:** Uses **Pandas** for data cleaning, seasonality calculation, and demographic segmentation.
3.  **Load:** Persists processed insights into a **MySQL Database** to ensure data integrity.
4.  **Visualize:** Generates interactive **Matplotlib** charts for business intelligence.
5.  **Export:** Allows users to query the SQL database and export specific reports back to CSV.

---

## 📈 Key Features

### Business Intelligence Modules
The application provides a GUI menu to visualize the following metrics:

* **KPI Dashboard:** Calculates Average Daily Rate (ADR), Mean Length of Stay, and Cancellation Rates per hotel.
* **Customer Segmentation:** Algorithmic classification of guests into *Solo, Couples, Families, or Groups* based on adult/child counts.
* **Seasonal Trends:** Time-series analysis of booking spikes across Winter, Spring, Summer, and Autumn.
* **Cancellation Risk:** Correlates seasonality with cancellation rates to identify high-risk periods.
* **Room Inventory:** Distribution analysis of reserved room types.

### Data Persistence & ETL
* **SQL Integration:** Connects to a local MySQL instance (`Hotel_booking_analysis`) and updates tables using `INSERT ... ON DUPLICATE KEY UPDATE` logic.
* **CSV Export Engine:** A dedicated menu allows users to fetch processed data from SQL and dump it into standardized CSV reports.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Data Processing:** Pandas, NumPy
* **Visualization:** Matplotlib
* **GUI Framework:** Tkinter
* **Database:** MySQL (via `mysql-connector-python`)

---

## 🚀 Installation & Setup

Follow these steps to set up the project locally.

### 1. Prerequisites
Ensure you have Python installed along with a local MySQL server. Install the required Python libraries:

```bash
pip install pandas matplotlib mysql-connector-python
2. Database Configuration
Crucial Step: Before running the app, you must initialize the database structure.

Create the Database: Open MySQL Workbench or your Command Line and run:

SQL
CREATE DATABASE Hotel_booking_analysis;
Import the Schema: A Hotel_booking_analysis.sql file is provided in this repository. It creates all necessary tables (basic_statistics, monthly_distribution, booking_trends, etc.).

Via MySQL Workbench: Go to Server -> Data Import -> Select Hotel_booking_analysis.sql -> Target Schema: Hotel_booking_analysis.

Via Command Line:

Bash
mysql -u root -p Hotel_booking_analysis < Hotel_booking_analysis.sql
3. Connection Setup
Open main.py and update the database credentials to match your local MySQL setup:

Python
mydb = mysql.connector.connect(
    host='localhost',
    user='root',       # Change to your MySQL username
    password='root',   # Change to your MySQL password
    database='Hotel_booking_analysis'
)
4. Running the App
Download the Data: Ensure the hotel_booking.csv dataset is present in the root directory (the same folder as main.py).

Launch the Dashboard:

Bash
python main.py
Interact: A GUI window will appear. Click on the menu buttons (e.g., "Display basic statistics") to visualize data. The application will automatically Insert/Update the SQL tables with the latest results upon every calculation.

📸 Screenshots
Main Menu
(Add screenshot here, e.g., ![])

Booking Trends Visualization
(Add screenshot here, e.g., ![])

👥 Author
Vasileios Zafeiris Computer Engineering and Informatics Department (CEID) University of Patras, Greece

Note: This project is for educational purposes and demonstrates the ability to build data-driven GUI applications and manage SQL pipelines via Python.
