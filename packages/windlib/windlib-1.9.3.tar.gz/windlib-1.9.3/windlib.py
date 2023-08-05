#!/usr/bin/env python3
#
#
#   windlib (Useful Functions Library)
#
#
#   Copyright (C) 2021 SNWCreations. All rights reserved.
#
#

__doc__ = """
windlib by SNWCreations

Copyright (C) 2021 SNWCreations. All rights reserved.

This library is only for my personal use, I hope to help you.
"""

# import libraries for functions
import contextlib
import hashlib
import importlib.metadata
import os
import shutil
import tarfile
import time
import zipfile
from gzip import GzipFile
from typing import List, Tuple, Any, Union

import rarfile
import requests

__version__ = importlib.metadata.version('windlib')

# the copyright message
print('windlib by SNWCreations')
print('Copyright (C) 2021 SNWCreations. All rights reserved.')


def typeof(variate: Any) -> str:
    """
    检测一个变量的类型，返回值是一个字符串。

    :param variate: 被检测的变量
    :return: 一个字符串
    """
    var_type = None
    if isinstance(variate, int):
        var_type = 'int'
    elif isinstance(variate, str):
        var_type = 'str'
    elif isinstance(variate, float):
        var_type = 'float'
    elif isinstance(variate, list):
        var_type = 'list'
    elif isinstance(variate, tuple):
        var_type = 'tuple'
    elif isinstance(variate, dict):
        var_type = 'dict'
    elif isinstance(variate, set):
        var_type = 'set'
    return var_type


def extract(filename: str, target_dir: str) -> None:
    """
    解压缩文件。

    支持 ".zip" ".gz" ".tar" ".rar" ".tar.gz" 文件。

    :param filename: 被解压的文件名
    :param target_dir: 解压到哪 (一个路径)
    :return: 无
    """

    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    if filename.endswith('.zip'):
        zip_file = zipfile.ZipFile(filename)
        for names in zip_file.namelist():
            zip_file.extract(names, target_dir)
        zip_file.close()
    elif filename.endswith('.gz'):
        f_name = filename.replace(".gz", "")
        g_file = GzipFile(filename)
        open(f_name, "w+").write(g_file.read())
        g_file.close()
    elif filename.endswith('.tar'):
        tar = tarfile.open(filename)
        names = tar.getnames()
        for name in names:
            tar.extract(name, target_dir)
        tar.close()
    elif filename.endswith('.rar'):
        rar = rarfile.RarFile(filename)
        with pushd(target_dir):
            rar.extractall()
        rar.close()
    elif filename.endswith("tar.gz"):
        tar = tarfile.open(filename, "r:gz")
        with pushd(target_dir):
            tar.extractall()
        tar.close()
    else:
        raise ValueError('未知的文件格式')


def get_file(url: str, save_as_name: str = None, save_path: str = '.', timeout: int = 10,
             headers=None, md5: str = None, sha1: str = None, max_retries: int = 0, no_overwrite: bool = False) -> str:
    """
    从互联网下载文件。

    :param url: 被下载文件的URL
    :param save_as_name: 文件在本地上将要使用的名称, 默认为 URL 指向的文件的名称
    :param save_path: 保存路径，默认为当前路径
    :param timeout: 超时时长，单位为秒，默认为 10
    :param headers: 请求头，默认为一个 Windows Chrome 的 UA
    :param md5: 如果提供此项, 在下载完成后会将此项的值作为校验值检查文件完整性
    :param sha1: 如果提供此项, 在下载完成后会将此项的值作为校验值检查文件完整性
    :param max_retries: 如果提供此项, 当下载失败时会重试, 直到下载完成或已重试次数超出限制
    :param no_overwrite: 如果此项不为 False, 则当本地存在与使用 文件在本地上将要使用的名称 命名的文件时引发 FileExistsError 异常。

    :return: 下载后的文件名。
"""
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/72.0.3626.121 Safari/537.36 '
        }

    if save_as_name is None:
        save_as_name = os.path.basename(url)
    filename = os.path.abspath(os.path.join(save_path, save_as_name))

    if os.path.isfile(filename) and no_overwrite is not False:
        raise FileExistsError(f"The file '{filename}' is already exists.")

    retries = 0

    # 请求下载地址，以流式的。打开要下载的文件位置。
    while True:
        try:
            response = requests.get(url, stream=True, timeout=timeout, headers=headers)
        except requests.exceptions.RequestException:
            retries += 1
            if retries > max_retries:
                raise
            time.sleep(3)
        else:
            with open(filename, 'wb') as file:
                # 开始下载每次请求1024字节
                for content in response.iter_content(chunk_size=1024):
                    # 写入数据块
                    file.write(content)
                if not content:
                    if (md5 is not None and not get_md5(filename) == md5) or \
                            (sha1 is not None and not get_sha1(filename) == sha1):
                        time.sleep(3)
                    break

    return filename


