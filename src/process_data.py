import pandas as pd
import json

# import tables
trees = pd.read_csv("../data/raw_trees.csv", sep=";")
bloom_range = pd.read_csv("../data/bloom_range.csv")

# set cultivar list to drop. These are not the right tree type
drop = ["SEIBOLDI", "SWEETHEART", "MIYAKO"]

# join the two tables to add defined bloom periods
bloom_include = pd.merge(left=trees, right=bloom_range, on="CULTIVAR_NAME", how="left")
# drop inappropriate cultivars
trees_upload = bloom_include[~bloom_include["CULTIVAR_NAME"].isin(drop)]

# Drop NA cultivar name and coordinates (to prevent issues with map)
trees_upload = trees_upload.dropna(subset=["CULTIVAR_NAME", "Geom"])

# extract coordinates
def as_tuple(s):
    return json.loads(s)["coordinates"]


def get_coord(x, pos):
    return as_tuple(x)[pos]


trees_upload["lon"] = trees_upload.Geom.apply(get_coord, args=[0])
trees_upload["lat"] = trees_upload.Geom.apply(get_coord, args=[1])

# Convert neighbourhood to title case (to match with map geojson)
trees_upload["NEIGHBOURHOOD_NAME"] = trees_upload["NEIGHBOURHOOD_NAME"].str.title()

# save new data
trees_upload.to_csv("../data/processed_trees.csv", index=False)
