# Getting Started

## Requirements

- Python 3
- pip

## Setup

### Install dependencies

```
$ pip install -r requirements.txt
```

### Required environment variables

| Name | Description |
|:----:|:----:|
| `PTX_TIMETABLE_JSON_BASE_URL` | Base URL for downloading JSON data. See https://ptx.transportdata.tw/MOTC for details. |
| `PTX_APP_ID` | App ID for [PTX](https://ptx.transportdata.tw/PTX/) |
| `PTX_APP_KEY` | App key for [PTX](https://ptx.transportdata.tw/PTX/) |
| `GIT_USER_NAME` | Git user name - the committer's name |
| `GIT_USER_EMAIL` | Git user email - the committer's email |
| `GITHUB_ORG_NAME` | GitHub organization name for storing processed data. |
| `GITHUB_ACCESS_TOKEN` | GitHub access token with repository creation permission. |

### Start Parsing!

```
$ script/crawl
```

# Using Processed Data

Processed data will be pushed to a repository under the GitHub organization specified.

# Parameters

| Name | Description |
|:----:|:----:|
| `GITHUB_ORG_NAME` | Specified organization name. |
| `DATE` | YYYYMMdd |
| `FROM_STATION` | Station ID, see [this](http://163.29.3.98/json/%E8%AA%AA%E6%98%8E/%E5%8F%B0%E9%90%B5%E7%81%AB%E8%BB%8A%E6%99%82%E5%88%BB%E7%B6%B2%E9%9A%9B%E8%B3%87%E8%A8%8A%E4%BA%A4%E6%8F%9B%E8%AA%AA%E6%98%8E.rtf) for details. |
| `TO_STATION` | Station ID, see [this](http://163.29.3.98/json/%E8%AA%AA%E6%98%8E/%E5%8F%B0%E9%90%B5%E7%81%AB%E8%BB%8A%E6%99%82%E5%88%BB%E7%B6%B2%E9%9A%9B%E8%B3%87%E8%A8%8A%E4%BA%A4%E6%8F%9B%E8%AA%AA%E6%98%8E.rtf) for details. |
| `TRAIN_ID` | Train ID |

## Timetables

### Request URL

```
https://{GITHUB_ORG_NAME}.github.io/{DATE}/timetables/{FROM_STATION}/{TO_STATION}.json
```

### Data Format

```js
[
  {
    "train_no": "1113",
    "departs_at": "05:12",
    "arrives_at": "05:19",
    "train_class": "1131",
    "carries_packages": true,
    "has_bike_stands": false,
    "has_breastfeeding_rooms": false,
    "has_dining_rooms": false,
    "is_accessible": false
  },
  ...
]
```

## Train Information

### Request URL

```
https://{GITHUB_ORG_NAME}.github.io/{DATE}/trains/{TRAIN_ID}.json
```

### Data Format

```js
{
  "train_no": "101",
  "train_class": "1108",
  "carries_packages": true,
  "has_bike_stands": false,
  "has_breastfeeding_rooms": false,
  "has_dining_rooms": false,
  "is_accessible": false,
  "stops": [
    {
      "station": "1319",
      "departs_at": "05:42",
      "arrives_at": "05:40"
    },
    ...
  ]
}
```
