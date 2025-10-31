# NASA-CEA Mole Fraction Parser

This Python script is designed to streamline the analysis of output from the NASA Chemical Equilibrium with Applications ($\text{CEA}$) tool by converting complex, fixed-format text into a clean, machine-readable spreadsheet.

The primary goal is to enable **faster data processing** and **clearer visualization** of mole fractions across large solution sets.

## ✨ Key Features & Benefits

- **Automation:** Automatically locates and extracts all instances of the "MOLE FRACTIONS" data blocks.
- **High-Volume Ready:** Supports large input vectors (multiple pressures and temperatures), allowing your $\text{CEA}$ input to contain many more steps for a higher resolution plot.
- **Structured Output:** Aggregates fragmented data into a single table, ready for plotting software.

## 📊 Output File Structure

The final output is a single `.csv` or `.xlsx` (.xlsx by default) file designed for direct import into tools like LibreOffice Calc or Excel.

| Column Name      | Description                                                                                                                    |
| :--------------- | :----------------------------------------------------------------------------------------------------------------------------- |
| **Index Column** | Contains the name of the chemical species (e.g., $\text{CH}_4$, $\text{CO}$, $\text{H}_2\text{O}$).                            |
| **Data Columns** | Contains the mole fraction value for each unique combination of input conditions (e.g., $P_1, T_1, P_1, T_2, P_2, T_1$, etc.). |

The total number of data columns will equal the total number of conditions (e.g., $5$ pressures $\times$ $5$ temperatures $= 25$ columns).

## ⚙️ Configuration (User Steps)

Before running the script, the user only needs to ensure their $\text{CEA}$ output file is placed in the project directory and change the following variables inside the Python script:

1.  `cea_out_file`: Path to your $\text{CEA}$ output file (e.g., `'./my_cea_run.out'`).
2.  `EXPORT_FILENAME`: The desired name of the output file (e.g., `'combustion_data'`).
3.  `FILE_EXTENSION`: Select either `'csv'` or `'xlsx'` (default).

## ⚠️ Important Note on Headers

The script only processes the data output. It will be up to the user to manually add the corresponding **Temperature** and **Pressure** headers above the columns in the exported spreadsheet. This is easily done by inputting the values once and copying them across the required number of columns.

---

## 🚀 Setup & Usage

### 1. Installation

1.  **Navigate** to the project directory in your terminal.
2.  **Create** a virtual environment:
    ```bash
    python -m venv .venv
    ```
3.  **Activate** the environment:
    ```bash
    source .venv/bin/activate
    ```
4.  **Install** dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### 2. Run the Script

With the virtual environment active and your input file configured:

```bash
python nasa_cea_parser.py
```
