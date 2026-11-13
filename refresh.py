"""Re-check every board in data/boards.json against the public ATS job-board APIs.
Updates open_jobs and checked, then writes data/boards.json and data/boards.csv.
Standard library only. Usage: python refresh.py"""
import csv, datetime, json, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = {"User-Agent": "ats-company-slugs-refresh/1.0 (+https://github.com/datakit457/ats-company-slugs)"}
URLS = {
    "greenhouse": "https://boards-api.greenhouse.io/v1/boards/{}/jobs",
    "lever": "https://api.lever.co/v0/postings/{}?mode=json",
    "ashby": "https://api.ashbyhq.com/posting-api/job-board/{}",
    "workable": "https://apply.workable.com/api/v1/widget/accounts/{}",
}

def count(ats, slug):
    try:
        req = urllib.request.Request(URLS[ats].format(slug), headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.load(r)
    except Exception:
        return None  # unreachable or board gone
    if ats == "lever":
        return len(d)
    return len(d.get("jobs", []))

def main():
    rows = json.load(open("data/boards.json"))
    today = datetime.date.today().isoformat()
    def work(r):
        time.sleep(0.2)
        n = count(r["ats"], r["slug"])
        r["open_jobs"] = n if n is not None else 0
        r["board_ok"] = n is not None
        r["checked"] = today
        return r
    with ThreadPoolExecutor(4) as ex:
        rows = list(ex.map(work, rows))
    rows.sort(key=lambda r: (-r["open_jobs"], r["company"].lower()))
    json.dump(rows, open("data/boards.json", "w"), indent=1)
    with open("data/boards.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["company", "ats", "slug", "industry", "open_jobs", "board_ok", "checked"])
        w.writeheader(); w.writerows(rows)
    ok = sum(r["board_ok"] for r in rows)
    print(f"{len(rows)} boards, {ok} reachable, {sum(r['open_jobs'] for r in rows)} open jobs")

if __name__ == "__main__":
    main()
