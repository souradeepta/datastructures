# Contributing

Thank you for improving InterviewPrep. Contributions should make the practice
loop clearer: explain the idea, show a focused implementation where useful, and
test behavior and edge cases.

## Repository layout

- `docs/` — interview guides, indexes, and the system-design catalog.
- `learning-paths/` — schedules and interview playbooks.
- `python/` — educational implementations.
- `tests/` — focused automated tests.
- `scripts/` — repository validation and content-quality checks.

## Before opening a change

Run these commands from the repository root:

```bash
pytest -q
python3 scripts/validate_repo.py --imports
python3 scripts/audit_system_design.py \
  --max-structural-filler 27 \
  --max-copied-capacity 134
```

Add or update focused tests for changed public behavior. Keep tests
deterministic, assert the documented contract, and cover meaningful edge cases.

## Documentation standard

New or substantially revised guides should state their audience and learning
objective, explain complexity and trade-offs, include edge cases or failure
modes, use checked units in calculations, and provide an exercise or practice
prompt. Links in active Markdown must point to real repository paths.

System-design guides are reviewed incrementally. Do not present illustrative
content as production guidance, and do not add generic structural filler or
copy the shared sizing block tracked by `scripts/audit_system_design.py`.
Topic-specific calculations must state assumptions and use consistent units.

Keep pull requests focused and describe what was tested. Do not rewrite the
700+ guide catalog in bulk as part of an unrelated change.
