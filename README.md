# The Cost of Context: An Evaluation of Claude Code's Agentic Tool Use on Coding Questions

Code and evaluation scripts for our study measuring how effectively Claude Code retrieves relevant context and at what cost when answering contextualized coding questions from **RubberDuckBench**.

## Summary

We compare Claude Opus 4 in a non-agentic setting (prompt only) against Claude Code (agentic, with Bash tool access) on RubberDuckBench, extended with manual line-level relevance annotations.

**Key findings:**
- Agentic setup improves accuracy only slightly (72.1% vs. 68.5%, +3.65 pts) but costs ~10x more ($0.39 vs. $0.04/execution).
- The agent recalls only 42.6% of relevant lines; 80.6% of lines it reads are irrelevant.
- Recall correlates with better answers (r = 0.56, p < .0001); irrelevant reads don't hurt accuracy but drive up cost (27.5% of total spend).
- Hallucination rates are unaffected by tool access.

## Dataset

We extend RubberDuckBench with manual line-level relevance annotations: for each question, five annotators recorded which lines of the project they consulted to answer it. A line counts as relevant if a majority of annotators flagged it. See the `dataset/` folder for questions, rubrics, and relevance annotations.

## Running the scripts

```bash
python eval/rq1.py # Effectiveness of context retrieval (recall/precision) 
python eval/rq2.py # Agentic vs. non-agentic performance
python eval/rq2_finding_4.py # Precision vs. performance change (Finding 4)
python eval/rq3.py # Cost of agentic context retrieval
python eval/rq4.py # Effect on hallucination rate
```

## Evaluation

[figure5.pdf](https://github.com/user-attachments/files/30759628/figure5.pdf)



Recorded agentic tool-invocation traces and rubric scoring results are in `results/`.
