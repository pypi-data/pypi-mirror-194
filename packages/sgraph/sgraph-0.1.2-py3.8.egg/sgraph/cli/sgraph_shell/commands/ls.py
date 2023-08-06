from sgraph.cli.sgraph_shell.commands.commandresult import CommandResult
from sgraph.cli.sgraph_shell.filesystem.path_handler import create_file_abstraction


class LsCommand:

    def __init__(self):
        pass

    def execute(self, _command_input, cmd, graph, state) -> CommandResult:
        output = []
        errors = []
        try:
            if not cmd.path_refs:
                # case: ls
                element = state['current_location']
                output = self.execute_for_element(element)
            elif len(cmd.path_refs) == 1:
                # case: ls fname
                file = create_file_abstraction(cmd.path_refs[0], state)
                if file.exists(graph):
                    output = self.execute_for_element(file.resolved_element)
                else:
                    errors.append(f'Not found: {file.relative_path} abs: {file.absolute_path}')
            else:
                # case: ls a b c
                for path_ref in cmd.path_refs:
                    file = create_file_abstraction(path_ref, state)
                    if file.exists(graph):
                        output.append(path_ref + ':')
                        output.append(self.execute_for_element(file.resolved_element))
                        output.append('')
                    else:
                        errors.append(f'Not found: {file.relative_path} abs:{file.absolute_path}')

            return CommandResult(output=output, errors=errors, return_code=1 if errors else 0)

        except Exception as e:
            return CommandResult(output=[], errors=[str(e)], return_code=1)

    def execute_for_element(self, element):
        listing = [f'<element>    {x.name}' for x in element.children]
        if element.outgoing:
            listing.append('<meta>       outgoing.json')
        if element.incoming:
            listing.append('<meta>       incoming.json')
        if element.attrs:
            listing.append('<meta>       attributes.json')
        return listing
