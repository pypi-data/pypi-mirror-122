"""
aws s3 命令行封装
"""
import s3fs
import os
from typing import List

class S3Helper:
    def __init__(self):
        self.s3 = s3fs.S3FileSystem(anon=False)

    def listdir(self, s3_path: str) -> List[str]:
        """
        查看目录下的文件列表
        """
        return self.s3.ls(s3_path)

    def copy(self, path1: str, path2: str):
        """
        双向复制文件
        """
        # s3 -> local
        if not path1.lower().startswith('s3'):
            self.s3.get_file(path1, path2)
        # local -> s3
        else:
            self.s3.put_file(path1, path2)

    def move(self, path1: str, path2: str):
        """
        移动s3上的文件的位置
        """
        if not path1.lower().startswith('s3') or not path2.lower().startswith('s3'):
            raise Exception("你指定的不是s3路径")
        else:
            self.s3.move(path1, path2)

    def rm(self, s3_path: str):
        """
        删除s3上的文件
        """
        self.s3.rm(s3_path)

    def rm_dir(self, s3_path: str):
        """
        递归删除s3上的文件夹及其文件
        """
        self.s3.rm(s3_path, recursive=True)

    def sync(self, path1: str, path2: str, exclude: List[str]):
        """
        使用递归的方式，同步文件夹
        如果 path1 是 local_path, 则是将本地文件同步到 s3，
        如果 path1 是 s3_path，则是将 s3 上的文件夹同步到本地
        exclude：要排除的文件类型，比如 [.log, .csv] 等
        aws s3 sync local_path s3_path --exclude "*.csv" --exclude "*.log"    # 排除csv文件和log文件
        """
        # s3 -> local
        if path1.lower().startswith('s3'):
            self.s3.get(path1, path2, recursive=True)
        # local -> s3
        else:
            self.s3.put(path1, path2, recursive=True)
