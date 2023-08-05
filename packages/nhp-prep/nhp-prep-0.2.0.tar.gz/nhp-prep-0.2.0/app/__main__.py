import click
import os
import pkg_resources

import pandas as pd

from app import __app_name__, __version__
from app.main_logger import logger
from app.column_mapper import map_columns
from app.subject_changer import change_sub
from app.timestamp_estimator import change_timestamp
from app.rename_files import file_rename
from time import time


FILE_TYPE = '.csv'
FILE_COLUMNS_STD = 'config/columns__std_format.csv'


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f'CLI: {__app_name__}')
    click.echo(f'Version: v{__version__}')
    ctx.exit()


def log_issues(issues_list: list):
    """Helper function to include in the logs
    the list of some of the issues found.

    Args:
        issues_list (list): List with empty or errors.
    """
    for err in issues_list:
        logger.error(err)


@click.group()
@click.option('--version', '-v', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True, help='Shows current version.')
def main():
    logger.info(f'CLI: {__app_name__}')
    logger.info(f'Version: v{__version__}')


@click.command(name='reorder-columns', short_help='Reorders columns in files.')
@click.option('--input', '-i', type=click.Path(exists=True, file_okay=True), required=True, help='The input input with the files to process OR a solo CSV file.')
@click.option('--output', '-o', type=click.Path(exists=False), required=True, help='The output input for the reordered files.')
@click.option('--ref-file', '-r', type=str, help='Reference file that contains the names of the columns.')
def reorder_columns(input, output, ref_file):
    """
    Processes the files from an input directory or file, and
    returns the same file(s) to a different output
    directory. If the reference file is not included
    the application will retrieve an internal standard file
    that will serve as a reference.

    OUTPUT: 
    If the output path does not exist, it will be created.

    """
    logger.info(
        f'-------------------------- REORDERING COLUMNS --------------------------')
    logger.info(f'Input: {input}')
    logger.info(f'Output path: {output}')
    logger.info(f'Columns reference file: {ref_file}')

    reference_file = ref_file if ref_file is not None else pkg_resources.resource_stream(__name__, FILE_COLUMNS_STD)
    df_reference = pd.read_csv(reference_file)
    ref_columns = list(df_reference.columns)
    """Creates the output path in case that it does not
    exists.
    """
    if not os.path.exists(output):
        os.makedirs(output)

    _files_to_process = 0
    _error_files = 0
    # TODO: Needs a validation for a directory or a file.
    for _, _, files in os.walk(input):
        for each in files:
            if each.endswith(FILE_TYPE):
                _files_to_process += 1
                filename = os.path.join(input, each)
                out_filename = os.path.join(output, each)
                try:
                    df_reordered = map_columns(
                        columns=ref_columns, filename=filename)
                    df_reordered.to_csv(out_filename, index=False)
                    logger.info(f'File reordered successfully: {out_filename}')
                except Exception as e:
                    logger.error(
                        f'An error has been detected while processing the file: {filename}. \n Please check the following error: {e}')
                    _error_files += 1
    _reordered_files = _files_to_process - _error_files
    _percentage_success = (_reordered_files / _files_to_process) * 100
    logger.info(
        f'Total files reordered successfully:  {_reordered_files}/{_files_to_process} => {_percentage_success} % success!')


@click.command(name='rename', short_help='Renames all the files based on standard.')
@click.option('--input', '-i', type=click.Path(exists=True, file_okay=True), required=True, help='The input directory with the files to process OR a solo CSV file.')
@click.option('--output', '-o', type=click.Path(exists=False), required=False, help='The output path for the reordered file(s) [OPTIONAL].')
def rename(input, output):
    """
    Processes the file(s) from an input, and
    returns the same file(s) to a different output
    input, but with the format:

    YYYY-MM-DD_HHmmh_<experiment_name>_<Subject_name>_<Researcher_name_or_initials>_data.csv

    OUTPUT: 
    If the output path does not exist, it will be created.
    Also, if the Output path is not passed, nhp-prep will
    proceed to use the path of each file and rename the original
    file.
    """       
    start_time = time()
    logger.info(
        f'-------------------------- RENAMING FILE(S) --------------------------')
    logger.info(f'Input: {input}')
    logger.info(f'Output path: {output}')
    if not os.path.exists(output):
        os.makedirs(output)
    if os.path.isfile(input):
        logger.info('File recognized. \n Proceeding to rename it...')
        _result = file_rename(filepath=input, output=output)
        if _result is False:
            logger.error(
                f'An error occurred during the process of renaming the file: {input}. Please check the logs.')
        logger.info(f'Total execution time: {time() - start_time} seconds')
    elif os.path.isdir(input):
        logger.info('Path recognized.')
        logger.info('Proceeding to rename all files within it...')
        num_files = 0
        num_errors = 0
        error_files = list()
        empty_files = list()
        for each in os.listdir(input):
            if each.endswith(FILE_TYPE):  # Filtering only .csv files
                filepath = os.path.join(input, each)
                num_files += 1
                _result = file_rename(filepath=filepath, output=output)
                if _result is False:
                    logger.error(
                        f'An error occurred during the process of renaming the file: {each}. Please check the logs.')
                    try:
                        file_df = pd.read_csv(filepath_or_buffer=filepath)
                        if file_df.empty:
                            logger.error(
                                f'The file {each} has been detected to be empty. It can be ignored!')
                            empty_files.append(filepath)
                        else:
                            error_files.append(filepath)
                    except Exception:
                        logger.error(
                            f'The file {each} cannot be processed. Please check the logs: ', exc_info=True)
                        empty_files.append(filepath)
                    num_errors += 1

        _renamed_files = num_files - num_errors
        _percentage_success = (_renamed_files / num_files) * 100
        logger.error(f'The list of files with errors is:')
        log_issues(error_files)

        logger.error(f'The list of empty files is:')
        log_issues(empty_files)

        logger.info(f'Total files with errors: {len(error_files)}')
        logger.info(f'Total empty files: {len(empty_files)}')

        logger.info(
            f'Total files reordered successfully:  {_renamed_files}/{num_files} => {_percentage_success} % success!')
        logger.info(f'Total execution time: {time() - start_time} seconds')


