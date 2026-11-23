"""Generate a public-only GitHub activity SVG with the Python standard library."""
import datetime
import html
import json
import os
from pathlib import Path
import urllib.request

owner = os.environ["GITHUB_REPOSITORY_OWNER"]
headers = {"Authorization": f"Bearer {os.environ['GH_TOKEN']}",
           "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
def get(path):
    request = urllib.request.Request("https://api.github.com" + path, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)
user = get(f"/users/{owner}")
# The public user endpoint excludes private repositories and private contribution data.
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
values = [("Public repositories", user["public_repos"]), ("Followers", user["followers"])]
text = "".join(f'<text x="{30 + i * 340}" y="85" fill="#b5e7c3" font-size="26">{value}</text>'
               f'<text x="{30 + i * 340}" y="113" fill="#a7b5ad" font-size="14">{html.escape(label)}</text>'
               for i, (label, value) in enumerate(values))
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="760" height="170" viewBox="0 0 760 170" '
       f'role="img" aria-labelledby="t d"><title id="t">Public GitHub activity for {html.escape(owner)}</title>'
       f'<desc id="d">Public repositories: {values[0][1]}. Followers: {values[1][1]}. Updated {now}.</desc>'
       '<rect width="760" height="170" rx="10" fill="#17201e"/>'
       '<g font-family="Arial,sans-serif"><text x="30" y="35" fill="#eff5f1" font-size="18">Public GitHub activity</text>'
       f'{text}<text x="30" y="149" fill="#a7b5ad" font-size="11">Updated {now} · Public data only</text></g></svg>')
Path("assets").mkdir(exist_ok=True)
Path("assets/github-metrics.svg").write_text(svg, encoding="utf-8")
