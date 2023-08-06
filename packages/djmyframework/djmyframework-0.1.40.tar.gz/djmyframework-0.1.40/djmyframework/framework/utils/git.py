# -*- coding: utf-8 -*-
# @Time    : 2023/1/3 14:38 
# @Author  : xzr
# @File    : git.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :
import inspect
import os

os.environ["GIT_PYTHON_REFRESH"] = "quiet"

def find_git_author(repo_path, file_path, line_num):
    from git import Repo, Commit
    repo = Repo(repo_path)
    tlc = 0
    for commit, lines in repo.blame('HEAD', file_path):
        tlc += len(lines)
        if tlc >= line_num:
            return commit
    return None


def get_last_frame_fileinfo(filter_root_path='') -> (str, int):
    traces = inspect.trace()
    if traces:
        for last_frame in traces[::-1]:
            if last_frame.filename.startswith(filter_root_path):
                yield last_frame.filename.replace(filter_root_path, '', 1).lstrip(os.path.sep), last_frame.lineno
    yield '', 0


def get_track_msg_author_info(filename='', lineno=0, repo_path='./', ) -> str:
    try:
        commit = find_git_author(repo_path, filename, lineno)
        return f'@{commit.author.name} : {commit.summary}' if commit else ''
    except Exception as e:
        return ''