@click.command(name='timestamp-estimate', short_help='Estimates trial true timestamp.')
@click.option('--input', '-i', type=str, help='Directory that contains all the CSV files to process.')
@click.option('--output', '-o', type=str, help='Output directory of the processed files.')
def timestamp_estimate(input, output):
    """This command estimates the timestamp of an specific trial
    inside of each file(s). In order for this command to work
    the file must have the following columns:

      - Time \n
      - ExpStartTimestamp
      - TrialStartTimestamp

    """
    logger.info(
        f'-------------------------- ESTIMATING TIMESTAMP IN output(S) --------------------------')
    logger.info(f'Input directory: {input}')
    logger.info(f'Output directory: {output}')
    """Creates the output path in case that it does not
    exists.
    """
    if not os.path.exists(output):
        os.makedirs(output)

    _files_to_process = 0
    _error_files = 0
    for _, _, files in os.walk(input):
        for each in files:
            if each.endswith(FILE_TYPE):
                _files_to_process += 1
                filename = os.path.join(input, each)
                out_filename = os.path.join(output, each)
                try:
                    df_timestamp_changed = change_timestamp(
                        filename = filename
                    )
                    df_timestamp_changed.to_csv(out_filename, index=False)
                    logger.info(f'Change timestamp successfully: {out_filename}')
                except Exception as e:
                    logger.error(
                        f'An error has been detected while processing the file: {filename}. \n Please check the following error: {e}')
                    _error_files += 1
    _reordered_files = _files_to_process - _error_files
    _percentage_success = (_reordered_files / _files_to_process) * 100
    logger.info(
        f'Total files reordered successfully:  {_reordered_files}/{_files_to_process} => {_percentage_success} % success!')


@click.command(name='sub-rename', short_help='Updates the subject name based trial level.')
@click.option('--ref-file', '-f', required=True, help='Reference file that contains the names of subjects and timestamp start and end.')
@click.option('--input', '-i', required=True, help='Input directory.')
@click.option('--output', '-o', help='Output directory.')
def sub_rename(input, output, ref_file):
    logger.info(
        f'-------------------------- SUBJECT RENAMING --------------------------')
    logger.info(f'Input directory: {input}')
    logger.info(f'Output directory: {output}')
    logger.info(f'Reference file: {ref_file}')
    """
    Processes the files from a directory, and
    returns the same files to a different output
    directory. If the reference file is not included
    the application will retrieve a standard file
    that will serve as a reference.

    DIRECTORY: The input directory with the files to process.

    OUTPUT: The output directory for the reordered files.
    If the output path does not exist, it will be created.

    REF-FILE: The file that contains the date, and the start
    and end timestamp of each subjects.
    """

    logger.info(f'Input directory: {input}')
    logger.info(f'Output directory: {output}')
    logger.info(f'Columns reference file: {ref_file}')

    reference_file = ref_file if ref_file is not None else './app/config/baboons_sessions_compiled.csv.csv'
    """Creates the output path in case that it does not
    exists.
    """
    if not os.path.exists(output):
        os.makedirs(output)

    _files_to_process = 0
    _error_files = 0
    for _, _, files in os.walk(input):
        for each in files:
            if each.endswith(FILE_TYPE):
                _files_to_process += 1
                filename = os.path.join(input, each)
                out_filename = os.path.join(output, each)
                try:
                    df_changed = change_sub(
                        file_path=filename, filename=each, ref_filename=reference_file)
                    df_changed.to_csv(out_filename, index=False)
                    logger.info(
                        f'Subject changed successfully: {out_filename}')
                except Exception as e:
                    logger.error(
                        f'An error has been detected while processing the file: {filename}. \n Please check the following error: {e}')
                    _error_files += 1
    _changed_files = _files_to_process - _error_files
    _percentage_success = (_changed_files / _files_to_process) * 100
    logger.info(
        f'Total files reordered successfully:  {_changed_files}/{_files_to_process} => {_percentage_success} % success!')


main.add_command(reorder_columns)
main.add_command(rename)
main.add_command(timestamp_estimate)
main.add_command(sub_rename)

if __name__ == '__main__':
    main()
