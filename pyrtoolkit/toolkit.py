import sys
import platform
import datetime
import toml
from pathlib import Path
from typing import Optional, Dict, Any

from .gitutil import git_is_file_updated, git_current_commit_hash, git_current_branch_name

# 更新がコミットされていない場合終了する。
def assert_file_is_not_modified(root_folder: Path = Path.cwd()):
    fileUpdated = git_is_file_updated(root_folder)
    if fileUpdated:
        print("The updated file has not been committed", file=sys.stderr)
        print("Please commit the changes before executing.", file=sys.stderr)
        for line in fileUpdated:
            print(line, file=sys.stderr)
        sys.exit(1)

# メタデータを習得する
def generate_metadata(
    root_folder: Path = Path.cwd(),
    description: Optional[str] = None,
) -> Dict[str, Any]:
    now = datetime.datetime.now()
    branch = git_current_branch_name(root_folder)
    hash = git_current_commit_hash(root_folder)
    change_status = git_is_file_updated(root_folder)

    metadata = {
        "date": now.isoformat(),
        "computer": platform.node(),
        "platform": platform.platform(),
        "branch": branch,
        "commit": hash,
        "status": change_status if change_status else [],
        "command": " ".join(sys.argv),
    }

    if description is not None:
        metadata["description"] = description

    return metadata
    
# output_folder/meta.tomlにメタデータを生成する
def log_metadata(
    root_folder: Path = Path.cwd(),
    output_folder: Optional[Path] = None,
    description: Optional[str] = None,
) -> None:
    now = datetime.datetime.now()
    hash = git_current_commit_hash(root_folder)

    # 出力フォルダが指定されていないときは/output/<hash>/YYYY-mm-DD_HH_MM_SSとする
    if output_folder is None:
        output_folder = (
            root_folder / "output" / hash[:7] / now.strftime("%Y-%m-%d_%H_%M_%S")
        )

    # メタデータを記録したファイルを出力する
    output_folder.mkdir(parents=True, exist_ok=True)
    metadata_file = output_folder / "meta.toml"
    
    metadata = generate_metadata(
        root_folder=root_folder,
        description=description,
    )
    with metadata_file.open("wt") as f:
        toml.dump(metadata, f)
    