def find_files_with_the_specified_extension(file_type: str, folder: str = '.') -> list:
    """
    在目标文件夹中找到具有指定扩展名的文件，返回值是一个列表。

    :param folder: 从哪里查找，默认值为当前目录。
    :param file_type: 一个扩展名。例如 "txt", "jar", "md", "class" 或 ".txt" ".jar" ".md" ".class".
    :return: 被筛选的文件名的列表
    """
    folder = os.path.abspath(folder)
    if not file_type[0] == '.':
        file_type = '.' + file_type
    with pushd(folder):
        items = os.listdir('.')
        file_list = []
        for names in items:
            if names.endswith(file_type):
                file_list.append(os.path.abspath(names))
    return file_list


def copy_file(src: Union[str, List[str], Tuple[str]], dst: str) -> None:
    """
    复制文件（或文件夹）到指定的目录。

    可以通过列表的方式同时将多个文件复制到指定目录。

    :param src: 源文件或目录
    :param dst: 目标路径
    :return:
    """
    src_type = typeof(src)
    if not os.path.exists(dst):
        os.makedirs(dst, exist_ok=True)
    if src_type in ('tuple', 'list'):
        for tmp in src:
            if os.path.isfile(tmp):
                shutil.copyfile(tmp, dst)
            elif os.path.isdir(tmp):
                shutil.copytree(tmp, dst)
    elif src_type == 'str':
        if os.path.isfile(src):
            shutil.copyfile(src, dst)
        elif os.path.isdir(src):
            shutil.copytree(src, dst)


def is_it_broken(path: Union[str, Tuple[str], List[str]]) -> bool or list:
    """
    检查一个文件（或目录）是否损坏。

    允许调用时通过列表检查大量文件和目录。

    若使用列表来检查文件，则返回一个记录所有损坏的文件路径的列表。

    :param path: 将要检查的路径
    :return: 布尔值或列表
    """
    if typeof(path) in ('tuple', 'list'):
        broken_files = []
        for tmp in path:
            if os.path.lexists(tmp) and not os.path.exists(tmp):
                broken_files.append(tmp)
        return broken_files
    elif typeof(path) == 'str':
        if os.path.lexists(path):
            if os.path.exists(path):
                return True
            return False
        return False


@contextlib.contextmanager
def pushd(new_dir: str):
    """
    临时切换到一个目录，操作完成后自动返回调用前路径。

    此函数为生成器，请配合 with 语句使用。

    例如:

    with pushd(directory):
        ...

    :param new_dir: 将要切换的路径
    """
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)


def compress(input_path: str, output_name: str, output_path: str = '.') -> str:
    """
    压缩一个目录下的所有文件到一个文件。

    :param input_path: 压缩的文件夹路径
    :param output_name: 带有扩展名的压缩包名称 (压缩包类型有效值: 'zip', 'tar', 'tar.gz') (例如: aaa.zip)
    :param output_path: 输出的路径
    :return: 压缩包文件的完整路径
    """
    filename = os.path.abspath(os.path.join(output_path, output_name))
    if output_name.endswith('.tar'):
        f = tarfile.open(filename, "w:")
    elif output_name.endswith('.tar.gz'):
        f = tarfile.open(filename, "w:gz")
    elif output_name.endswith('.gz'):
        f = GzipFile(filename=filename)
    else:
        f = zipfile.ZipFile(filename,
                            'w', zipfile.ZIP_DEFLATED)
    file_list = []
    with pushd(input_path):
        for root, dirs, files in os.walk('.', topdown=True):
            for name in files:
                file_list.append(os.path.join(root, name))
        try:
            if not output_name.endswith('.tar'):
                for fi in file_list:
                    f.write(fi)
            else:
                for fi in file_list:
                    f.add(fi)
        finally:
            f.close()
    return filename


def get_sha1(path: str) -> str:
    """
    获取一个文件的SHA1校验值，返回值是一个字符串。

    :param path: 目标文件名
    :return: SHA1字符串
    """
    sha1_obj = hashlib.sha1()
    a = open(path, 'rb')
    while True:
        b = a.read(128000)
        sha1_obj.update(b)
        if not b:
            break
    a.close()
    return sha1_obj.hexdigest()


def get_md5(path: str) -> str:
    """
    获取一个文件的MD5校验值，返回值是一个字符串。

    :param path: 目标文件名
    :return: SHA1字符串
    """
    md5_obj = hashlib.md5()
    a = open(path, 'rb')
    while True:
        b = a.read(128000)
        md5_obj.update(b)
        if not b:
            break
        a.close()
    return md5_obj.hexdigest()


class ExtendedDict(dict):
    """
    增强版的字典类型, 其实只是重写了 __getattr__ 和 __setattr__ 。
    """
    def __getattr__(self, k):
        return self[k]

    def __setattr__(self, key, value):
        self[key] = value


def parent_dir(path: str):
    """
    获取 path 的父路径, 仅支持绝对路径。

    :param path: 希望获取父路径的路径字符串
    :return: 父路径字符串
    """
    return os.path.abspath(path)[:-len(os.path.basename(path))]

