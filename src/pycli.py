import re
import ast
import sys


available_modules = [module for module in sys.modules.keys() if not module.startswith('_')]


def add_imports(command_string):
    matches = re.findall(r'([\w.]+)\.\w+', command_string)
    imports = []
    for match in matches:
        if match in available_modules:
            imports.append(match)

    if len(imports) > 0:
        return f'import {",".join(imports)}; {command_string}'
    return command_string


def execute_command(command_string: str, line: str) -> str:
    syntax_tree = ast.parse(command_string)
    syntax_tree.body[-1] = ast.parse('output = ' + ast.unparse(syntax_tree.body[-1])).body[0]

    internal_locals = {'line': line}
    exec(compile(syntax_tree, '<string>', 'exec'), None, internal_locals)
    return internal_locals.get('output')


def main(argv: list) -> None:
    command_string = argv[1]

    command_with_imports = add_imports(command_string)
    if len(argv) == 2:
        for line in sys.stdin:
            print(execute_command(command_with_imports, line))
    else:
        with open(argv[2]) as file_handler:
            for line in file_handler.readlines():
                print(execute_command(command_string, line))


if __name__ == "__main__":
    main(sys.argv)
