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
├── pipeline.py
├── Assignment.ipynb
├── Assignment.pdf
├── Report.pdf
├── aviation_data.csv
├── generate_report.py
├── README.md
├── requirements.txt
```

## Requirements

- Python 3.x
- Jupyter Notebook (if manually running the notebook)
- Required Python libraries (listed in `requirements.txt`)
- MySQL Server (for database setup)
- VS Code

---

## Automated Setup and Execution (Recommended)

For a streamlined process, the `pipeline.py` script automates the setup, execution, and report generation.

### Steps for Automated Pipeline:

1. **Clone the Repository**:

   First, clone the project repository from GitHub:

   ```bash
   git clone https://github.com/viseshagarwal/Akasa-Air-Analytics-Assignment.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd Akasa-Air-Analytics-Assignment
   ```

3. **Run the `pipeline.py` Script**:

   Now, simply run the `pipeline.py` file:

   ```bash
   python pipeline.py
   ```

### What the `pipeline.py` Script Does:

- **Virtual Environment**: It creates and activates a virtual environment.
- **Dependency Installation**: Automatically installs all necessary dependencies using `requirements.txt`.
- **Environment Setup**: It will prompt you to enter your MySQL database credentials and create a `.env` file based on your inputs.
- **Jupyter Notebook / VS Code**: It will try to launch Jupyter Notebook. If Jupyter is not installed, it will automatically open VS Code, allowing you to run the notebook manually.
- **Report Generation**: After executing the notebook, the script will generate an HTML report (`aviation_report.html`) in the `reports/` directory and open it in your browser.

### Outcome:

After running the `pipeline.py` script:

- All necessary steps, including setting up the virtual environment, installing dependencies, and running the notebook, will be handled.
- The generated HTML report (`aviation_report.html`) will open automatically in your default browser, summarizing the analysis and visualizations.

---

## Manual Setup and Execution (if `pipeline.py` fails)

In case the `pipeline.py` script fails or you prefer to manually run the project, follow these steps:

### Step 1: **Set Up a Virtual Environment**

1. Navigate to the project directory:

   ```bash
   cd Akasa-Air-Analytics-Assignment
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

### Step 2: **Install Dependencies**

With the virtual environment activated, install the required Python packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Step 3: **Set Up the `.env` File**

1. Copy the `.env.example` file to create a `.env` file:

   ```bash
   cp .env.example .env
   ```

2. Open the `.env` file and add your MySQL database credentials:
   ```plaintext
   DB_USER=""
   DB_PASSWORD=""
   DB_HOST=""
   DB_NAME=""
   DB_PORT=""
   ```

### Step 4: **Database Setup**

Ensure that your MySQL server is running and that you have created the necessary database with the same name as in the `.env` file. The database should contain the data for this analysis.

### Step 5: **Run the Jupyter Notebook**

1. Start the Jupyter Notebook server from your terminal:

   ```bash
   jupyter notebook
   ```

2. Open `Assignment.ipynb` and execute the cells step by step:
   - The notebook performs data loading, cleaning, and normalization.
   - Visualizes key insights using `matplotlib` and `seaborn`.
   - Saves visualizations (e.g., bar charts, histograms) as `.png` files in the `reports/` folder.

### Step 6: **Generate the HTML Report**

After completing the analysis in the notebook:

1. Run the `generate_report.py` script to generate the HTML report:

   ```bash
   python generate_report.py
   ```

2. The report will be saved as `aviation_report.html` in the `reports/` directory. Open it in your browser to view the analysis.

---

## Notes

- If Jupyter Notebook is not installed, you can manually execute the notebook using VS Code or any other Python IDE.
- Ensure that your MySQL server is running and the necessary database is created before running the scripts.

---

## Disclaimer

This project is an assignment for Akasa Air and is intended for educational purposes only. The data used in this project is for demonstration purposes and does not reflect actual data from Akasa Air or any Airline.

---
