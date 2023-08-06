# nhp-prep

This is a CLI Tool that has been created to pre-process historical data that has been collected
in multiple instances. This includes data collected at Seneca Zoo and Mellon Institute.

### Requirements

This package requires Python 3.

### Installing

To install this CLI tool you can run the below command

```
pip3 install nhp-prep
```

Alternatively, you clone this repo and then run this command from **_within_** the repository folder

```
python3 setup.py install
```

Another way to install this solution is by running the following command from **_within_** the repository folder:

```
pip install -e .
```

Both the above commands would install the package globally and `nhp-prep` will be available on your system.

### How to use

There are multiple instances in which you can use this tool.

```
nhp-prep COMMAND [OPTIONS]
```

There are four use-cases (commands) in which you can use this tool:

1. Mapping columns from prior to current format (`reorder-columns`)

```
nhp-prep reorder-columns -i <directory_with_files_to_reorder_columns_OR_unique_CSV_file> -o <output_directory> -r <file_with_reference_columns>
```

2. Rename the files to follow current standard (`rename`)

```
nhp-prep rename -i <directory_files_to_rename_OR_uniques_CSV_file> -o <output_directory>
```

The current format for the file is: `YYYY-MM-DD_HHmmh_<experiment_name>_<Subject_name>_<Researcher_name_or_initials>_data.csv`

3. Timestamp estimation trials from historical data files based on column <X> (`timestamp-estimate`)

```
nhp-prep --timestamp-estimate -i <input_file>
```

Alternatively, you can pass the directory of the files to estimate the timestamp of each trial:

```
nhp-prep timestamp-estimate -i <directory_with_files_OR_unique_CSV_file>
```

4. Renaming of Subject according to logs file (needs the file) (`sub-rename`)

```
nhp-prep sub-rename -r <file_with_columns_and_reference_subject_names> -i <directory_with_files_OR_unique_CSV_file> -o <output_directory>
```

You could also run `nhp-prep --help` to see the available commands and their corresponding usage.

If you want to know all the options available for an specific command, run the following:

```
nhp-prep COMMAND --help
```

Example:

```
nhp-prep sub-rename --help
```

### Feedback

Please feel free to leave feedback in issues/PRs.
