#!/usr/bin/env python
import os
import json
import pandas as pd

os.chdir(os.path.dirname(__file__))
reg_df = pd.read_csv("registry-info.csv")
reg_df.rename(
    columns= {
        "Label for tag": "label",
        "Quantity": "quantity",
        "Link for new": "link",
        "Description": "description",
        "Specifications if buying used": "specs",
        "Deleted": "deleted"
    },
    inplace = True
)

to_json = {}
colnames = [c for c in reg_df.columns if c != "UUID"]
for index, line in reg_df.iterrows():
    to_json[line["UUID"]] = {
        k: line[k] for k in colnames
    }

out_path = os.path.join("..", "src", "assets", "items-info.json")
with open(out_path, "w") as f:
    json.dump(to_json, f)