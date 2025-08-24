# Electricity Consumption and Production Analysis

## Overview
The **Electricity Consumption and Production Analysis Application** is a user-friendly desktop application that allows users to visualize and analyze energy consumption and production data. The application provides a graphical interface to load CSV files, display data in a table, and generate various plots for analysis.

This project is ideal for researchers, students, and professionals interested in monitoring and analyzing energy usage trends.

---

## Features
- Load energy data from a CSV file (`electricityConsumptionAndProduction.csv`)
- Display data in a tabular format
- Generate different types of plots:
  - **Line Graph**: Shows Consumption and Production over time
  - **Scatter Plot**: Compares Consumption vs Production
  - **Box Plot**: Displays Production variability by type (Nuclear, Wind, Hydroelectric, Oil and Gas, Coal, Solar, Biomass)
- Save processed data to a new CSV file
- Simple and intuitive GUI with PyQt5

---

## Files
- **`data_analysis_code.py`**: Main Python script for the application  
- **`electricityConsumptionAndProduction.csv`**: Sample dataset used for analysis

---

## Requirements
- Python 3.x
- Libraries:
  - `pandas`
  - `matplotlib`
  - `PyQt5`

Install the required libraries using pip:
```bash
pip install pandas matplotlib pyqt5
