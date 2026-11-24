"""Contract for cranemath_en: canonical schema, non-empty text, positive token counts, uniform source, a per-row
licence that is never empty, unique ids, every row synthetic with a generator and derived_from, and stats consistent
with the rows."""
import json
from pathlib import Path

import pyarrow.parquet as pq
import pytest

import shard

KEY = "cranemath_en"
D = Path(__file__).resolve().parent.parent / "data" / KEY


@pytest.fixture(scope="module")
def table():
    p = D / f"{KEY}.parquet"
    if not p.exists():
        pytest.skip(f"{p} not built")
    return pq.read_table(p)


def test_contract(table):
    assert table.schema.equals(shard.SCHEMA)
    rows = table.to_pylist()
    assert rows
    assert all(r["text"].strip() for r in rows)
    assert all(r["token_count"] > 0 for r in rows)
    assert {r["source"] for r in rows} == {KEY}
    assert all(r["license"] and r["license"].strip() for r in rows)
    assert len({r["id"] for r in rows}) == len(rows)
    assert all(r["text_origin"] == "synthetic" and r["generator"] and r["derived_from"] for r in rows)
    assert all("<think>" not in r["text"] for r in rows)
    stats = json.loads((D / f"{KEY}.stats.json").read_text(encoding="utf-8"))
    assert stats["docs"] == len(rows)
    assert stats["tokens"] == sum(r["token_count"] for r in rows)
