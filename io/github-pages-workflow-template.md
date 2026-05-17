# Repository-Inherited IO Publisher Template

This is a reference workflow, not enabled by default. Copy it into `.github/workflows/publish-io.yml` only when the generated Pages/artifact will inherit the same repository access boundary as the source repository.

```yaml
name: publish metaharness io

on:
  workflow_dispatch:
    inputs:
      contract:
        description: Contract path
        required: true
        default: contracts/examples/io-publication.repository-inherited.valid.yaml

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  render:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
      - name: Run metaharness suite
        run: python3 scripts/run_metaharness.py --contract "${{ inputs.contract }}" --json > receipt.json
      - name: Render IO
        run: python3 scripts/render_io.py --contract "${{ inputs.contract }}" --receipt receipt.json --out _site
      - uses: actions/upload-pages-artifact@v3
        with:
          path: _site
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: render
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

Security notes:

- IO contracts must use `io_publication.access_model: repository_inherited`.
- Do not use a separate public IO repository for private source repositories.
- If the review audience is narrower or broader than the source repository readers, change the repository/artifact host first; do not encode ad-hoc visibility in the task contract.
- Keep `scripts/render_io.py` in the source repo so every host uses the same sanitizer and receipt format.
