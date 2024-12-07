# Answers

## Activity 1.1.

```sh
docker volume create boston-data
```

## Activity 1.2.

Usually, port `5432` is used by `postgres`. Therefore, for this command to work correctly, the `postgres` process should be terminated.

```sh
docker run -d --rm --name boston-db \
-e POSTGRES_USER=postgres \
-e POSTGRES_PASSWORD=postgres \
-e POSTGRES_DB=boston \
-p 5432:5432 \
-v boston-data:/var/lib/postgresql/data \
postgres:latest
```

## Activity 1.3.

```sh
cat database.sql | docker exec -i boston-db psql -U postgres -d boston
```

## Activity 3.2.

```sh
docker build -t app:v1.0 .
```

## Activity 3.3.

```sh
docker run -d --rm --name boston-app \
-e DB_HOST=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' boston-db) \
-p 8080:8080 app:v1.0
```

## Activity 4.1.

```sh
docker tag app:v1.0 <docker_username>/boston-app:v1.0
docker push <docker_username>/boston-app:v1.0
```

## Activity 5.2.

```
docker-compose up -d
```
