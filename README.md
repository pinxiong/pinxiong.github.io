# xiongpin.dev

Source for my personal site — engineering write-ups from real production work.
Built with [Hugo](https://gohugo.io/) + [PaperMod](https://github.com/adityatelange/hugo-PaperMod),
deployed to GitHub Pages at **https://xiongpin.dev** via GitHub Actions.

## Publishing an article

```bash
# 1. Create a post (uses the 4-part archetype: Problem / Diagnosis / Fix / Lessons)
./scripts/new-post.sh "How I Cut EC2 Cold Start by 40%"

# 2. Preview locally — drafts included
hugo server -D          # http://localhost:1313

# 3. Write it, then publish: flips draft -> false, commits, pushes
./scripts/publish.sh content/posts/how-i-cut-ec2-cold-start-by-40.md
```

Pushing to `master` triggers `.github/workflows/hugo.yml`, which builds the site and
deploys it. Live in roughly a minute.

**Drafts never go live.** A post with `draft: true` in its front matter is skipped by the
production build, so you can push work-in-progress safely. `publish.sh` warns you about
any posts left in draft.

## Layout

```
config.yaml              # site config: title, description, baseURL, menus, social links
content/
  posts/                 # articles (one .md per post)
  about.md               # About page
  archives.md            # Archive page
  search.md              # Search page (Fuse.js index)
archetypes/posts.md      # template every new post starts from
layouts/                 # theme overrides go here (takes precedence over themes/)
themes/PaperMod/         # vendored theme (see note below)
static/                  # CNAME, images, favicon — copied verbatim to the site root
scripts/                 # new-post.sh, publish.sh
```

## Notes

- **Theme is vendored, not a submodule.** `themes/PaperMod/` is committed directly, so a
  clone builds without `--recursive`. When upgrading the theme, re-apply the local patch:
  `layouts/partials/templates/{schema_json,opengraph,twitter_cards}.html` call internal
  partials without the legacy `partials/` prefix, which Hugo ≥ 0.152 requires.
- **Hugo version.** CI pins `HUGO_VERSION` in the workflow; install a matching extended
  build locally (`brew install hugo`). The site config declares a minimum of 0.146.0.
- **Custom domain.** `static/CNAME` holds `xiongpin.dev` and ships inside every build, so
  deployments never drop the domain. Keep it.
- **`baseURL`.** Locally Hugo serves `http://localhost:1313`; in CI the base URL comes from
  `actions/configure-pages`, which resolves to the custom domain. No manual editing needed.
