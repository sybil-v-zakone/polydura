import functools
import json

from loguru import logger


def read_from_txt(file_path):
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file]
    except FileNotFoundError as e:
        logger.exception(f"File '{file_path}' not found.")
    except Exception as e:
        logger.exception(
            f"Encountered an error while reading a TXT file: {file_path} | {str(e)}."
        )


def read_from_json(file_path):
    try:
        with open(file_path) as json_file:
            return json.load(json_file)
    except FileNotFoundError as e:
        logger.exception(f"File '{file_path}' not found.")
    except Exception as e:
        logger.exception(
            f"Encountered an error while reading a JSON file: '{file_path}'."
        )


def write_to_json(file_path, data):
    try:
        with open(file_path, "w") as json_file:
            json_file.write(data)
            return True
    except FileNotFoundError as e:
        logger.exception(f"File '{file_path}' not found.")
        return False
    except Exception as e:
        logger.exception(
            f"Encountered an error while writing to a JSON file: {file_path} | {str(e)}."
        )
        return False
