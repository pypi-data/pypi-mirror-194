from pymermaid2dir.graph import MermaidFlowchart


def test_mermaid_flowchart():
    m = MermaidFlowchart()
    m.add_node("Node 1")
    m.add_node("Node 2")
    m.add_edge(
        from_i_node="1", from_node="Node 1", to_i_node="2", to_node="Node 2"
    )
    expected = "```mermaid\ngraph TD;\n  Node 1;\n  Node 2;\n  None[None]-->1[Node 1];\n  1[Node 1]-->2[Node 2];\n```\n"
    assert m.to_markdown() == expected
