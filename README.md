# BBMRI_ERIC_data_mover

This script downloads data from one server of BBMRI eric and uploads it to a specified target server. The datamodel is altered.
This new model is specified in the data_model folder. This new model will be uploaded.
The old data retrieved from the specified server will be converted to the new model.
Invalid rows will be filtered out and written to logfiles. The valid data will be uploaded in the models<br/>

<h3>New model</h3>
 - <b>One_to_many</b> instead of xref for biobanks, subcollections and persons. This datatype allows for circular dependencies.
 This makes it for instance possible to show collections in the network table and networks in the collection table; before in only one
 of both tables the information could be shown. This change needed the contact column in networks, biobanks and collections to become an xref instead of
 mref, which means items with more than one contact are also invalid and will be filtered out<br/>
 - <b>Disease types</b> are filtered and ready for semantic search. The disease types contained a lot of invalid disease types and wildcards.
 These are now declared invalid. Semantic search will be implemented in a next release of Molgenis, this allows for searching on more generic
 ICD10 terms and also finding more specific terms that are related to your search query. This functionality could not work with the wildcards.

<h3>Run</h3>
Add a config.txt file in the format of config_example.txt, in the same directory. <br/>
Config.txt:

```
url=http(s)://source-server/api/
account=username
password=password
countries=AT,BE,CZ,DE,EE,FI,FR,GR,IT,MT,NL,NO,PL,SE,UK,LV
target_server=http(s)://target-server/api/
target_account=username
target_password=password
```
Run the script:<br/>

```
python3 Bbmri_data_mover.py
```

<h3>Model</h3>
Model for countries will be created in /datamodel/countries.
Model for general directory is already in /datamodel and will be zipped as: meta_data.zip

<h3>Data</h3>
Data will be retrieved from one server, converted to new model and put in the new server. Invalid rows are filtered out.

<h3>Logs of invalid data</h3>
Logs will be created in /Bbrmi_eric_quality_checker. Two logs will be written:

| Logfile           | Description                                                                                 |
|-------------------|---------------------------------------------------------------------------------------------|
| logs.txt          | Contains all rows with invalid data                                                         |
| breaking_rows.txt | Contains data invalid rows that are not uploaded in the new model on the target server      |