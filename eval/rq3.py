import csv

ctx = 0.0
tot = 0.0
rel = 0.0
irr = 0.0
fin = 0.0
overhead = 0.0
dup = 0.0
with open("../dataset/cost.csv") as f:
    for r in csv.DictReader(f):
        ctx += float(r["Cost of duplicates"]) + float(r["Cost of irrelevant"]) + float(r["Cost of relevant"])
        tot += float(r["Total"])
        rel += float(r["Cost of relevant"])
        irr += float(r["Cost of irrelevant"])
        dup += float(r["Cost of duplicates"])
        fin += float(r["Final Answer cost"])
        overhead += float(r["Cost of other tool calls"]) + float(r["bg calls Cost"])

print(f"Context retrieval cost: {ctx:.4f}")
print(f"Relevant retrieval cost: {rel:.4f}")
print(f"Irrelevant retrieval cost: {irr:.4f}")


print(f"Relevent Retrieval Percentage: {rel/tot*100:.1f}%")
print(f"Irrelevent Retrieval Percentage: {irr/tot*100:.1f}%")
print(f"Dup Retrieval Percentage: {dup/tot*100:.1f}%")
print("="*50)


print(f"Final Answer cost: {fin:.4f}")
print(f"Overhead cost: {overhead:.4f}")
print(f"Total cost: {tot:.4f}")
print("="*50)

print(f"Context Retrieval Percentage: {ctx/tot*100:.1f}%")
print(f"Final Answer Percentage: {fin/tot*100:.1f}%")
print(f"Overhead Percentage: {overhead/tot*100:.1f}%")
