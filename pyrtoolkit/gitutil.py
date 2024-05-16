import subprocess
from pathlib import Path
from typing import List

# 現在のブランチ名を取得する
def git_current_branch_name(root_folder: Path = Path.cwd()):
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        cwd=root_folder
    )
    return result.stdout.decode().strip()

# 最後のコミットのハッシュを取得する
def git_current_commit_hash(root_folder: Path = Path.cwd()):
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True,
        cwd=root_folder,
    )
    return result.stdout.decode("ascii").strip()

# 最後のコミットからの変更があるか調べる
def git_is_file_updated(root_folder: Path = Path.cwd()) -> None | List[str]:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        cwd=root_folder,
    )
    output = result.stdout.decode().strip()
    if output == "":
        return None
    status_files = output.split("\n")
    return status_files
