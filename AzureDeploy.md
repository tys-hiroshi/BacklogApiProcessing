## create function app

```
$ az functionapp create --resource-group kazokunokiroku --os-type Linux \
> --consumption-plan-location westeurope  --runtime python --runtime-version 3.7 \
> --name pybacklogprocessingfunc --storage-account  webjobsappconsoleappv1

$ func azure functionapp publish pybacklogprocessingfunc --build remote
```
