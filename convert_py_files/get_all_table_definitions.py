import json

IN = "all_tab_cols.json"
OUT = "all_table_definitions.json"

with open(IN, "r") as f:
    data = json.load(f)
    f.close()

# in:
# [
#     { <field> },
# ]

# out:
# { tables: [ { <table> fields: [ { <field> }, ] }, ] }

def full() -> dict:
    def create_table(field: dict) -> dict:
        owner = field["OWNER"]
        return { "table_name": table_name, "owner": owner, "fields": {} }

    def create_field(field: dict) -> dict:
        res = {}
        res["data_type"] = field["DATA_TYPE"]

        for k, v in field.items():
            if k not in ["COLUMN_NAME", "DATA_TYPE", "TABLE_NAME", "OWNER"]:
                res[str(k).lower()] = v
        return res


    tables = {}

    for field in data:
        # table_name = field["TABLE_NAME"].lower()
        field_name = field["COLUMN_NAME"].lower()
        if table_name not in tables:
            tables[table_name] = create_table(field)
        tables[table_name]["fields"][field_name] = create_field(field)
    
    return tables

def reduced() -> dict:
    def create_table(field: dict) -> dict:
        return { "fields": {} }
    
    def create_field(field: dict) -> dict:
        return {
            "data_type": field["DATA_TYPE"].lower(),
            "data_length": field["DATA_LENGTH"],
            "nullable": (field["NULLABLE"] == "Y"),
        }
    
    tables = {}
    
    for field in data:
        table_name = field["TABLE_NAME"].lower()
        field_name = field["COLUMN_NAME"].lower()
        if table_name not in tables:
            tables[table_name] = create_table(field)
        tables[table_name]["fields"][field_name] = create_field(field)
    
    return tables

tables = reduced()


with open(OUT, "w") as f:
    json.dump(tables, f, indent=4)
    f.close()

print("Done.")


