import datetime
import tempfile


def generate_timestamp_file_name():
    return datetime.datetime.now().strftime("%d%m%Y_%H%M%S")


def create_tmp_file():
    create_file = tempfile.NamedTemporaryFile(suffix=".csv", prefix=f"data_out_{generate_timestamp_file_name()}_",
                                              delete=False)
    return create_file.name
