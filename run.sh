docker_local_up() {
    docker compose -f docker-compose.local.yaml up -d
}

docker_local_down() {
    docker compose -f=docker-compose.local.yaml down
}