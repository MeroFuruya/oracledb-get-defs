import json

IN = "all_tab_cols.json"
OUT = "all_table_names.json"

with open(IN, "r") as f:
    data_in = json.load(f)
    f.close()

data_out = []

for field in data_in:
    if field["TABLE_NAME"].lower() != "EMBARCADERO_EXPLAIN_PLAN".lower():
        table_name = field["TABLE_NAME"].lower()
        if table_name not in data_out:
            data_out.append(table_name)

with open(OUT, "w") as f:
    json.dump(data_out, f, indent=4)
    f.close()

print("Done.")
