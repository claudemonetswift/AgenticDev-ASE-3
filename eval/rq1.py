import json
import os
import csv




def load_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        obj = json.load(f)

    loaded_lines = []

    for fname, lines in obj.items():
        fname = os.path.normpath(fname)

        if isinstance(lines, int):
            loaded_lines.append((fname, lines))

        elif isinstance(lines, list):
            for chunk in lines:
                if isinstance(chunk, int):
                    loaded_lines.append((fname, chunk))
                else:
                    s, e = map(int, chunk.split("-"))
                    for i in range(s, e+1):
                        loaded_lines.append((fname, i))

    #print(loaded_lines)
    return loaded_lines


def load_read_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        obj = json.load(f)

    loaded_lines = []
    obj = obj["lines_read"]

    for entry in obj:
        for fname, lines in entry.items():
            fname = os.path.normpath(fname)

            if isinstance(lines, int):
                loaded_lines.append((fname, lines))

            elif isinstance(lines, list):
                for chunk in lines:
                    if isinstance(chunk, int):
                        loaded_lines.append((fname, chunk))
                    else:
                        s, e = map(int, chunk.split("-"))
                        for i in range(s, e+1):
                            loaded_lines.append((fname, i))

    #print(loaded_lines)
    return loaded_lines

total_relevant_lines_needed = 0
total_relevant_lines_read = 0
total_irrelevant_lines_read = 0
total_lines_read = 0
data = {}


for LANG in ["java", "py", "cpp"]:
    for SAMPLE_NUM in range(1, 6):
        for TRIAL_NUM in range(1, 4):
            RESULTS_PREFIX = os.path.join("results/out/", LANG, str(SAMPLE_NUM))

            f_read = os.path.join(RESULTS_PREFIX, f"Trial{TRIAL_NUM}-lines-read.json")
            if not os.path.exists(f_read): continue

            f_given = os.path.join("given-context", f"{LANG}{SAMPLE_NUM}.json")
            f_relevant = os.path.join("relevant-context", f"{LANG}{SAMPLE_NUM}.json")

            given = set(load_lines(f_given))
            relevant = set(load_lines(f_relevant))
            total_relevant_lines_needed += len(relevant)
            raw_read = load_read_lines(f_read)

            total_lines_read += len(raw_read)
            #print(raw_read)

            read = set(raw_read)

            relevant_lines_read = len(relevant) - len(relevant - read)
            total_relevant_lines_read += relevant_lines_read
            
            duplicate_given = len(read) - len(read - given)
            duplicate_reads = len(raw_read) - len(read)
            duplicate_lines_read = duplicate_given + duplicate_reads

            irrelevant_lines_read = len(raw_read) - relevant_lines_read - duplicate_lines_read
            total_irrelevant_lines_read += irrelevant_lines_read

            recall = relevant_lines_read / len(relevant) if len(relevant) > 0 else 0
            precision = relevant_lines_read / len(raw_read) if len(raw_read) > 0 else 0

            print(f"------{LANG}{SAMPLE_NUM} Trial {TRIAL_NUM}--------")

            print(f"Total lines read: {len(raw_read)}")
            print(f"Total relevant lines: {len(relevant)}")
            print(f"Duplicates lines read: {duplicate_lines_read}")
            print(f"Irrelevant lines read: {irrelevant_lines_read}")
            print(f"Relevant lines read: {relevant_lines_read}")
            print(f"Recall: {recall}")
            print(f"Precision: {precision}")
            print("-"*50)
            data[str(LANG)+ str(SAMPLE_NUM) +  " - Trial " + str(TRIAL_NUM)] = {}
            data[str(LANG)+ str(SAMPLE_NUM) +  " - Trial " + str(TRIAL_NUM)]["Total lines read"] = len(raw_read)
            data[str(LANG)+ str(SAMPLE_NUM) +  " - Trial " + str(TRIAL_NUM)]["Total relevant lines"] = len(relevant) if len(relevant) > 0 else 0
            data[str(LANG)+ str(SAMPLE_NUM) +  " - Trial " + str(TRIAL_NUM)]["Duplicates lines read"] = duplicate_lines_read
            data[str(LANG)+ str(SAMPLE_NUM) +  " - Trial " + str(TRIAL_NUM)]["Irrelevant lines read"] = irrelevant_lines_read
            data[str(LANG)+ str(SAMPLE_NUM) +  " - Trial " + str(TRIAL_NUM)]["Relevant lines read"] = relevant_lines_read
            data[str(LANG)+ str(SAMPLE_NUM) +  " - Trial " + str(TRIAL_NUM)]["Recall"] = recall
            data[str(LANG)+ str(SAMPLE_NUM) +  " - Trial " + str(TRIAL_NUM)]["Precision"] = precision


with open("relevant_lines_stats.json",mode="w") as file:
    json.dump(data, file, indent=4)

print()
print("Total relevant lines needed: ", total_relevant_lines_needed)
print("Total relevant line read: ", total_relevant_lines_read)
print("PERCENTAGE OF RELEVANT LINES READ: ", total_relevant_lines_read / total_relevant_lines_needed)
print("RECALL: ", total_relevant_lines_read / total_relevant_lines_needed)
print("PRECISION: ", total_relevant_lines_read / total_lines_read)
