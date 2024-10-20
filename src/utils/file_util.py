import os


def ensure_directory_exists(directory: str):
    """
    如果给定的目录不存在的话，则创建

    TODO 2024-10-20 00:13:43 需要考虑存在但是是文件的情况
    :param directory:
    :return:
    """
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
