import os

import pytest

from pymermaid2dir.fsnode import FileInfo, FolderTree, Node, SymlinkNode


def test_node():
    parent_i_node = "parent_i_node"
    parent_i_name = "parent_i_name"
    current_i_node = "current_i_node"
    current_i_name = "current_i_name"
    child_i_node = "child_i_node"
    child_i_name = "child_i_name"

    node = Node(
        parent_i_node,
        parent_i_name,
        current_i_node,
        current_i_name,
        child_i_node,
        child_i_name,
    )

    assert node.parent_i_node == parent_i_node
    assert node.parent_i_name == parent_i_name
    assert node.current_i_node == current_i_node
    assert node.current_i_name == current_i_name
    assert node.child_i_node == child_i_node
    assert node.child_i_name == child_i_name

    node = Node(
        parent_i_node=parent_i_node,
        current_i_node=current_i_node,
        child_i_name=child_i_name,
    )
    assert node.parent_i_node == parent_i_node
    assert node.parent_i_name is None
    assert node.current_i_node == current_i_node
    assert node.current_i_name is None
    assert node.child_i_node is None
    assert node.child_i_name == child_i_name


def test_symlink_node():
    parent_i_node = "parent_i_node"
    parent_i_name = "parent_i_name"
    current_i_node = "current_i_node"
    current_i_name = "current_i_name"
    link_i_node = "link_i_node"
    link_i_name = "link_i_name"

    symlink_node = SymlinkNode(
        parent_i_node,
        parent_i_name,
        current_i_node,
        current_i_name,
        link_i_node,
        link_i_name,
    )

    assert symlink_node.parent_i_node == parent_i_node
    assert symlink_node.parent_i_name == parent_i_name
    assert symlink_node.current_i_node == current_i_node
    assert symlink_node.current_i_name == current_i_name
    assert symlink_node.link_i_node == link_i_node
    assert symlink_node.link_i_name == link_i_name

    symlink_node = SymlinkNode(
        parent_i_node=parent_i_node,
        current_i_node=current_i_node,
        link_i_name=link_i_name,
    )
    assert symlink_node.parent_i_node == parent_i_node
    assert symlink_node.parent_i_name is None
    assert symlink_node.current_i_node == current_i_node
    assert symlink_node.current_i_name is None
    assert symlink_node.link_i_node is None
    assert symlink_node.link_i_name == link_i_name


@pytest.fixture
def file_info():
    return FileInfo("test.txt", "sample/f2.txt", True, False)


def test_file_info_name(setup_testfolder, file_info):
    assert file_info.name == "test.txt"


def test_file_info_path(setup_testfolder, file_info):
    assert file_info.path == "sample/f2.txt"


def test_file_info_is_file(setup_testfolder, file_info):
    assert file_info.is_file is True


def test_file_info_is_symlink(setup_testfolder, file_info):
    assert file_info.is_symlink is False


def test_file_info_target_path(setup_testfolder, file_info):
    assert file_info.target_path is None


def test_file_info_target_is_file(setup_testfolder, file_info):
    assert file_info.target_is_file is None


def test_folder_tree(setup_testfolder):
    # FolderTreeオブジェクトを作成し、ツリー構造を走査する
    root = "sample"
    tree = FolderTree(root)
    relations = list(tree.get_relation())

    # Check the relations
    assert len(relations) == 7

    # Check the first relation is a Node
    assert isinstance(relations[0], Node)
    assert relations[0].parent_i_node == str(os.stat(root).st_ino)
    assert relations[0].parent_i_name == os.path.basename(root)
    assert relations[0].current_i_node == str(
        os.stat(os.path.join(root, "f2.txt")).st_ino
    )
    assert relations[0].current_i_name == "f2.txt"
    assert relations[0].child_i_node is None
    assert relations[0].child_i_name is None
