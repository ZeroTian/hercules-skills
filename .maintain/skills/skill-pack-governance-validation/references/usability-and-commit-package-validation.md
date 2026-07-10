# Lightweight Runtime and Package Validation

```bash
python3 -m unittest discover -s .maintain/tests -p 'test_*.py' -v
python3 .maintain/scripts/validate-skill-pack.py --strict
bash -n init.sh .maintain/scripts/check-package.sh .maintain/scripts/smoke-fresh-clone.sh
git diff --check
.maintain/scripts/check-package.sh
.maintain/scripts/smoke-fresh-clone.sh
```

Confirm `skills/` contains exactly the five paths in
`.maintain/skills/hercules-skill-pack-management/SKILL.md`. Hercules performs
no third-party installation, configuration, or authentication.
