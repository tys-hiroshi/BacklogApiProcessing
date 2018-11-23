# BacklogApiProcessing

BacklogApiProcessing is the totaling up of issues that the issue type in term.

## Usage

1.Clone this repository

2.You modified BacklogApiProcessing/BacklogApiProcessing/config.yml.

API_KEY.GLOBAL is global api key.
API_KEY.GLOBAL is global api key.
PROCESSING_PROJECT_KEY is project keys of the totaling up.
PROCESSING_TERM is term of the totaling up.
PROCESSING_ISSUE_TYPE_NAME is issue type name of the totaling up.

3.Run BacklogApiProcessing/BacklogApiProcessing/BacklogApiProcessing.py

```
$ cd BacklogApiProcessing/BacklogApiProcessing
$ python BacklogApiProcessing.py
```

4.You can see BacklogApiProcessing.log.

```actual_hours``` is project actual hours of issue type in term.

## Require

follow the BacklogApiProcessing/BacklogApiProcessing/requirements.txt
