# Greenhouse, Lever, Ashby and Workable company slugs (843 verified job boards)

A free, open list of **843 company job boards** with their ATS (applicant tracking system) and board slug, checked against the public job-board APIs. Every row was reachable on the date in the `checked` column, and the list re-checks itself weekly with GitHub Actions.

Why this exists: Greenhouse, Lever, Ashby and Workable all publish open jobs as public JSON, but you need each company's board slug, and it's often not what you'd guess. I built this list while working on a jobs tool and am sharing it so you don't have to probe slugs yourself.

| ATS | Boards | Open jobs (2026-11-13) |
|---|---:|---:|
| Ashby | 509 | 10,102 |
| Greenhouse | 236 | 17,627 |
| Lever | 91 | 2,484 |
| Workable | 7 | 72 |

## Files

- [`data/boards.csv`](data/boards.csv) / [`data/boards.json`](data/boards.json): `company, ats, slug, industry, open_jobs, board_ok, checked`
- [`fetch_jobs.py`](fetch_jobs.py): print the open jobs for one board (standard library only)
- [`refresh.py`](refresh.py): re-check every board and rewrite the data files (runs weekly in `.github/workflows/refresh.yml`)

## Endpoints

| ATS | Public endpoint |
|---|---|
| Greenhouse | `https://boards-api.greenhouse.io/v1/boards/<slug>/jobs` |
| Lever | `https://api.lever.co/v0/postings/<slug>?mode=json` |
| Ashby | `https://api.ashbyhq.com/posting-api/job-board/<slug>` |
| Workable | `https://apply.workable.com/api/v1/widget/accounts/<slug>` |

## Example

```bash
python fetch_jobs.py greenhouse stripe
python fetch_jobs.py ashby openai
```

```
Research Engineer | San Francisco | https://jobs.ashbyhq.com/openai/240d459b-...
...
827 jobs
```

Find every board with remote data roles:

```python
import csv
boards = [r for r in csv.DictReader(open("data/boards.csv")) if int(r["open_jobs"]) > 0]
print(len(boards), "boards with open jobs")
```

## Where the companies came from

Public company directories (Y Combinator's company list and similar public lists), plus probing well-known tech company names against the four APIs. Only boards that responded are kept. Company names and slugs are business data; the list contains no personal data.

## Hosted version

If you'd rather not run the polling yourself, I also built an Apify Actor that uses this directory: [ATS Jobs Feed on Apify](https://apify.com/datakit/ats-jobs-feed) (keyword/location filters, only-new-jobs mode, CSV/JSON export). More tools and tutorials: [datakit457.github.io](https://datakit457.github.io/).

## Licence

Data and code: CC0 / public domain. Job postings belong to the companies that published them; check each ATS's terms before republishing job content.
