import subprocess

from sgraph.cli.sgraph_shell.commands.commandresult import CommandResult
from sgraph.cli.sgraph_shell.filesystem.path_handler import create_file_abstraction


class SGraphVisualizeCommand:
    def __init__(self):
        pass

    def execute(self, command_input, cmd, _graph, state) -> CommandResult:
        if cmd.target_file:
            output_filename = cmd.target_file
        else:
            output_filename = '/tmp/foo.png'

        from sgraph.converters.graphviz_dot import graph_to_dot
        dot_data = graph_to_dot(_graph)
        print(dot_data)
        # Format flag

        dot = subprocess.Popen(['dot', '-T', 'png', '-o', output_filename], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #dot.stdin.write(dot_data)
        (dot_out, dot_err) = dot.communicate(input=dot_data.encode())
        print(dot_out)
        print(dot_err)
        print(dot.returncode)

        subprocess.run(['xdg-open', output_filename])
        # visualizing: kitty +kitten icat

        return CommandResult(output=[state['current_location'].getPath()], errors=[''],
                             return_code=0)
