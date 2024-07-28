from deobf import Deobf
import json
import pathlib

deobf_path = pathlib.Path("src/todeobf.json")

if __name__ == '__main__':
    with open(deobf_path, "r") as pairs_file:
        pairs = json.load(pairs_file)
    key_mappings = {}
    for filename, make_id in pairs.items():
        deobfer = Deobf(filename)
        deobfer.do(makeID=make_id if make_id != "None" else None)
        for k1, v1 in key_mappings.items():
            for k2, v2 in deobfer.key_mapping.items():
                if k1 != k2 and v1 == v2:
                    print(f"The dictionaries have the same value {v1} for different keys {k1}, {k2} -> {filename}")
                    exit()
                if k1 == k2 and v1 != v2:
                    print(f"The dictionaries have the same key {k1} for different values {v1}, {v2} -> {filename}")
                    exit()
        key_mappings |= deobfer.key_mapping
    with open("generated_mapping.json", "w") as gen_map_file:
        json.dump(key_mappings, gen_map_file, indent=2)
