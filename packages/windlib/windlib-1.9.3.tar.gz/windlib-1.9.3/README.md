# **Windlib**

有用的函数库，由SNWCreations创建。

只是为个人使用而编写，但我希望这能帮助到你。

## **用法**

### **typeof**

typeof(variate) -> str

检测变量类型，返回字符串。

示例:

    >>> a = 10
    >>> typeof(a)
    'int'

---

### **extract**

extract(filename: str, target_dir: str) -> None

支持 ".zip" ".gz" ".tar" ".rar" ".tar.gz" 文件。

示例:

    >>> extract('a.zip', 'a')
    >>>

---

### **get_file**

get_file(url: str, save_path: str) -> str

从互联网下载文件。

参数:

    url: 被下载文件的URL
    save_as_name: 文件在本地上将要使用的名称, 默认为 URL 指向的文件的名称
    save_path: 保存路径，默认为当前路径
    timeout: 超时时长，单位为秒，默认为 10
    headers: 请求头，默认为一个 Windows Chrome 的 UA
    md5: 如果提供此项, 在下载完成后会将此项的值作为校验值检查文件完整性
    sha1: 如果提供此项, 在下载完成后会将此项的值作为校验值检查文件完整性
    max_retries: 如果提供此项, 当下载失败时会重试, 直到下载完成或已重试次数超出限制
    no_overwrite: 如果此项不为 False, 则当本地存在与使用 文件在本地上将要使用的名称 命名的文件时引发 FileExistsError 异常。

返回: 下载后的文件名

可能引发的异常: 当 请求出错 时, 会引发 requests 库的某个原生异常。

当 no_overwrite 的值不为 False, 则当本地存在与使用 文件在本地上将要使用的名称 命名的文件时引发 FileExistsError 异常。

---

### **find_files_with_the_specified_extension**

find_files_with_the_specified_extension(file_type: str, folder: str, slient: bool) -> list

在目标文件夹中找到具有指定扩展名的文件，返回值是一个列表。

参数:

    folder: 从哪里查找，默认值为当前目录。
    file_type: 一个扩展名，不需要带有 “.” 。例如 "txt", "jar", "md", "class" 或 ".txt" ".jar" ".md" ".class".

返回: 被筛选的文件名的列表

---

### **copy_file**

copy_file(src: str or Iterable, dst: str) -> None

复制文件（或文件夹）到指定的目录。

可以通过列表的方式同时将多个文件复制到指定目录。

参数:

    src: 源文件或目录
    dst: 目标路径

---

### **is_it_broken**

is_it_broken(path: str or list) -> bool or list

检查一个文件（或目录）是否损坏。

允许调用时通过列表检查大量文件和目录。

若使用列表来检查文件，则返回一个记录所有损坏的文件路径的列表。

参数:

    path: 文件路径

示例:

    >>> is_it_broken('./aaa.txt')
    False
    >>> is_it_broken(['./aaa.txt', './bbb.txt', './ccc.txt'])
    []

---

### **pushd**

pushd(new_dir: str)

临时切换到一个目录，操作完成后自动返回调用前路径。

此函数为生成器，请配合 with 语句使用。

参数:

    new_dir: 路径

示例:

    >>> print(os.getcwd())
    'D:\\windlib-test'
    >>> with pushd('./aaa'):
    ...    print(os.getcwd())
    'D:\\windlib-test\\aaa'
    >>> print(os.getcwd())
    'D:\\windlib-test'

---

### **compress**

compress(input_path: str, output_name: str, output_path: str = '.', ext='zip') -> str

压缩一个目录下的所有文件到一个zip文件，无返回值。

参数:

    input_path: 压缩的文件夹路径

    output_name: 压缩包名称 (不需要带扩展名)

    output_path: 输出的路径

    ext: 压缩包类型 (有效值: 'zip', 'tar', 'tar.gz')

    返回: 压缩包文件的完整路径

示例:

    >>> compress('./a', 'a', ext='zip')
    'D:\windlib-test\a.zip'
    >>>

---

### **get_sha1**

get_sha1(path: str) -> str

获取一个文件的SHA1校验值，返回值是一个字符串。

参数:

    path: 文件路径

示例:

    >>> get_sha1('setup.py')
    'acdf35508f4dfb49e522f161a3e3e885adbf3b99'

---

### **get_md5**

get_md5(path: str) -> str

获取一个文件的MD5校验值，返回值是一个字符串。

参数:

    path: 文件路径

示例:

    >>> get_md5('setup.py')
    'ec210fa5cc05bed851da3fe222b733a9'

---

### **parent_dir**

获取 path 的父路径, 仅支持绝对路径。

参数:

    path: 希望获取父路径的路径字符串

示例:
    
    >>> parent_dir('aaa/bbb/ccc')
    'aaa/bbb/'

---

### **ExtendedDict**

增强版的字典类型, 其实只是重写了 __getattr__ 和 __setattr__ 。

示例:
    
    >>> exdict = ExtendedDict(a='bbb', c='ddd')
    >>> exdict
    {'a': 'bbb', 'c': 'ddd'}
    >>> exdict.a = 'eee' # __setattr__
    >>> exdict.a # __getattr__
    'eee'

---

版权所有 (C) 2021 SNWCreations。

欢迎对此库做出 Commit 和 Pull Request!
