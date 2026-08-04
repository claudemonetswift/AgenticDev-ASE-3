from pathlib import Path
import pandas as pd
import csv
import numpy as np
from collections import defaultdict
from scipy.stats import spearmanr, mannwhitneyu


# ============================================================
# Files
# ============================================================

CONTEXT_CSV = "context_stats.csv"
CSV_DIR = Path("../results/rubric-applications/csvs")


# ============================================================
# Hallucination rubric items
# ============================================================

HALLUCINATION_ITEMS = {

    "cpp1": {"1b","2a","2b","2c","3a"},
    "cpp2": {"1b","2c","3c"},
    "cpp3": {"1b","2c"},
    "cpp4": {"1b","2b","3b","4b","4c"},
    "cpp5": {"1b","2b"},

    "py1": {"1b","2b"},
    "py2": {"1b","2b"},
    "py3": {"2b"},
    "py4": {"1b"},
    "py5": {"1b","4b"},

    "java1": {"1b","2b","3b"},
    "java2": {"2d"},
    "java3": {"1b","2b","2c"},
    "java4": {"1b","1c","1d","1e","1f","2b","3c"},
    "java5": {"1b","2b","2c","2d","2e","2f","2g","3b","4b"},
}



def normalize_name(x):

    x = (
        x.lower()
        .replace(" ", "")
    )

    if x.startswith("python"):
        x = x.replace("python","py")

    return x



def aggregate_trial(x):

    x = int(x)

    if x <= 3:
        return 1
    elif x <= 6:
        return 2
    else:
        return 3



# ============================================================
# Read hallucination CSVs
# ============================================================

hall_raw = defaultdict(list)


for file in CSV_DIR.glob("*.csv"):

    benchmark = normalize_name(file.stem)

    if benchmark not in HALLUCINATION_ITEMS:
        print("Skipping", file.name)
        continue


    with open(file, newline="") as f:

        reader = csv.DictReader(f)

        for row in reader:

            model = (
                "tools"
                if "agentic" in row["model_name"].lower()
                else "no_tools"
            )


            trial = aggregate_trial(row["trial"])


            deducted = row["rubric items deducted"].strip()


            if deducted:

                items = {
                    x.strip().lower()
                    for x in deducted.split(",")
                }

            else:
                items=set()


            total = len(items)

            hallucination = len(
                items &
                HALLUCINATION_ITEMS[benchmark]
            )


            hall_raw[
                (
                    benchmark,
                    model,
                    trial
                )
            ].append(
                (
                    total,
                    hallucination
                )
            )



# Average graders

hall_stats = {}


for key, vals in hall_raw.items():

    avg_total = np.mean(
        [x[0] for x in vals]
    )

    avg_hall = np.mean(
        [x[1] for x in vals]
    )


    hall_stats[key] = {

        "total": avg_total,

        "hall": avg_hall,

        "rate":
            avg_hall /
            max(avg_total,1)

    }



# ============================================================
# Overall hallucination
# ============================================================


print("\n")
print("="*80)
print("OVERALL HALLUCINATION STATISTICS")
print("="*80)


overall = defaultdict(lambda:[0,0])


for key,val in hall_stats.items():

    benchmark,model,trial = key

    overall[model][0] += val["total"]
    overall[model][1] += val["hall"]



for model,name in [
    ("no_tools","Claude Opus 4 (No Tools)"),
    ("tools","Agentic Claude Opus 4 (Tools)")
]:

    total,hall = overall[model]

    print(name)

    print(
        f"  Hallucination share: "
        f"{100*hall/total:.2f}%"
    )

    print(
        f"  Total deductions: {total:.2f}"
    )

    print()



# ============================================================
# Per benchmark/trial
# ============================================================


print("="*80)
print("BENCHMARK + TRIAL HALLUCINATION")
print("="*80)



for benchmark in sorted(HALLUCINATION_ITEMS):

    print("\n",benchmark)

    for trial in [1,2,3]:

        for model in [
            "no_tools",
            "tools"
        ]:

            r = hall_stats.get(
                (
                    benchmark,
                    model,
                    trial
                )
            )

            if r:

                print(
                    f"  Trial {trial} {model}: "
                    f"{r['rate']*100:.2f}%"
                )



