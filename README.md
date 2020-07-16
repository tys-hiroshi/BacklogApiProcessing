# BacklogApiProcessing

BacklogApiProcessing is the totaling up of issues that the issue type in term on Azure Function(Python).

## Usage

1.Clone this repository

2.You should modifiy ```BacklogApiProcessing/AzureFunctionProj/BacklogApiTimerTrigger/config_sample.yml.```

```
API_KEY.GLOBAL is global api key. (*)
WIKI_SPACE is workspace name (*)
PROCESSING_PROJECT_KEY is project keys of the totaling up. (*)
PROCESSING_DATETIME ( format: %Y-%m-%d %H:%M:%S ) is executing datetime of the totaling up. (If this is empty, datetime is used datetime now.)
PROCESSING_ISSUE_TYPE_NAME is issue type name of the totaling up. (*)
PROCESSING_UPDATE_WIKI.SUMMARY_WIKI_ID is update summary wiki id. (*)
PROCESSING_UPDATE_WIKI.DETAIL_WIKI_ID is update detail wiki id. (*)
```


3.Rename config_sample.yml to config.yml

4.You execute below command.

```
$ az functionapp create --resource-group [resource group name] --os-type Linux \
> --consumption-plan-location westeurope  --runtime python --runtime-version 3.7 \
> --name [app name] --storage-account  [storage account name]

$ func azure functionapp publish [app name] --build remote
```

ref. [Quickstart: Create an HTTP triggered Python function in Azure](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python)


## Requirements

follow the BacklogApiProcessing/AzureFunctionProj/requirements.txt

## References

https://pypi.org/project/backlogprocessing/

https://github.com/tys-hiroshi/backlogprocessing/tree/master


https://docs.microsoft.com/ja-jp/cli/azure/install-azure-cli?view=azure-cli-latest

