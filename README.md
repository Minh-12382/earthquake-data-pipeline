# 🌍 Global Earthquake Data Pipeline

> Built an end-to-end automated data pipeline for global earthquake data using Python, MySQL, Power BI, and Airflow.

---
## 📊 Dashboard

!![Dashboard_earthquake_NOAA](https://github.com/user-attachments/assets/0172b9a0-bf6c-4c6a-93c3-2b34944e22ba)

## 📌 Overview
This project builds an end-to-end data pipeline to collect, process, and analyze global earthquake data from multiple reliable sources.

The goal is to transform raw seismic data into structured datasets for analysis and visualization.

---

## 🏗️ Architecture
Data is collected from public sources and processed through an automated pipeline:

Data Sources (NOAA, GFZ)
        ↓
Python ETL (cleaning & transformation)
        ↓
MySQL Data Warehouse
        ↓
Power BI Dashboard
        ↓
Airflow (automation & scheduling)

---

## 📊 Data Sources
- NOAA (National Oceanic and Atmospheric Administration)
- GFZ (German Research Centre for Geosciences)

Datasets include:
- Earthquake events
- Tsunami events
- Volcano data

---

## ⚙️ Pipeline
- Extract: Load raw CSV data from multiple sources  
- Transform: Clean, standardize, and merge datasets using Python  
- Load: Store structured data into MySQL Data Warehouse  
- Automate: Schedule and monitor pipeline using Apache Airflow  

---

## 📈 Dashboard
Power BI dashboards were built to explore:

- Earthquake distribution by region  
- Magnitude and depth patterns  
- Frequency trends over time  

---

## 🔍 Key Insights
- Earthquakes are concentrated along tectonic plate boundaries  
- Most earthquakes are low to medium magnitude  
- Countries like Japan and Indonesia experience the highest frequency of strong earthquakes  

---

## 🛠 Tech Stack
- Python  
- SQL (MySQL)  
- Apache Airflow  
- Power BI  

---

## 🚀 Future Improvements
- Integrate real-time streaming data  
- Improve data modeling and scalability  
- Enhance visualization and interactivity  

---

## 🔗 Project Resources
- Dashboard:
### NOAA Data
![Dashboard_earthquake_NOAA](https://github.com/user-attachments/assets/4874902f-3756-4000-9ffd-2125d5ce74d0)

### GEO Data
![GEO Dashboard](dashboard/geo.png)(https://github.com/user-attachments/assets/27567d40-0f4c-4d2e-b5c7-e4db34e43af0)

- Source code: [link]
## 🔗 Project Resources
[run_etl_source_dims_fact.py](https://github.com/user-attachments/files/26311088/run_etl_source_dims_fact.py)
[run_etl_geophon_source_dims_fact.py](https://github.com/user-attachments/files/26311104/run_etl_geophon_source_dims_fact.py)
[full_earthquake_pipeline_dag.py](https://github.com/user-attachments/files/26311185/full_earthquake_pipeline_dag.py)


## 👤 Author
Minh Nguyen  
Aspiring Data Engineer & Data Analyst

