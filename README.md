# xiongpin.dev

Source for my personal site — engineering write-ups from real production work.
Built with [Hugo](https://gohugo.io/) + [Blowfish](https://github.com/nunocoracao/blowfish),
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

On macOS it installs to `~/.local/bin` (no sudo). Newer Hugo releases ship a `.pkg` instead of a
`.tar.gz`; the script extracts the payload with `pkgutil`, so it works on both old and new
versions. Behind a slow connection, point it at a mirror:

```bash
HUGO_RELEASE_BASE=https://gh-proxy.com/https://github.com/gohugoio/hugo/releases/download \
  ./scripts/install-hugo.sh
```

**Credentials** are the one genuinely per-machine thing. Authenticate once with `gh auth login`,
an SSH key, or a personal access token — after that, `git push` just works.

## Layout

```
config/_default/          # site config, split the way Blowfish expects it:
  hugo.toml               #   baseURL, taxonomies, outputs, min Hugo version
  params.toml             #   theme options (colour scheme, homepage, article, list)
  languages.en.toml       #   title, description, author profile, social links
  menus.en.toml           #   header menu (Posts, About)
  markup.toml             #   goldmark + chroma settings the theme requires
content/
  _index.md               # homepage intro (shown under the profile header)
  posts/                  # articles (one .md per post)
  about.md                # About page
assets/css/custom.css     # site typography — loaded last, overrides the theme
archetypes/posts.md       # template every new post starts from
themes/blowfish/          # vendored theme, pristine upstream (see BLOWFISH_VERSION)
static/                   # CNAME, favicon, images — copied verbatim to the site root
scripts/                  # new-post.sh, publish.sh, install-hugo.sh
docs/                     # operating manuals (not part of the published site)
.devcontainer/            # Codespaces / VS Code Dev Containers definition
.github/workflows/        # build + deploy pipeline
```

## Notes

- **The theme is vendored and unmodified.** `themes/blowfish/` is a pristine copy of upstream
  (pinned version in `themes/blowfish/BLOWFISH_VERSION`), committed directly — no submodule, so a
  plain `git clone` builds, and no Hugo Modules, so no Go toolchain is needed. Upgrading means
  replacing the folder.
- **Site look lives in `assets/css/custom.css`.** Blowfish concatenates it *after* its own
  compiled CSS, so every rule there wins without touching the theme. This is where the
  Medium-style reading typography comes from: serif body (`charter`/`Georgia` stack), 21px at a
  ~672px measure, sans-serif headings, quiet code blocks with a single frame on
  `.highlight-wrapper` (not on `.highlight` or `pre` — Blowfish nests three layers, and framing
  more than one draws stacked borders).
- **Hugo version.** CI pins `HUGO_VERSION` in the workflow and `scripts/install-hugo.sh` reads that
  same value, so local and deployed builds cannot drift. Blowfish v3.8 uses `site.Language.Locale`,
  which needs Hugo ≥ 0.162; this repo pins 0.165.0 (the version the theme author tests against),
  and `config/_default/hugo.toml` declares the same minimum.
- **Search and archives.** Search is the magnifier in the header (Fuse.js over `index.json`);
  the post list at `/posts/` groups by year and doubles as the archive. There are no separate
  `/search/` or `/archives/` pages.
- **Videos.** Use the theme's shortcodes: `{{</* youtubeLite id="VIDEO_ID" */>}}` for a fast
  YouTube embed, `{{</* video src="clip.mp4" */>}}` for self-hosted files.
- **Name.** The byline everywhere on the site is **Pin Xiong** — given name first, so English
  readers parse the surname correctly. Use **Xiong, Pin** only in indexed/formal contexts
  (citations, speaker rosters) where the surname must be unambiguous.
- **Custom domain.** `static/CNAME` holds `xiongpin.dev` and ships inside every build, so
  deployments never drop the domain. Keep it.
- **`baseURL`.** Locally Hugo serves `http://localhost:1313`; in CI the base URL comes from
  `actions/configure-pages`, which resolves to the custom domain. No manual editing needed.

## Manuals

The operating manuals live in `docs/` so they travel with the repository:

- `docs/github-pages-setup-manual.md` — full site setup walkthrough
- `docs/github-pages-custom-domain-manual.md` — DNS, HTTPS, and domain verification
- `docs/hugo-publish-manual.md` — day-to-day publishing and troubleshooting
