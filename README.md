# memcache-monitor

![Build Status](https://img.shields.io/docker/cloud/build/bitsbeats/memcache-mon)

Memcache monitoring tool with metrics.

This tool will set and get a configurable key / value to memcache and expose prometheus metrics.

## Parameters / Environment Variables

| parameter | env variable | description  | default value |
|---|---|---|---|
| -mp / --metricsport    | METRICSPORT     | port of the metrics webserver         | 8000      |
| -s / --sleep           | SLEEP           | sleep between set / get in seconds    | 0.5       |
| -m / --memcacheaddress | MEMCACHEADDRESS | memcache address                      | 127.0.0.1 |
| -p / --memcacheport    | MEMCACHEPORT    | memcache port                         | 11211 |
| -mk / --memcachekey    | MEMCACHEKEY     | memcache key                          | memcache-mon |
| -mv / --memcachevalue  | MEMCACHEVALUE   | memcache value                        | memcache-val |
| -b / --memcachebuckets | MEMCACHEBUCKETS | histogram metric buckets in seconds   | 0.0001, 0.001, 0.01, 0.1, 0.2, 0.4, 0.8, 1, 2, 4, 8 |
| -v / --verbose         | MEMCACHEMONVERBOSE | verbose logging                    | False |

## Metrics
| name | type | unit | desc | 
|---|---|---|---|
| memcachemon_request_duration_seconds_bucket | Histogram | seconds | Request time |
| memcachemon_request_failures_total | Counter | int | Failure counter |

### Labels
| name | desc |
|---|---|
| memcache | value from -m (memcacheaddress) |
| operation | "get" or "set" |

## Running via docker-compose
Whole stack with prometheus and grafana.

Modify .env to your needs
```
docker-compose up -d --build
```
Now go to http://127.0.0.1:3000

## Running locally

```
git clone <repo>
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python memcache-mon.py -h
```

## Running via docker

```
# pull
docker pull bitsbeats/memcache-mon

# run
docker run -rm bitsbeats/memcache-mon -h

# env example
docker run -rm -e SLEEP=0.1 bitsbeats/memcache-mon

# stable
docker pull bitsbeats/memcache-mon:<github-tag eg. 0.0.1>
```

## Dashboard Screenshot
![](dashboard.png)