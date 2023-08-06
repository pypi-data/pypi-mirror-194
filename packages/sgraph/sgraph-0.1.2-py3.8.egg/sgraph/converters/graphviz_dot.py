

def graph_to_dot(g):
    out = 'digraph G {'
    deps = []

    def handle_elem(elem, indent):
        out_element = ''
        if elem.children:
            subgraph_id = id(elem)
            c = '	'
            out_element += c * indent + 'subgraph cluster' + str(subgraph_id) + ' {\n'

            for child in elem.children:
                if not child.children:
                    n = str(id(child))
                    for assoc in child.outgoing:
                        used = assoc.toElement
                        if used.children:
                            pass
                        else:
                            deps.append((n, str(id(used)), assoc.deptype))

                    out_element += c * (indent + 1) + n + ' [label="' + child.name + '"];\n'
                else:
                    out_element += handle_elem(child, indent + 1)
            if elem.name:
                out_element += c * (indent + 1) + 'label = "' + elem.name + '";\n'
            out_element += c * indent + '}\n'
        return out_element

    out += handle_elem(g.rootNode, indent=1)
    out += '\n'
    for a, b, t in deps:
        out += '   ' + a + ' -> ' + b + ' [label = "' + t + '"];\n'
    out += '}\n'
    return out
