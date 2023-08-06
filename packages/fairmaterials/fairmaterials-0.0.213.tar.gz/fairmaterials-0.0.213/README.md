
![logo](https://i.imgur.com/pqR2OBe.png)

# Fairmaterials
Fairmaterials is a tool for fairing data. It reads a template JSON file to get the preset data. The user can edit the data by manually inputting or by importing a csv file. The final output will be a new JSON file with the same structure. 


# Features
 -  Importing JSON template as JSON-LD.
 -   Display fair data in dataframe format.
 -   Automatically notify duplicate names.
 -   Modify JSON data.
		- Based on CSV file.
		- Based on keyboard input.
 -   Output as standard JSON-LD.
 -   CSV-based group input and output.
#  Setup
1. Install it at bash
```bash
$ pip install fairmaterials
```
2.	Import it in python
```python
from fairmaterials.fair import fairjson
``` 
#  A quick example
***Load a template file***
```python
device=fairjson('cots_json_template.json')
``` 
***Display the data***
```python
device.display_current_JSONDF()
``` 
***Load a CSV file***
```python
device.importCsv('data.csv')
``` 
***Check the detailed description of the key***
```python
device.searchKey('scbi')
``` 
***Change the value of "scbi" to "testvalue"*** 
```python
device.setValue('scbi','testvalue')
``` 
***Save to JSON file***
```python
device.save_to_json('test.json')
``` 
***Generate a blank CSV file with name "group_input.csv" for group input***
```python
device.generate_group_input_csv(3)
``` 
***Directly convert a group input CSV file to multiple json files***
```python
device.convert_group_input_csv_to_json_files("group_input.csv" )
``` 
#  Versions
All notable changes to this project will be documented in this file.
## [0.0.213] - 2021-10-8
### Added
- Add template csv file.
## [0.0.212] - 2021-10-7
### Added
- Add group input CSV file generation function.
- Add directly convert a group input CSV file to multiple json file function.
- Add Version part in Readme.md file.