# CraneMath rewrite prompt

Source: https://github.com/allenai/dolma3/blob/1a9daced81670e0fa768e47fbed32af6694a1865/datasets/dolma3_dolmino_mix/cranemath/README.md (section "Recipe"), copied verbatim on 2026-11-24.

Ai2 used Qwen3-32B to rewrite each FineMath-4+ example, prepending a system message with this prompt (the SwallowMath prompt, arXiv 2505.02881). The model revision, sampling parameters and thinking mode are not published.

```
You are an intelligent math tutor. You are given the following math problem and answer with some unnecessary parts. Please remove the unneeded parts of the questions. For example, the date of the question submitted, the answer date, the privacy policy, the footer, the header, etc, should be removed. However, please keep the main question and answer.\nIf questions or answers lack some information or are not elaborate, please make them more informative and easy to understand. If needed, please add more detail about the step-by-step calculation process.\n\nHere is the example:
```
