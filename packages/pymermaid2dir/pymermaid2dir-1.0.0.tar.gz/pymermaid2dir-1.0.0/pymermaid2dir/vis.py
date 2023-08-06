from pathlib import Path
from typing import Union

from pymermaid2dir.fsnode import FolderTree, Node, SymlinkNode
from pymermaid2dir.graph import MermaidFlowchart


def to_markdown(root_folder: Union[str, Path], *, output: str = "markdown") -> str:
    """
    Convert a directory to mermaid syntax in Markdown format.

    Args:
        root_folder (Union[str, Path]): The directory to convert.
        output (str, optional): The type of output. Defaults to "markdown".

    Returns:
        str: The mermaid syntax after conversion.
    """
    mermaid = MermaidFlowchart()

    if isinstance(root_folder, Path):
        root_folder = str(root_folder)
    folder = FolderTree(root_folder)

    for node in folder.get_relation():
        if isinstance(node, Node):
            if node.parent_i_node is None:
                continue
            mermaid.add_edge(
                from_i_node=node.current_i_node,
                from_node=node.current_i_name,
                to_i_node=node.child_i_node,
                to_node=node.child_i_name,
                parent_i_node=node.parent_i_node,
                parent_node=node.parent_i_name,
            )
        elif isinstance(node, SymlinkNode):
            if node.parent_i_node is None:
                continue
            mermaid.add_edge(
                from_i_node=node.current_i_node,
                from_node=node.current_i_name,
                to_i_node=node.link_i_node,
                to_node=node.link_i_name,
                parent_i_node=node.parent_i_node,
                parent_node=node.parent_i_name,
            )

    if output == "markdown":
        print(mermaid.to_markdown())
    else:
        # [TODO]現在の別モードがないのでMarkdownを設定
        print(mermaid.to_markdown())

    return mermaid.to_markdown()
