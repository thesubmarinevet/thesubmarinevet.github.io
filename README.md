# The Submarine Vet — website

A single-page landing site: `index.html` with everything inline (no build step, no dependencies besides Google Fonts). Sections: hero, positioning statement, the lexicon glossary, about, and a follow grid linking every platform under @thesubmarinevet.

## Deploying on GitHub Pages (recommended, free, matches the domain already purchased)

1. In the `thesubmarinevet` GitHub org, create a new **public** repo named exactly `thesubmarinevet.github.io` — that exact name is what makes GitHub serve it at the org's default Pages URL.
2. Push these three files (`index.html`, `CNAME`, `README.md`) to the `main` branch of that repo.
3. In the repo's **Settings → Pages**, set the source to deploy from the `main` branch, root folder. GitHub will pick up the `CNAME` file automatically and offer to enforce HTTPS once DNS is pointed at it — turn that on.
4. At your domain registrar for **thesubmarinevet.com**, add:
   - An `A` record for the root domain pointing to GitHub Pages' IPs: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - A `CNAME` record for `www` pointing to `thesubmarinevet.github.io`
5. DNS can take anywhere from a few minutes to a few hours to propagate. Once it does, thesubmarinevet.com will serve this page directly.
6. Point the older `thesubmarineveteran.com` domain at the same site as a redirect (most registrars have a "forward this domain" option) rather than leaving its old GoDaddy placeholder live.

## Editing

Everything is in `index.html` — no separate CSS/JS files. The one section worth personalizing before this goes live is **About** (search for the HTML comment `<!-- Draft copy -->`): it's a reasonable placeholder in the brand voice, but it should carry your actual service background (boat/rate, years, how trading came into it) rather than staying generic.

The lexicon terms and the follow-grid links match what's tracked in the project's `claude/30-day-launch-plan.md` doc — if a handle or platform changes, update both places.
