#!/usr/bin/env python3
import requests
import sys

# ==== CONFIG ====
NEXUS_URL = "http://www.pgrnexus.com"   # Base URL of Nexus (no /v2)
REPOSITORY = "pgr-devops-docker-local"  # Docker repo in Nexus
USERNAME = "reguser"                     # Nexus username
PASSWORD = "RegUser1234"                 # Nexus password
FORMAT = "docker"                        # Could be docker, maven, npm, etc.
# ===============

session = requests.Session()
session.auth = (USERNAME, PASSWORD)

def nexus_search(repository, format_type, filter_name=None):
    """
    Search Nexus Docker repo and optionally filter by partial image name.
    """
    continuationToken = None
    results = []

    while True:
        params = {
            "repository": repository,
            "format": format_type
        }
        if continuationToken:
            params["continuationToken"] = continuationToken

        url = f"{NEXUS_URL}/service/rest/v1/search"
        resp = session.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

        for item in data.get("items", []):
            full_name = item.get("name")
            version = item.get("version")

            if not version:
                continue

            # Extract short image name
            short_name = full_name.split('/')[-1]

            # Apply filter if provided
            if filter_name and filter_name.lower() not in short_name.lower():
                continue

            results.append(f"{short_name}:{version}")

        continuationToken = data.get("continuationToken")
        if not continuationToken:
            break

    return results

if __name__ == "__main__":
    filter_name = sys.argv[1] if len(sys.argv) == 2 else None
    try:
        tags = nexus_search(REPOSITORY, FORMAT, filter_name)
        if tags:
            for t in tags:
                print(t)
        else:
            print("No matching images found.")
    except requests.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
