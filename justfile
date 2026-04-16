@jupyter:
    podman run \
        --rm \
        --interactive \
        --tty \
        --detach \
        -p 8888:8888 \
        --name jupyter \
        --volume .:/data:z \
        dvf:latest \
        uv run jupyter lab \
            --ip 0.0.0.0 \
            --allow-root \
            --no-browser

# Kill jupyter server container
@jupyter-kill:
    podman kill jupyter

# Open jupyter lab in a browser
browser:
    #!/usr/bin/env bash
    set -euo pipefail

    token=$(
        podman exec jupyter \
            uv run jupyter lab list --json \
        | jq -r ".token"
    )
    url="http://127.0.0.1:8888/lab?token=${token}"
    xdg-open "${url}"

# Start a shell on a running container
@shell:
    podman exec \
        --interactive \
        --tty \
        --env "TERM=xterm-256color" \
    jupyter bash
