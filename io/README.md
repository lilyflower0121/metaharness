# Metaharness IO

This directory contains reusable conventions for publishing metaharness gate results in a human-reviewable static form.

The canonical renderer lives at:

```bash
python3 scripts/render_io.py --contract <contract.yaml> --receipt <receipt.json> --out <site-dir>
```

IO is designed to be derived from a metaharness-enabled repo. It should be published only through a repository-synchronized target: same-repository Pages, same-repository CI artifact, or an internal docs target whose ACL mirrors repository readers.

Task contracts must use:

```yaml
io_publication:
  access_model: repository_inherited
```

See [`../docs/io-publishing.md`](../docs/io-publishing.md).
