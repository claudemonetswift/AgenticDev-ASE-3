from collections import defaultdict
import json
import csv
import os
import numpy as np

context_related = {"java": {1: "1a, 1b, 2a, 2b", 2: "2a, 2b, 2c, 2d", 3: "2a, 2b, 2c, 2d", 4: "3a, 3b, 3c", 5: "3a, 3b"},
        "py": {1: "1a, 1b", 2: "2a, 2b", 3: "", 4: "2a, 2b", 5: "2a, 2b, 2c, 2d, 2e, 2f, 2g, 2h, 3a, 3b, 3c"},
        "cpp": {1: "", 2: "3a, 3b, 3c", 3: "3a, 3b", 4: "", 5: "2a"} 
}

context_total_points = { #"java": {1: 6, 2: 4, 3: 5, 4: 4, 5: 3},
        "java": {
            1: {"1": 3, "2": 3},
            2: {"2": 4},
            3: {"2": 5},
            4: {"3": 4},
            5: {"3": 3}
        },

        "py": {
               1: {"1": 2, "2": 2}, 
               2: {"2": 2},
               3: {}, 
               4: {"2": 2},
               5: {"2": 5, "3": 3}}, 
        "cpp": {
            1: {},
            2: {"3": 3},
            3: {"3": 3},
            4: {},
            5: {"2": 1}
        } 
}


def calculate_score(rubric, r_deducted, lang, sample_num):
    #print(lang, sample_num, r_deducted)
    totals = {}
    points = {}
    for i, rubric_item in enumerate(rubric):
        r_number = i+1

        if not str(r_number) in context_related[lang][sample_num]: continue

        totals[r_number] = context_total_points[lang][sample_num][str(r_number)]
        points[r_number] = context_total_points[lang][sample_num][str(r_number)]


        '''
        #print(rubric_item)
        for i, subitem in enumerate(rubric_item["subitems"]):

            r = str(r_number) + chr(i + ord('a'))

            if not r in context_related[lang][sample_num]: 
                totals[r_number] -= subitem["points"] 
                points[r_number] -= subitem["points"]

                #continue
            #print(subitem["points"])

            #totals[r_number] += subitem["points"] 
            #points[r_number] += subitem["points"]
        '''

    if r_deducted:
        for rubric_item_deducted in r_deducted.split(","):
            #print(rubric_item_deducted)
            r_number = int(rubric_item_deducted[0]) #index from 0

            if not rubric_item_deducted in context_related[lang][sample_num]:
                continue

            points_to_deduct = get_points_from_ritem(rubric, rubric_item_deducted)
            #print(r_number+1, "-",points_to_deduct)
            points[r_number] -= points_to_deduct
            #print("deducting", points_to_deduct)
            #print(points[r_number])

    score = 0
    for total, point in zip(totals.items(), points.items()):
        #print(point, "/", total)
        score += float(point[1]) / float(total[1])

    #print(score, len(totals))
    return score / len(totals)  if len(totals) > 0 else 0

def get_points_from_ritem(rubric, r_item):
    assert len(r_item) == 2

    r_number = int(r_item[0])-1 #index from 0
    sub_item = ord(r_item[1])-ord('a')

    return rubric[r_number]["subitems"][sub_item]["points"]

data = {}
all_lang_scores = defaultdict(list)
for LANG in  ["java", "py", "cpp"]:  #["java", "py"]: #, "cpp"]:
    all_q_scores = defaultdict(list)

    for SAMPLE_NUM in range(1,6): #range(1,6): #6):
        f_csv = f"{LANG}{SAMPLE_NUM}.csv"
        f_results = f"../results/rubric-applications/csvs/{f_csv}"
        f_rubrics = f"../dataset/{LANG}/rubrics/{SAMPLE_NUM}.json"
        if not os.path.exists(f_results):
            continue

        rubric = json.load(open(f_rubrics))

        all_scores = defaultdict(list)

        with open(f_results) as f:
            reader = csv.reader(f)

            next(reader)

            for row in reader:
                model = row[0]
                trial_num = row[1]
                r_deducted = row[2]
                
                all_scores[model].append(calculate_score(rubric, r_deducted, LANG, SAMPLE_NUM))


        '''
        Calculate performance change on rubric items that require context

        '''

        max_key_length = max(len(str(k)) for k in all_scores.keys())

        print("--------------------------------------")
        print("Rubric Related Performance Change for question:", LANG, str(SAMPLE_NUM))
        
        averages = []
        for k, v in all_scores.items():
            if k.startswith("Agentic"):
                for i in range(0, len(v), 3):
                    group = v[i:i+3]
                    if len(group) == 3:
                        average = sum(group) /3
                        averages.append(("Trial " + str(i// 3+1) , average))
                        all_q_scores[k].append(average)
                        all_lang_scores[k].append(average)

            else:
                average = sum(v) / len(v)
                averages.append((k, average))
                all_q_scores[k].append(average)
                all_lang_scores[k].append(average)


        #averages.sort(key=lambda x: (-round(x[1], 4), x[0]))
        averages.sort(key=lambda x: x[0], reverse=False)
        data[f"{LANG}{SAMPLE_NUM}"] = {}

        claude_avg = averages[0][1]
#        data[f"{LANG}{SAMPLE_NUM}"]["Claude No Tools"] = round(claude_avg, 2)
        print(f"Claude Opus 4: {claude_avg:.2%}")

        agentic_avg = sum([v[1] for v in averages[1:]])/3
        if agentic_avg == claude_avg:
            data[f"{LANG}{SAMPLE_NUM}"][f"Difference ({k})"] = 0.0
            print(f"Agentic Claude Opus 4: {agentic_avg:.2%}")
            print("NO CHANGE")
        else:
            for k, average in averages[1:]:
                diff = average - claude_avg
                data[f"{LANG}{SAMPLE_NUM}"][f"Difference ({k})"] = round(diff, 2)
                print(f"Agentic Claude Opus 4 ({k}): {average:.2%} ({diff:.2%})")

#with open("rubric_based_performances.json", "w") as file:
#    json.dump(data, file, indent =4)