# ============================================================
# Where tools increase hallucination
# ============================================================


print("\n")
print("="*80)
print("CASES WHERE TOOLS INCREASE HALLUCINATION")
print("="*80)



for benchmark in sorted(HALLUCINATION_ITEMS):

    for trial in [1,2,3]:

        no = hall_stats.get(
            (
                benchmark,
                "no_tools",
                trial
            )
        )

        tool = hall_stats.get(
            (
                benchmark,
                "tools",
                trial
            )
        )


        if no and tool:

            diff = (
                tool["rate"]
                -
                no["rate"]
            )


            if diff > 0:

                print(
                    f"{benchmark} trial {trial}: "
                    f"{no['rate']*100:.2f}% -> "
                    f"{tool['rate']*100:.2f}% "
                    f"(+{diff*100:.2f} pp)"
                )



# ============================================================
# Load context statistics
# ============================================================


ctx = pd.read_csv(
    CONTEXT_CSV
)



def parse_sample(x):

    x = (
        x.lower()
        .replace(" ","")
    )


    parts = x.split("-")

    benchmark = parts[0]

    if benchmark.startswith("python"):
        benchmark = benchmark.replace(
            "python",
            "py"
        )


    execution = int(parts[-1])

    return benchmark,execution



ctx[
    ["benchmark", "execution"]
] = ctx["sample"].apply(
    lambda x: pd.Series(parse_sample(x))
)



ctx["trial"] = (
    ctx.execution
    .apply(aggregate_trial)
)



ctx["relevant_recall"] = (
    ctx.relevant_read /
    ctx.total_relevant_lines.replace(
        0,
        np.nan
    )
)


ctx["irrelevant_fraction"] = (
    ctx.irrelevant_lines /
    ctx.total_tool_lines.replace(
        0,
        np.nan
    )
)


ctx["duplicate_fraction"] = (
    ctx.duplicate_lines /
    ctx.total_tool_lines.replace(
        0,
        np.nan
    )
)



# Attach hallucination score for tools

ctx["hallucination"] = np.nan


for i,row in ctx.iterrows():

    key = (
        row["benchmark"],
        "tools",
        row["trial"]
    )


    if key in hall_stats:

        ctx.loc[i,"hallucination"] = (
            hall_stats[key]["rate"]
        )



tool_ctx = ctx.dropna(
    subset=[
        "hallucination"
    ]
)



# ============================================================
# Spearman correlations
# ============================================================


print("\n")
print("="*80)
print("RETRIEVAL VS HALLUCINATION SPEARMAN")
print("="*80)



for feature in [

    "total_tool_lines",

    "relevant_recall",

    "irrelevant_fraction",

    "duplicate_fraction"

]:


    data = tool_ctx.dropna(
        subset=[
            feature,
            "hallucination"
        ]
    )


    rho,p = spearmanr(
        data[feature],
        data.hallucination
    )


    print(
        f"{feature}: "
        f"rho={rho:.3f}, "
        f"p={p:.5f}, "
        f"n={len(data)}"
    )



# ============================================================
# Zero retrieval analysis
# ============================================================


print("\n")
print("="*80)
print("ZERO RETRIEVAL VS RETRIEVAL")
print("="*80)



zero = tool_ctx[
    tool_ctx.total_tool_lines == 0
].hallucination


retrieved = tool_ctx[
    tool_ctx.total_tool_lines > 0
].hallucination



print(
    "Zero retrieval mean:",
    zero.mean(),
    "n=",
    len(zero)
)


print(
    "Retrieved mean:",
    retrieved.mean(),
    "n=",
    len(retrieved)
)



if len(zero)>0 and len(retrieved)>0:

    u,p = mannwhitneyu(
        zero,
        retrieved,
        alternative="two-sided"
    )


    print(
        "Mann Whitney p:",
        p
    )
