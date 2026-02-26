# Docs Deployment (GitHub Pages)

This project deploys docs to `docs.itsor.app` using a GitHub Actions workflow artifact and GitHub Pages.

No dedicated deployment branch (such as `gh-pages`) is used.

## Workflow

- Workflow file: `.github/workflows/docs-deploy.yml`
- Trigger: push to `main` when docs-related files change (plus manual dispatch)
- Build command: `mkdocs build --strict`
- Publish mechanism: `actions/upload-pages-artifact` + `actions/deploy-pages`

## One-time GitHub repository setup

1. Open **Settings → Pages** in the repository.
2. Under **Source**, select **GitHub Actions**.
3. Confirm environment protections (if any) allow deployment to `github-pages`.

## Custom domain (`docs.itsor.app`)

1. In **Settings → Pages**, set **Custom domain** to `docs.itsor.app`.
2. In DNS, create a `CNAME` record:
   - Name: `docs`
   - Target: `<org-or-user>.github.io`
3. Wait for DNS propagation, then verify the site URL is reachable.

## Validation checklist

- Workflow `Docs Deploy` completes successfully on `main`.
- GitHub Pages environment shows latest deployment.
- `https://docs.itsor.app` serves the expected MkDocs content.
