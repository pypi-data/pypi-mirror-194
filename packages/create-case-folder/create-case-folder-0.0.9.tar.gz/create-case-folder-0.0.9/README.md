# create-case-folder

A command line script for creating a parent folder and sub-folders for case management.

## Usage

To use the script, run the following command in your terminal:

```sh
create-case-folder --case F01-66 --evidence EV01
```

or

```sh
create-case-folder -c F01-66  -e EV01 EV02 EV03 
```


The `--case` argument is optional and will default to `YYYYMMDDHHmmss_NEWCASE` if not provided. 

The `--evidence` argument is also optional and will default to `EVIDENCE` if not provided.

The script will create the parent folder and sub-folder for evidence, and then create the following sub-folders inside the evidence folder:

- Documents
- Extracts
- Pictures
- Videos
- Reports

If the folders are successfully created, the script will output a success message.

If there's an error, the script will output an error message with the exception.

## Example
![Example](https://raw.githubusercontent.com/jaytrairat/python-create-case-folder/main/assets/demo.gif)

## Contributing

Feel free to fork the repository and make any changes or improvements that you'd like to see. If you have any questions or suggestions, please don't hesitate to reach out to jaytrairat@outlook.com.
