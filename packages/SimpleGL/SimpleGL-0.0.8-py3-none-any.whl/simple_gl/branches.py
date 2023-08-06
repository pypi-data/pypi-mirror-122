# -*- coding: utf-8 -*- 
# @Time : 10/8/21 2:59 PM 
# @Author : mxt
# @File : branches.py
import logging
from typing import *
from .utils import time_format, get_time_diff
from simple_gl.gitlab_base import GitLabBase, MergeRequestResponse


class Branches(GitLabBase):
    def __init__(self, url: str = "", private_token: str = ""):
        super(Branches, self).__init__(url=url, private_token=private_token)

    # 创建分支
    def create_branch(self, project_id: Union[str, int], branch: str = "", ref: str = ""):
        try:
            project = self.gl.projects.get(project_id)
            _branch = project.branches.create({
                "branch": branch,
                "ref": ref
            })
            return _branch
        except Exception as e:
            logging.getLogger(__name__).error("Branches.create_branch.error: %s" % str(e))
            return False

    # 删除分支
    def delete_branch(self, project_id: Union[str, int], branch: str = ""):
        try:
            project = self.gl.projects.get(project_id)
            project.branches.delete(branch)
        except Exception as e:
            logging.getLogger(__name__).error("Branches.delete_branch.error: %s" % str(e))

    # 保护分支
    def protect_branch(self, project_id: Union[str, int], branch: str = "",
                       developers_can_push: bool = True, developers_can_merge: bool = True):
        try:
            project = self.gl.projects.get(project_id)
            _branch = project.branches.get(branch)
            _branch.protect(developers_can_push=developers_can_push, developers_can_merge=developers_can_merge)
        except Exception as e:
            logging.getLogger(__name__).error("Branches.protect_branch.error: %s" % str(e))

    # 代码合并
    def merge_requests(self, project_id: Union[str, int], source_branch: str = "", target_branch: str = "",
                       title: str = "", description: str = ""):
        try:
            project = self.gl.projects.get(project_id)
            try:
                mr = project.mergerequests.create({
                    "source_branch": source_branch,
                    "target_branch": target_branch,
                    "title": title,
                    "description": description
                })
            except:
                mr = project.mergerequests.list(
                    source_branch=source_branch,
                    target_branch=target_branch,
                    state="opened"
                )[0]
            attr = mr.changes()
            commit_num = set(attr.get("diff_refs").values())
            name = attr.get("author").get("name")
            username = attr.get("author").get("username")
            created_at = get_time_diff(time_format(attr.get("created_at")))
            if attr.get("merge_status") == "can_be_merged":
                mr.merge()
                status = "0"
                navigete_to = ""
                message = u"由%s(%s)发起的合并请求：%s合并至%s，合并成功，正在触发流水线。" % (
                    name, username, source_branch, target_branch
                )
            else:
                status = "3" if len(commit_num) < 3 else "2"
                navigete_to = attr.get("web_url")
                message = u"%s由%s(%s)发起的合并请求：%s合并至%s请求失败，请处理后再次发起。" % (
                    created_at, name, username, source_branch, target_branch
                )
            return MergeRequestResponse(
                status=status, message=message, navigateTo=navigete_to
            )
        except Exception as e:
            logging.getLogger(__name__).error("Branches.merge_requests.error: %s" % str(e))
            return False
