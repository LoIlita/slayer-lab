---
license: other
language:
- pl
- en
pretty_name: Dataset team submissions
task_categories:
- text-generation
configs:
- config_name: default
  data_files:
  - split: train
    path: data/*/*.parquet
- config_name: cranemath_en
  data_files:
  - split: train
    path: data/cranemath_en/cranemath_en.parquet
- config_name: finemath_4plus_en
  data_files:
  - split: train
    path: data/finemath_4plus_en/finemath_4plus_en.parquet
- config_name: infiwebmath_4plus_en
  data_files:
  - split: train
    path: data/infiwebmath_4plus_en/infiwebmath_4plus_en.parquet
- config_name: stack_edu_python
  data_files:
  - split: train
    path: data/stack_edu_python/stack_edu_python.parquet
---

# Dataset team submissions

Openly licensed Polish and English text that the dataset team submits, one source per directory under `data/`.
It sits beside [Polish Dynaword](https://huggingface.co/datasets/SlayerLab/polish-dynaword) and extends
Dynaword's row schema with 4 columns, with the same rights review and takedown procedure.

## How it differs from Dynaword

- Polish and English, and `pl+en` for mixed text. Dynaword is Polish only.
- Synthetic and machine-translated text is allowed. Every such row names its `generator` (model, revision and
  committed prompt) and, when it derives from other text, its `derived_from`.
- Rows that Dynaword ships are excluded: the Dynaword text keys, upstream hosts and blocklist are pinned in
  `dynaword/` and checked on every source.
- One licence per source is not enough: each row carries its own `license`. The card licence is `other`.

## Rules

Every source passes a rights review before it merges. [AGENTS.md](AGENTS.md) is the contributor guide and
reviewer checklist; [LESSONS.md](LESSONS.md) gives the rules learned from Dynaword's rights review; the
[rights-review skill](.agents/skills/source-rights-review/SKILL.md) is the procedure. In short: a licence on a
platform or compilation is not a licence on the works inside, unverified means not admitted, and every source
has a datasheet that says what was not checked.

## Sources

| Source | Language | Origin | Licence | Documents | Tokens |
|---|---|---|---|---|---|

## Columns

`id`, `text`, `source`, `added`, `created`, `token_count`, `license`, `author`, `language` (`pl`, `en` or
`pl+en`), `text_origin` (`human`, `translated` or `synthetic`), `generator` and `derived_from` (both nullable).
Personal data is masked before a shard is written (`[PHONE]`, `[PII]`, `[PERSON]`).

## Loading at a commit

The data changes with every merge. Cite a commit, not `main`. Record the SHA with your training run. Tags are optional.

```python
from datasets import load_dataset

ds = load_dataset("SlayerLab/dataset-team-submissions", "default", revision="<commit sha>")
```

Pass a source key instead of `default` to load one source once its config exists.

## Takedown

To have a record removed, write to takedown@fabryka.ai. How requests are handled and what has been removed:
[takedown/PROCEDURE.md](takedown/PROCEDURE.md), [takedown/register.md](takedown/register.md).
