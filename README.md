# emby_exporter_v2

## Docker test
```
docker run docker run -d --volume programdata:/config --volume <movie_share_folder>:/mnt/share1 --publish 8096:8096 --publish 8920:8920 --name embytest --env UID=1000 --env GID=100 --env GIDLIST=100 emby/embyserver:latest
docker build -t emby_exporter:latest . 
docker run --link embytest -p 9123:9123 -it emby_exporter:latest --emby embytest:8096 --auth <api_key> --userid <user_id> 
```

## Standalone test
```
python emby_exporter/emby_exporter.py --emby <emby_server> --auth <api_key> --userid <user_id> 