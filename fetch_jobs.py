"""Print open jobs for one board from data/boards.csv, e.g.:
    python fetch_jobs.py greenhouse stripe
Standard library only; calls the public job-board API directly."""
import json, sys, urllib.request

ats, slug = sys.argv[1], sys.argv[2]
url = {
    "greenhouse": f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs",
    "lever": f"https://api.lever.co/v0/postings/{slug}?mode=json",
    "ashby": f"https://api.ashbyhq.com/posting-api/job-board/{slug}",
    "workable": f"https://apply.workable.com/api/v1/widget/accounts/{slug}",
}[ats]
req = urllib.request.Request(url, headers={"User-Agent": "ats-company-slugs-example/1.0"})
data = json.load(urllib.request.urlopen(req, timeout=30))
jobs = data if ats == "lever" else data.get("jobs", [])
for j in jobs:
    title = j.get("title") or j.get("text")
    loc = j.get("location")
    if isinstance(loc, dict):
        loc = loc.get("name")
    loc = loc or (j.get("categories") or {}).get("location") or ""
    link = j.get("absolute_url") or j.get("hostedUrl") or j.get("jobUrl") or j.get("url") or ""
    print(f"{title} | {loc} | {link}")
print(f"{len(jobs)} jobs", file=sys.stderr)
