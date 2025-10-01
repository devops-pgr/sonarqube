curl -s -u reguser:RegUser1234 \
    "http://www.pgrnexus.com/service/rest/v1/search?repository=pgr-devops-docker-local&format=docker" \
    | jq -r '.items[] | "\(.name):\(.version)"' \
    | awk -F/ '{print $NF}' \
    | grep -i hado