


import re
import ast
import os
from gherkin.parser import Parser
from pytest_bdd import given, when, then, parsers

def parse_gherkin_step(step_str):
    step_pattern = re.compile(r'^(Given|When|Then) (.+)$')
    match = step_pattern.match(step_str)
    if not match:
        raise ValueError(f"Invalid Gherkin step: {step_str}")
    return match.group(1).lower(), match.group(2)

def find_step_location(step_str, directory):
    step_type, step_name = parse_gherkin_step(step_str)

    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                file_content = file.read()

            tree = ast.parse(file_content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Call) and hasattr(decorator.func, 'id'):
                            if decorator.func.id in ['given', 'when', 'then']:
                                # Extract the pattern string from the decorator arguments
                                pattern = None
                                if len(decorator.args) > 0:
                                    arg = decorator.args[0]
                                    if isinstance(arg, ast.Call) and hasattr(arg.func, 'attr') and arg.func.attr == 'parse':
                                        if len(arg.args) > 0:
                                            pattern_arg = arg.args[0]
                                            if isinstance(pattern_arg, ast.Constant):  # Python 3.8+
                                                pattern = pattern_arg.value
                                            elif isinstance(pattern_arg, ast.Str):  # Python 3.7 and earlier
                                                pattern = pattern_arg.s
                                if pattern:
                                    parsed_pattern = parsers.parse(pattern)
                                    regex = parsed_pattern.parser._search_re
                                    if regex.match(step_name):
                                        return filepath, node.lineno

    raise ValueError(f"No matching step definition found for: {step_str}")

def get_step_from_feature(feature_file, line_number):
    with open(feature_file, 'r') as file:
        feature_content = file.read()

    parser = Parser()
    gherkin_document = parser.parse(feature_content)
    feature = gherkin_document['feature']
    scenarios = feature['children']

    for scenario in scenarios:
        for step in scenario['scenario']['steps']:
            if step['location']['line'] == line_number:
                return f"{step['keyword'].strip()} {step['text']}"

    raise ValueError(f"No step found at line {line_number}")

if __name__ == "__main__":
    import sys

    # if len(sys.argv) != 4:
    #     print("Usage: python find_step_ast_parse.py <feature_file> <line_number> <steps_directory>")
    #     sys.exit(1)

 

    line_number = 8


    step_str = get_step_from_feature(feature_file, line_number)
    try:
        file_name, starting_line_number = find_step_location(step_str, steps_directory)
        print(f"Step: {step_str}")
        print(f"File: {file_name}:{starting_line_number}")
        print(f"Starting Line Number: {starting_line_number}")
    except ValueError as e:
        print(e)









