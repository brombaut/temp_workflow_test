# gh-aw Draft: Repo Health PR Analysis

This is a draft of the equivalent gh-aw source shape for the deterministic PR
analysis workflow.

Do not use this as the first runnable POC yet. Compiling this source currently
creates a normal gh-aw agent workflow, including Copilot token validation and
agent setup, even though the deterministic steps emit `noop`. The runnable POC
therefore lives in:

```text
.github/workflows/repo-health-pr-analysis.yml
```

The gh-aw version becomes useful after either:

- the workflow actually asks an agent to interpret the report, or
- gh-aw supports a cleaner deterministic/no-agent workflow mode for this shape.

```md
---
name: Repo Health PR Analysis
description: Deterministic POC that runs repo-analysis on PR base and head commits and publishes comparison artifacts.
on:
  pull_request:
    types: [opened, synchronize, reopened]
    paths:
      - "**/*.py"
      - "pyproject.toml"
      - "requirements*.txt"
      - "setup.py"
      - "setup.cfg"
  workflow_dispatch:
permissions:
  contents: read
  pull-requests: read
safe-outputs:
  noop:
steps:
  - name: Checkout base commit
    uses: actions/checkout@v4
    with:
      path: base
      ref: ${{ github.event.pull_request.base.sha || github.sha }}
      fetch-depth: 0
      persist-credentials: false

  - name: Checkout head commit
    uses: actions/checkout@v4
    with:
      path: head
      ref: ${{ github.event.pull_request.head.sha || github.sha }}
      fetch-depth: 0
      persist-credentials: false

  - name: Checkout repo analyzer
    uses: actions/checkout@v4
    with:
      repository: PGCodeLLM/code-health
      path: analyzer
      ref: main
      token: ${{ secrets.REPO_ANALYSIS_TOKEN || github.token }}
      persist-credentials: false

  - name: Analyze base commit
    run: |
      set -euo pipefail
      python analyzer/analyze.py \
        --output /tmp/repo-analysis/output/base \
        base

  - name: Analyze head commit
    run: |
      set -euo pipefail
      python analyzer/analyze.py \
        --skip-build \
        --output /tmp/repo-analysis/output/head \
        head

  - name: Compare outputs and skip agent
    run: |
      set -euo pipefail
      BASE_JSON="$(find /tmp/repo-analysis/output/base -name '*_codehealth_analysis_*.json' | sort | tail -1)"
      HEAD_JSON="$(find /tmp/repo-analysis/output/head -name '*_codehealth_analysis_*.json' | sort | tail -1)"
      python analyzer/scripts/compare-pr-analysis.py \
        --base "$BASE_JSON" \
        --head "$HEAD_JSON" \
        --output /tmp/repo-analysis/report.md \
        --top 10
      cat /tmp/repo-analysis/report.md >> "$GITHUB_STEP_SUMMARY"
      echo '{"type":"noop","message":"Deterministic repo health report generated; no agent interpretation requested."}' >> "$GH_AW_SAFE_OUTPUTS"

post-steps:
  - name: Upload analysis artifact
    uses: actions/upload-artifact@v4
    if: always()
    with:
      name: repo-health-pr-analysis-${{ github.event.pull_request.number || github.run_id }}
      path: |
        /tmp/repo-analysis/output/base/
        /tmp/repo-analysis/output/head/
        /tmp/repo-analysis/report.md
      retention-days: 14
---

# Repo Health PR Analysis

This workflow intentionally does not ask an agent to interpret the report.
```
