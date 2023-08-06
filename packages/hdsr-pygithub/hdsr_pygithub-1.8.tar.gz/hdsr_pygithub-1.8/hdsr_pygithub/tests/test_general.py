from github import BadCredentialsException
from hdsr_pygithub import exceptions
from hdsr_pygithub import GithubFileDownloader
from hdsr_pygithub.downloader.base import GithubDownloaderBase
from pathlib import Path

import pytest


def test_wrong_token():
    repo_name = "startenddate"
    target_file = Path("data/output/results/mwm_peilschalen_short.csv")
    with pytest.raises(BadCredentialsException):
        GithubFileDownloader(repo_name=repo_name, target_file=target_file, personal_access_token="xxx")


def test_repo_does_not_exist():
    repo_name = "xxx"
    target_file = Path("xxx")
    with pytest.raises(exceptions.GithubRepoInstanceError):
        GithubFileDownloader(repo_name=repo_name, target_file=target_file)


def test_not_main_branch_works():
    repo_name = "FEWS-WIS_HKV"
    file = Path("FEWS/Config/IdMapFiles/IdOPVLWATER.xml")
    for branch_name in ("productie", "test"):
        downloader = GithubFileDownloader(repo_name=repo_name, target_file=file, branch_name=branch_name)
        expected = f"https://api.github.com/repos/hdsr-mid/{repo_name}/contents/{file.as_posix()}?ref={branch_name}"
        assert downloader.downloadable_content.url == expected


def test_avoid_instance_base_class():
    repo_name = "FEWS-WIS_HKV"
    with pytest.raises(TypeError):
        GithubDownloaderBase(repo_name=repo_name)
