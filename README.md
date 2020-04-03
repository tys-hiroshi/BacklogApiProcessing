# BacklogApiProcessing

BacklogApiProcessing is the totaling up of issues that the issue type in term.

## Usage

1.Clone this repository

2.You should modifiy BacklogApiProcessing/BacklogApiProcessing/config.yml.

```
HOST.URL is base url for target api.
HOST.SPACE_NAME is target backlog space name.
API_KEY.VALUE is api key.
PROCESSING_PROJECT_KEY is project keys of the totaling up.
PROCESSING_TERM is term of the totaling up.
PROCESSING_ISSUE_TYPE_NAME is issue type name of the totaling up.
PROCESSING_UPDATE_WIKI.IS_UPDATE is to update wiki flag.
PROCESSING_UPDATE_WIKI.WIKI_ID is update wiki id.
```


3.Run BacklogApiProcessing/BacklogApiProcessing/BacklogApiProcessing.py

```
$ cd BacklogApiProcessing/BacklogApiProcessing
$ python BacklogApiProcessing.py
```

4.You can see BacklogApiProcessing.log.

```actual_hours``` is project actual hours of issue type in term.

5.You can see backlog's wiki.(PROCESSING_UPDATE_WIKI.WIKI_ID)

Project actual hours is listed.

## Wiki Template

BacklogApiProcessing/WikiTemplate.md


## Requirements

follow the BacklogApiProcessing/BacklogApiProcessing/requirements.txt

