import json

IN = "all_tab_cols.json"
OUT = "all_data_types_and_count.json"

with open(IN, "r") as f:
    data_in = json.load(f)
    f.close()

data_out = {}

for field in data_in:
    if field["TABLE_NAME"].lower() != "EMBARCADERO_EXPLAIN_PLAN".lower():
        data_type = field["DATA_TYPE"].lower()
        if data_type not in data_out:
            data_out[data_type] = 0
        data_out[data_type] += 1

with open(OUT, "w") as f:
    json.dump(data_out, f, indent=4)
    f.close()

print("Done.")
