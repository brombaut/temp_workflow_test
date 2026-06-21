# Repo Analysis Workflow Test

Small Python repository for testing the repo-analysis PR workflow.

The workflow in `.github/workflows/repo-health-pr-analysis.yml` checks out a PR
base commit and head commit, checks out the analyzer repository, runs the
analyzer on both revisions, compares the JSON outputs, writes a markdown report
to the GitHub Actions step summary, and uploads raw artifacts.

The source files intentionally contain code-health and AI-slop patterns so the
analyzer has findings to report.

There is also a gh-aw draft in `docs/repo-health-pr-analysis-gh-aw-draft.md`.
It is documentation only for now. The first runnable POC uses plain GitHub
Actions because the compiled gh-aw form still performs agent/Copilot setup even
when the deterministic steps emit `noop`.

## Analyzer Checkout

The workflow currently checks out:

```yaml
repository: PGCodeLLM/code-health
ref: main
```

If that repository is private, add a repository secret named
`REPO_ANALYSIS_TOKEN` with read access to `PGCodeLLM/code-health`.

## Local Smoke Test

From this repository, after the analyzer repository exists at
`../repo-analysis-prototype` or another local path:

```bash
python ../repo-analysis-prototype/analyze.py \
  --output /tmp/repo-analysis/output/head \
  .
```

## PR Test Shape

1. Push this repository to GitHub.
2. Commit the current files to `main`.
3. Create a branch that makes `src/workflow_sample/processor.py` worse.
4. Open a pull request.
5. Inspect the workflow step summary and uploaded artifact.
