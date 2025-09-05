
import pandas as pd
import os
import argparse
from openpyxl import Workbook

# === CLI Arguments ===
parser = argparse.ArgumentParser(description="Validación LATAM por país")
parser.add_argument('--market', type=str, required=True, help='Market to process: ARG, PE, MX, EC, HTC')
args = parser.parse_args()

market = args.market.upper()
base_input = "Input"
output_dir = "Output"
os.makedirs(output_dir, exist_ok=True)

market_parts = {
    'ARG': ['Part1'],
    'EC': ['Part1'],
    'HTC': ['Part1'],
    'PE': ['Part1', 'Part2'],
    'MX': ['Part1', 'Part2', 'Part3', 'Part4']
}

file_map = {
    'volume': ('volume_sales', 13),
    'revenue': ('revenue_sales', 13),
    'transactions': ('stddisc_transaction', 14)
}

def process_file_chunked(filepath, col_idx):
    chunks = pd.read_csv(filepath, header=None, chunksize=500_000)
    result = {}
    for chunk in chunks:
        chunk = chunk.dropna(subset=[0, col_idx])
        chunk[col_idx] = pd.to_numeric(chunk[col_idx], errors='coerce')
        for date, value in chunk.groupby(0)[col_idx].sum().items():
            result[date] = result.get(date, 0) + value
    return pd.DataFrame(list(result.items()), columns=["Día", "Valor"])

writer_df = None

for metric, (pattern, col_idx) in file_map.items():
    dfs = []
    part_dirs = [os.path.join(base_input, p) for p in market_parts.get(market, [])]

    for part in part_dirs:
        if not os.path.isdir(part):
            print(f"⚠️ Folder {part} not found.")
            continue
        matched_file = next((f for f in os.listdir(part) if pattern in f.lower()), None)
        if not matched_file:
            print(f"⚠️ No file matching {pattern} in {part}")
            continue

        print(f"📄 Processing {matched_file} from {part} for {metric}")
        filepath = os.path.join(part, matched_file)
        df = process_file_chunked(filepath, col_idx)
        dfs.append(df)

    if not dfs:
        print(f"❌ No data for {metric} in {market}")
        continue

    if market == 'PE' and len(dfs) == 2:
        combined = pd.merge(dfs[0], dfs[1], on="Día", how='outer').fillna(0)
        combined["Valor"] = combined.iloc[:, 1] + combined.iloc[:, 2]
        df_final = combined[["Día", "Valor"]]
    else:
        df_final = pd.concat(dfs).groupby("Día")["Valor"].sum().reset_index()

    df_final.rename(columns={"Valor": metric}, inplace=True)
    if writer_df is None:
        writer_df = df_final
    else:
        writer_df = pd.merge(writer_df, df_final, on="Día", how="outer")

if writer_df is not None:
    writer_df.sort_values(by="Día", inplace=True)
    excel_path = os.path.join(output_dir, f"validation_report_{market}.xlsx")
    writer_df.to_excel(excel_path, index=False)
    print(f"✅ Report saved to: {excel_path}")
else:
    print("❌ No data was processed.")
