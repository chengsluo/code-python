import os


def create_dirs(dir_path):
    """
    如果不存在则创建一个目录
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def delete_dirs(dir_path):
    """
    删除文件目录下所有文件和目录
    :param dir_path: 目录路径
    :return:
    """
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def delete_file(file_path):
    """
    删除指定文件
    :param file_path: 文件路径
    :return:
    """
    os.remove(file_path)
