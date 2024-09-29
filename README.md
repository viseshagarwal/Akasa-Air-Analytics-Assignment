# Akasa Air Analytics Assignment

## Overview

This repository contains the analytics assignment for Akasa Air. The project primarily uses Jupyter Notebooks for data analysis and Python for scripting.

## Project Structure

The project is structured as follows:

```plaintext
Akasa-Air-Analytics-Assignment/
│
├── datasets/
│   ├── aviation_data_cleaned.csv
│   ├── normalized_data.csv
│
├── reports/
│   ├── average_delay_airline.png
│   ├── average_delay_hour.png
│   ├── delay_distribution.png
│   ├── departure_vs_delay.png
│   └── aviation_report.html
│
├── .env.example
├── .gitignore
├── Assignment.ipynb
├── aviation_data.csv
├── generate_report.py
├── README.md
├── requirements.txt
```

## Requirements

- Python 3.x
- Jupyter Notebook
- Required Python libraries (listed in requirements.txt)

## Installation

### Step 1: **Set Up a Virtual Environment**

1. Clone the repository:

```bash

git clone https://github.com/viseshagarwal/Akasa-Air-Analytics-Assignment.git

```

2. Navigate to the project directory:

```bash

cd Akasa-Air-Analytics-Assignment

```

3. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

5. Now that the virtual environment is activated, install the project dependencies.

### Step 2: **Install Dependencies**

With the virtual environment activated, install the required Python packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Step 3: **Set Up the `.env` File**

1. You have an `.env.example` file that serves as a template for the `.env` file. Rename `.env.example` to `.env`:

   ```bash
   cp .env.example .env
   ```

2. Open `.env` and add your MySQL database credentials:
   ```env
   DB_USER=""
   DB_PASSWORD=""
   DB_HOST=""
   DB_NAME=""
   DB_PORT=""
   ```

These environment variables will be loaded automatically by `python-dotenv` and used to connect to your database.

### Step 4: **Database Setup**

Ensure that your MySQL server is running and that you have created the necessary database with the same name as in the `.env` file. The database should contain the data for this analysis.

### Step 5: **Running the Jupyter Notebook**

1. Start the Jupyter Notebook server from your terminal:

   ```bash
   jupyter notebook
   ```

2. Open `Assignment.ipynb` and execute the cells step by step:

   - The notebook performs data loading, cleaning, and normalization.
   - It visualizes key insights using `matplotlib` and `seaborn`.
   - The visualizations (e.g., bar charts, histograms) are saved as `.png` files in the `reports/` folder.

3. Once you've completed the analysis, make sure all cells have been run successfully. The output visualizations will automatically be saved in the `reports/` folder.

### Step 6: **Generating the HTML Report**

After completing the analysis in the notebook, you can generate a comprehensive HTML report.

1. Run the `generate_report.py` script:

   ```bash
   python generate_report.py
   ```

2. The script will produce an HTML file (`aviation_report.html`) in the `reports/` directory, which contains:
   - A summary of data cleaning and normalization steps.
   - Visualizations, such as the average delay per airline, delay distribution, and more.
   - Key insights and recommendations based on your analysis.

---
