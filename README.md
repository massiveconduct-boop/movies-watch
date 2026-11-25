# The Watchlist

A single-page catalog of 60 films, series, anime and adult animation picked for one taste profile: crime/psychological, sci-fi, dark fantasy, martial arts, superhero, survival — overpowered or mastermind leads, real power progression, no filler, high tolerance for violence.

- **60 titles**: 15 movies, 15 series, 15 anime (incl. donghua), 15 western adult animation
- **Ratings**: IMDb (via OMDb), Rotten Tomatoes (critics + audience, scraped), and the TFP upload index's own posted score (reference only)
- **Per title**: poster, synopsis, "why it fits", content notes, tier, links to IMDb / RT / where-to-watch
- **No download links** anywhere. TFP numbers are shown as a data point, not a source.

## View it

```bash
cd movies-watch
python3 -m http.server 8099
# open http://localhost:8099
```

`index.html` is fully self-contained (data is inlined), so you can also just double-click it. `data.json` is the same dataset if you want to reuse it.

Features: search, type tabs, genre filter, IMDb thresholds (8.5+/8.0+/7.5+), sort by IMDb / RT critics / RT audience / year / title, and deep links (`index.html#t=tt15239678`).

## Deploy free

- **Netlify Drop** — drag the `movies-watch` folder onto https://app.netlify.com/drop. Instant URL.
- **GitHub Pages** — push the folder to a repo, Settings → Pages → deploy from branch root.
- **Cloudflare Pages** — connect the repo, no build command, output directory `/`.

No server code, no build step.

## Telegram

`telegram/posts.json` holds 60 ready-made posts (image URL + HTML caption with ratings, synopsis, notes and links). `telegram/post.py` sends them one by one.

```bash
export TELEGRAM_BOT_TOKEN="123:abc"      # from @BotFather
export TELEGRAM_CHAT_ID="@yourchannel"   # bot must be channel admin

python3 telegram/post.py --dry-run        # preview, no network
python3 telegram/post.py --limit 3        # test 3 posts
python3 telegram/post.py                  # all 60, 4s apart
```

Use `--start N` to resume, `--delay` to slow down if you hit rate limits. On a failed photo send it falls back to a text message so nothing is lost.

## Data notes

- IMDb is the reference score. TFP's posted ratings are frequently stale or inflated (e.g. several 8.8–9.3 site scores map to 3.6–5.6 on IMDb), so they are labelled "TFP site" and never used for ranking.
- RT scores are missing for a chunk of anime/donghua because Rotten Tomatoes has no page; the UI shows `—`.
- Synopses come from OMDb; content notes are editorial.
- Posters are hot-linked from Amazon's IMDb image CDN; they load fine but are not bundled.

## Files

```
index.html          the app (data inlined)
data.json           catalog dataset
telegram/posts.json 60 channel-ready posts
telegram/post.py    Bot API sender
```
