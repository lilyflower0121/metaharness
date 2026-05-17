# Metaharness IO

This directory contains reusable conventions for publishing metaharness gate results in a human-reviewable static form.

The canonical renderer lives at:

```bash
python3 scripts/render_io.py --contract <contract.yaml> --receipt <receipt.json> --out <site-dir>
```

IO is designed to be derived from a metaharness-enabled repo. It may be published to a public Pages site, a private/internal Pages site, or retained as a CI artifact depending on `io_publication.visibility` and the host repository permissions.

See [`../docs/io-publishing.md`](../docs/io-publishing.md).
