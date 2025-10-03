Inventory BI Project
Overview

This project provides a Business Intelligence (BI) solution for managing and analyzing inventory data.
It is designed for academic and professional use, with a focus on data visualization, dashboard creation, and integration with modern BI tools.

Features

Data ingestion from CSV/Excel/Database sources

Automated ETL pipeline for cleaning and transforming raw inventory data

Interactive dashboards for business insights

KPI tracking (e.g., stock levels, sales performance, reorder alerts)

Scalable structure for future expansion

Technologies

Python – Data processing and ETL

Pandas / NumPy – Data analysis

SQL – Database integration

Power BI / Tableau – Visualization (optional)

GitHub – Version control and collaboration

Installation

Clone the repository:

git clone https://github.com/tamircohhen/inventory-bi.git
cd inventory-bi


Create a virtual environment:

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows


Install dependencies:

pip install -r requirements.txt

Usage

Place your raw data files inside the data/ folder.

Run the ETL script:

python src/etl.py


Access the cleaned dataset in the output/ folder.

Use the output file in Power BI or Tableau for dashboards.

Project Structure
inventory-bi/
│
├── data/               # Input data (CSV/Excel/Database exports)
├── output/             # Processed data files
├── src/                # Source code (ETL, utils, processing scripts)
├── notebooks/          # Jupyter notebooks for analysis
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── .gitignore          # Git ignore file

Contribution

Contributions are welcome.
Please follow these steps:

Fork the repository

Create a feature branch (git checkout -b feature-name)

Commit your changes (git commit -m "Description")

Push to the branch (git push origin feature-name)

Open a Pull Request

License

This project is licensed under the MIT License – see the LICENSE
 file for details.
