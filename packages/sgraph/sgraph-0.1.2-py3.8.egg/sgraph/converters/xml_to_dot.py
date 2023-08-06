import sys

from sgraph import SGraph
from sgraph.converters.graphviz_dot import graph_to_dot

inputfilepath = sys.argv[1]
outfilepath = None
if len(sys.argv) > 2:
    outfilepath = sys.argv[2]

egm = SGraph.parse_xml_or_zipped_xml(inputfilepath)

print(graph_to_dot(egm))