from typing import Any, Dict, List

from sgraph.cli.sgraph_shell.commands.commandresult import CommandResult


class CommandAbstraction:

    def execute(self, command_input: List[str], cmd, graph,
                state: Dict[str, Any]) -> CommandResult:
        raise Exception('Not implemented')
