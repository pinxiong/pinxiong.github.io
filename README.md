# xiongpin.dev

Source for my personal site — engineering write-ups from real production work.
Built with [Hugo](https://gohugo.io/) + [PaperMod](https://github.com/adityatelange/hugo-PaperMod),
deployed to GitHub Pages at **https://xiongpin.dev** via GitHub Actions.

**This repository is the single source of truth.** Everything required to build the site is
committed here — content, configuration, theme, and the CI workflow. GitHub does the building,
so no part of the site depends on a particular laptop.

## Publishing an article

```bash
./scripts/new-post.sh "How I Cut EC2 Cold Start by 40%"   # 1. scaffold from the 4-part archetype
hugo server -D                                            # 2. write + preview at localhost:1313
./scripts/publish.sh content/posts/how-i-cut-ec2-cold-start-by-40.md   # 3. un-draft, commit, push
```

Pushing to `master` triggers `.github/workflows/hugo.yml`, which builds the site and deploys it.
Live in about a minute.

**Drafts never go live.** A post with `draft: true` is skipped by the production build, so pushing
work in progress is safe. `publish.sh` tells you about any posts still left in draft.

## Working from another computer

The build runs on GitHub, not locally, so a new machine needs no build tooling at all. Pick
whichever entry point fits the moment:

| Situation | How | Local install required |
|---|---|---|
| Quick text edit | Open the repo on github.com, or press `.` for github.dev, and commit from the browser | none |
| Full writing session, any machine | **GitHub Codespaces** — the dev container provisions Hugo automatically | none |
| Your own Mac / Linux box | `./scripts/install-hugo.sh` | Hugo only |

**Codespaces.** Open the repo → *Code* → *Codespaces* → *Create codespace on master*. The
container installs the same Hugo version CI uses, forwards port 1313, and ships with GitHub CLI
so you can watch runs with `gh run list`. Preview with:

```bash
hugo server -D --bind 0.0.0.0
```

**A fresh Mac or Linux box.**

```bash
git clone https://github.com/pinxiong/pinxiong.github.io.git
cd pinxiong.github.io
./scripts/install-hugo.sh        # installs exactly the version CI pins; safe to re-run
```

On macOS it installs to `~/.local/bin` (no sudo) and tells you if that directory is missing from
`PATH`. Behind a slow connection, point it at a mirror:

```bash
HUGO_RELEASE_BASE=https://gh-proxy.com/https://github.com/gohugoio/hugo/releases/download \
  ./scripts/install-hugo.sh
```

**Credentials** are the one genuinely per-machine thing. Authenticate once with `gh auth login`,
an SSH key, or a personal access token — after that, `git push` just works.

## Layout

```
config.yaml              # site config: title, description, baseURL, menus, social links
content/
  posts/                 # articles (one .md per post)
  about.md               # About page
  archives.md            # Archive page
  search.md              # Search page (Fuse.js index)
archetypes/posts.md      # template every new post starts from
layouts/                 # site-level overrides — wins over themes/ (see Notes)
themes/PaperMod/         # vendored theme, pristine upstream v8.0
static/                  # CNAME, favicon, images — copied verbatim to the site root
scripts/                 # new-post.sh, publish.sh, install-hugo.sh
docs/                    # operating manuals (not part of the published site)
.devcontainer/           # Codespaces / VS Code Dev Containers definition
.github/workflows/       # build + deploy pipeline
```

## Notes

- **The theme is vendored and unmodified.** `themes/PaperMod/` is a byte-for-byte copy of upstream
  v8.0, committed directly (no submodule, so a plain `git clone` builds). Upgrading means replacing
  the folder — any local fixes live in `layouts/` instead and survive the swap.
- **Why `layouts/` has three files.** PaperMod v8.0 calls an internal partial with a legacy
  `partials/` prefix that Hugo ≥ 0.152 no longer resolves. `layouts/partials/templates/`
  `{opengraph,twitter_cards,schema_json}.html` are copies with that prefix removed. Site-level
  layouts take precedence over the theme, so the fix lives outside the vendored tree. Verified both
  ways: with the override the build passes, without it the build fails.
- **Hugo version.** CI pins `HUGO_VERSION` in the workflow and `scripts/install-hugo.sh` reads that
  same value, so local and deployed builds cannot drift. `config.yaml` declares a minimum of
  extended 0.146.0.
- **Custom domain.** `static/CNAME` holds `xiongpin.dev` and ships inside every build, so
  deployments never drop the domain. Keep it.
- **`baseURL`.** Locally Hugo serves `http://localhost:1313`; in CI the base URL comes from
  `actions/configure-pages`, which resolves to the custom domain. No manual editing needed.

## Manuals

The operating manuals live in `docs/` so they travel with the repository:

- `docs/github-pages-setup-manual.md` — full site setup walkthrough
- `docs/github-pages-custom-domain-manual.md` — DNS, HTTPS, and domain verification
- `docs/hugo-publish-manual.md` — day-to-day publishing and troubleshooting
