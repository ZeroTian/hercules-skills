# Hercules maintainer boundary

Public runtime behavior lives in `init.sh` and the five Skills under `skills/`. Repository governance, historical records, tests, and packaging tools stay under `.maintain/`.

## Contributor checks

```bash
python3 .maintain/scripts/validate-skill-pack.py --strict
python3 .maintain/tests/test_init.py -v
python3 .maintain/tests/test_runtime_skill_contract.py -v
python3 .maintain/tests/test_validate_skill_pack_cli.py -v
.maintain/scripts/smoke-fresh-clone.sh
.maintain/scripts/check-package.sh
```

Collaboration records and repository guidance live in [`docs/ai-collaboration/`](docs/ai-collaboration/).
