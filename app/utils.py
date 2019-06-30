import datetime


def generate_timestamp_file_name():
    return datetime.datetime.now().strftime("%d%m%Y_%H%M%S")