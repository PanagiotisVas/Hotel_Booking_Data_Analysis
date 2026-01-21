# Hotel Booking Data Analysis
> A full-stack desktop application that analyzes hotel booking data, visualizes business metrics, and persists insights into a MySQL database.

![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Language](https://img.shields.io/badge/Language-Python-1f425f)
![Library](https://img.shields.io/badge/Library-Pandas_%7C_Matplotlib-007ACC)
![Interface](https://img.shields.io/badge/Interface-Tkinter-9cf)
![DB](https://img.shields.io/badge/DB-MySQL-orange)

# Hotel Booking Analysis & ETL Dashboard

**An end-to-end data analysis tool developed to derive actionable insights from over 119,000 hotel booking records.**

Unlike standard analysis scripts, this is a fully interactive **Desktop Application** built with **Tkinter**. It functions as a complete **ETL (Extract, Transform, Load)** pipeline.

---

## Project Overview

This application manages the full data lifecycle:

1.  **Extract:** Ingests raw CSV data (`hotel_booking.csv`).
2.  **Transform:** Uses **Pandas** for data cleaning, seasonality calculation, and demographic segmentation.
3.  **Load:** Persists processed insights into a **MySQL Database** to ensure data integrity.
4.  **Visualize:** Generates interactive **Matplotlib** charts for business intelligence.
5.  **Export:** Allows users to query the SQL database and export specific reports back to CSV.

---

## Key Features

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

## Tech Stack

* **Language:** Python 3.x
* **Data Processing:** Pandas, NumPy
* **Visualization:** Matplotlib
* **GUI Framework:** Tkinter
* **Database:** MySQL (via `mysql-connector-python`)

---

## Installation & Setup

Follow these steps to set up the project locally.

### 1. Prerequisites
Ensure you have Python installed along with a local MySQL server. Install the required Python libraries:

```bash
pip install pandas matplotlib mysql-connector-python
```

### 2. Database Configuration
**Crucial Step:** Before running the app, you must initialize the database structure.


1.  **Create the Database & Import the Schema:**
    A `Database.sql` file is provided in this repository. It contains the code to create all necessary tables (`basic_statistics`, `monthly_distribution`, `booking_trends`, etc.).

    * **Via MySQL Workbench:** Go to *Server -> Data Import -> Select `Database.sql` -> Target Schema: `Hotel_booking_analysis`*.
    * **Via Command Line:**
        ```bash
        mysql -u root -p Hotel_booking_analysis < Database.sql
        ```

### 3. Connection Setup
Open `main.py` and update the database credentials to match your local setup:

```python
mydb = mysql.connector.connect(
    host='localhost',
    user='root',       # Change to your MySQL username
    password='root',   # Change to your MySQL password
    database='Hotel_booking_analysis'
)
 ```

 ### 4. Running the App
1.  **Download the Data:** Ensure the `hotel_booking.csv` dataset is present in the **root directory** (the same folder as `main.py`).
2.  **Launch the Dashboard:**
    ```bash
    python main.py
    ```
3.  **Interact:** A GUI window will appear. Click on the menu buttons (e.g., "Select Hotel" and then "Guest Type Distribution") to visualize data. The application will automatically insert/update the SQL tables with the latest results upon every calculation.

---

## UI Examples

### Main Menu
![Main Menu Screenshot](path/to/your/screenshot1.png)


### Booking Trends
![Booking Trends Screenshot](path/to/your/screenshot2.png)


---

## Developed By:

**Vasilopoulos Panagiotis**
Computer Engineering and Informatics Department (CEID)
University of Patras

> **Note:** This project is for educational purposes and demonstrates the ability to build data-driven GUI applications and manage SQL pipelines via Python.
