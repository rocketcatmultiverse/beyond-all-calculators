#converts json_dump widget into 1 file to be consumed.
import glob
import json
read_files = glob.glob("/data/json_dump/*.json")
output_list = []
for f in read_files:
  with open(f, "rb") as infile:
    print(json.load(infile))
    #output_list.append(json.load(infile))
