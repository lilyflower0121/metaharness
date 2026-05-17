# Public Repository Safety Checklist

Use before pushing or publishing content to a public repository.

- [ ] No secrets, tokens, private keys, `.env` files, or credential dumps.
- [ ] No private user data, DMs, customer data, or internal-only workspace paths unless intentionally documented and safe.
- [ ] No proprietary code or license-incompatible material.
- [ ] Repo description and README match the actual contents.
- [ ] Generated artifacts and local caches are ignored or excluded.
- [ ] A lightweight secret scan or filename/content scan was run.
- [ ] The pushed commit hash and GitHub URL were read back after publication.
