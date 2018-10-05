# Model Import/Export Example

A example project using model import export. 

It shows how to use model-import-export package in django. model-import-export allows you to export your django model into csv or excel format and imports excel format into django model.

## Files & directories
app_name: testapp
views: testapp.views
models: testapp.models

## Urls
'/' : Root url

'/export/subject.xlsx': Export subject model to excel

'/import/subject': Import uploaded file to subject model

'/import/subject/test': Test the import process without uploading file. (uses documents/test.xlsx)


## Model Import/Export
[![GitHub model_import_export](https://github.com/aj3sh/model_import_export)

