# AC Data Validation

Python scripts to validate monthly sales data. The scripts read CSVs, aggregate totals, and export Excel reports.

## How it works
- Reads three CSVs: **Volume**, **Revenue**, and **Transactions**
- Groups by date to calculate totals
- For Mexico:
  - Filters client `231013` (Vending)
  - Splits Vending by SKU (Volume only)
- Exports Excel reports with multiple sheets

## Run locally
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. **For Mexico (Parts 1–4 sample data included):**
   ```bash
   python src/validate_All_MX.py --completo
   ```

3. **For LATAM (sample data included, e.g. PE):**
   ```bash
   python src/validate_All_LATAM.py --market PE
   ```

Excel files are created in each `Output/` folder.

## Repo layout
```
src/                     # Python scripts
  validate_All_MX.py
  validate_All_LATAM.py
DataValidationMX/        # Sample input data (Parts 1–4)
  Input/
  Output/                # Generated Excel reports (ignored by git)
DataValidationLATAM/     # Sample input data
  Input/
  Output/                # Generated Excel reports (ignored by git)
requirements.txt
LICENSE
README.md
```

## Notes
- Client ID is column **2** in the CSV and must include `231013` for Vending sections.
- Metrics:
  - **Column 13** → Volume & Revenue
  - **Column 14** → Transactions
- Sample data is synthetic and included for demonstration.
