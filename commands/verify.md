---
description: Verify the package (harness + unit tests) and report actual results.
---

Verify the package: $ARGUMENTS

1. Run `bash scripts/verify-harness.sh` and
   `python3 -m unittest discover -s tests`.
2. Report the actual result of each check (PASS/FAIL, counts).
   Never claim a pass that did not run.
3. If a check fails, stop and name the failure. Do not work around
   it by skipping the check.
