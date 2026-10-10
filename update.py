import json
import os
import requests

URL = "https://api.github.com/graphql"
H = {"Authorization": f"bearer {os.environ['ACCESS_TOKEN']}"}

def gql(q, v=None):
    r = requests.post(URL, json={"query": q, "variables": v or {}}, headers=H)
    r.raise_for_status()
    d = r.json()
    if "errors" in d and not d.get("data"):
        raise SystemExit(d["errors"]) 
    return d["data"]

me = gql("{viewer{id login followers{totalCount}}}")["viewer"]

repos, cursor = [], None
while True:
    d = gql(
        """query($c:String){viewer{repositories(first:100,after:$c,ownerAffiliations:[OWNER]){
        pageInfo{hasNextPage endCursor}
        nodes{nameWithOwner stargazerCount isFork owner{login}}}}}""",
        {"c": cursor},
    )["viewer"]["repositories"]
    repos += d["nodes"]
    if not d["pageInfo"]["hasNextPage"]:
        break
    cursor = d["pageInfo"]["endCursor"]

add = dele = commits = 0
for r in repos:
    owner, name = r["nameWithOwner"].split("/")
    cursor = None
    while True:
        d = gql(
            """query($o:String!,$n:String!,$a:ID!,$c:String){repository(owner:$o,name:$n){
            defaultBranchRef{target{... on Commit{history(first:100,after:$c,author:{id:$a}){
            pageInfo{hasNextPage endCursor}nodes{additions deletions}}}}}}}""",
            {"o": owner, "n": name, "a": me["id"], "c": cursor},
        )["repository"] or {}
        ref = d["defaultBranchRef"]
        if not ref:
            break
        h = ref["target"]["history"]
        for n in h["nodes"]:
            add += n["additions"]
            dele += n["deletions"]
            commits += 1
        if not h["pageInfo"]["hasNextPage"]:
            break
        cursor = h["pageInfo"]["endCursor"]

json.dump(
    {
        "repos": len(repos),
        "stars": sum(r["stargazerCount"] for r in repos),
        "followers": me["followers"]["totalCount"],
        "commits": commits,
        "add": add,
        "del": dele,
        "loc": add - dele,
    },
    open("stats.json", "w"),
)