import os
from dataclasses import dataclass
from typing import Generator, List, Optional, Union


@dataclass
class Node:
    parent_i_node: Optional[str] = None
    parent_i_name: Optional[str] = None
    current_i_node: Optional[str] = None
    current_i_name: Optional[str] = None
    child_i_node: Optional[str] = None
    child_i_name: Optional[str] = None


@dataclass
class SymlinkNode:
    parent_i_node: Optional[str] = None
    parent_i_name: Optional[str] = None
    current_i_node: Optional[str] = None
    current_i_name: Optional[str] = None
    link_i_node: Optional[str] = None
    link_i_name: Optional[str] = None


class FileInfo:
    def __init__(
        self,
        name: str,
        path: str,
        is_file: bool,
        is_symlink: bool,
        *,
        target_path=None,
        target_is_file=None,
    ):
        self.name = name
        self.path = path
        self.is_file = is_file
        self.is_symlink = is_symlink
        self.target_path = target_path
        self.target_is_file = target_is_file
        self.inode = ""

        if is_symlink:
            self.inode = str(os.lstat(path).st_ino)
        else:
            self.inode = str(os.stat(path).st_ino)


class FolderTree:
    def __init__(self, path: str, parent: Optional[FileInfo] = None):
        self.path = path
        self.name = os.path.basename(path)
        self.parent = parent
        self.inode = os.stat(path).st_ino
        self.files: List[FileInfo] = []
        self.folders: List[FolderTree] = []
        self.__scan(path)

    def __scan(self, path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            is_file = os.path.isfile(item_path)
            is_symlink = os.path.islink(item_path)
            target_path = None
            target_is_file = None
            if is_symlink:
                target_path = os.readlink(item_path)
                target_is_file = os.path.isfile(target_path)
            if is_file or is_symlink:
                self.files.append(
                    FileInfo(
                        item,
                        item_path,
                        is_file,
                        is_symlink,
                        target_path=target_path,
                        target_is_file=target_is_file,
                    )
                )
            else:
                self.folders.append(FolderTree(item_path, parent=self))

    def get_relation(self) -> Generator[Union[Node, SymlinkNode], None, None]:
        for file in self.files:
            if file.is_symlink:
                current_inode = file.inode
                current_name = file.name
                link_inode = str(os.stat(file.target_path).st_ino)
                link_name = os.path.basename(file.target_path)
                yield SymlinkNode(
                    parent_i_node=str(os.stat(self.path).st_ino),
                    parent_i_name=os.path.basename(self.path),
                    current_i_node=current_inode,
                    current_i_name=current_name,
                    link_i_node=str(link_inode),
                    link_i_name=link_name,
                )
            else:
                if self.parent:
                    # 末端以外のファイル
                    yield Node(
                        parent_i_node=str(os.stat(self.parent.path).st_ino),
                        parent_i_name=os.path.basename(self.parent.path),
                        current_i_node=str(self.inode),
                        current_i_name=self.name,
                        child_i_node=str(file.inode),
                        child_i_name=file.name,
                    )
                else:
                    # 末端のファイル
                    yield Node(
                        parent_i_node=str(self.inode),
                        parent_i_name=self.name,
                        current_i_node=str(file.inode),
                        current_i_name=file.name,
                        child_i_node=None,
                        child_i_name=None,
                    )
        for folder in self.folders:
            yield from folder.get_relation()

    def fs_pretty_print(self, indent=0):
        if indent == 0:
            print("  " * indent + self.name + "/")
        else:
            print("  " * indent + "├── " + self.name + "/")

        for file_info in self.files:
            ftype = "file" if file_info.is_file else "symlink"
            if file_info.is_symlink:
                target_type = "file" if file_info.target_is_file else "folder"
                print(
                    "  " * (indent + 1)
                    + "├── "
                    + f"{file_info.name} ({ftype, file_info.inode}) --> {file_info.target_path}({target_type, file_info.inode})"
                )
            else:
                print(
                    "  " * (indent + 1)
                    + "├── "
                    + f"{file_info.name} ({ftype, file_info.inode})"
                )
        for sub in self.folders:
            sub.fs_pretty_print(indent + 1)
