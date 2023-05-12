import ast

# def analyze_python_program(program):
#     """
#     Analyze a Python program and return a list of semantic errors.

#     :param program: str, the Python program to analyze
#     :return: list of str, the semantic errors found in the program
#     """
#     errors = []

#     # Parse the Python program
#     try:
#         parsed_program = ast.parse(program)
#     except SyntaxError as e:
#         errors.append(f"Syntax error: {e}")
#         return errors

#     # Traverse the AST and check for semantic errors
#     for node in ast.walk(parsed_program):
#         if isinstance(node, ast.Call):
#             if isinstance(node.func, ast.Attribute):
#                 if node.func.attr == 'append':
#                     if isinstance(node.func.value, ast.Name) and node.func.value.id == 'list':
#                         errors.append(f"Using 'list.append' is not recommended, use the '+' operator instead. Line {node.lineno}")
#             elif isinstance(node.func, ast.Name):
#                 if node.func.id == 'print':
#                     errors.append(f"Using 'print' is not recommended, use logging instead. Line {node.lineno}")

#     return errors
def perform_semantic_analysis(program):
    # Create an empty symbol table
    symbol_table = {}

    # Split the program into lines
    lines = program.split('\n')

    # Initialize the result string
    result = "Semantic Analysis:\n\n"

    # Perform semantic analysis on each line of the program
    for i, line in enumerate(lines):
        # Remove any whitespace from the line
        line = line.strip()

        # Ignore empty lines and comment lines
        if not line or line.startswith('//'):
            continue

        # Check for variable declarations and add them to the symbol table
        if 'int ' in line or 'float ' in line:
            words = line.split()
            var_name = words[1]
            var_type = words[0]
            symbol_table[var_name] = var_type

            # Add the symbol to the result string
            result += f"Added variable '{var_name}' of type '{var_type}' to symbol table.\n"

        # Check for arithmetic operations and perform type checking
        if '+' in line or '-' in line or '*' in line or '/' in line:
            words = line.split()
            operands = []
            for word in words:
                if word in symbol_table:
                    operands.append(symbol_table[word])
            if len(operands) == 2 and operands[0] != operands[1]:
                error = f"Error at line {i+1}: invalid types in arithmetic operation ({words[1]}). Expected {operands[0]}, but got {operands[1]}."
                result += error + "\n"

        # Check for printf statements and type check the argument
        if 'printf' in line:
            words = line.split('"')
            format_string = words[1]
            argument = words[2][1:-3]
            if argument in symbol_table and symbol_table[argument] != 'float':
                error = f"Error at line {i+1}: invalid argument type in printf statement. Expected float, but got {symbol_table[argument]}."
                result += error + "\n"

    # Add the symbol table to the result string
    result += "\nSymbol Table:\n--------------\n"
    result += "name    | type\n"
    result += "------- | ----\n"
    for name, var_type in symbol_table.items():
        result += f"{name:<8} | {var_type}\n"

    # Add the type checking results to the result string
    result += "\nType Checking:\n--------------\n"
    type_errors = [line for line in result.split('\n') if 'invalid types' in line or 'invalid argument' in line]
    if not type_errors:
        result += "No type errors found.\n"
    else:
        result += '\n'.join(type_errors) + '\n'

    # Add the scoping results to the result string
    result += "\nScoping:\n--------\n"
    for name in symbol_table:
        result += f"Variable {name} is valid in scope.\n"
    print(result)
    return result

# program = """
# import cmath

# a = 1
# b = 5
# c = 6
# d = (b**2) - (4*a*c)
# sol1 = (-bcmath.sqrt(d))/(2*a)
# sol2 = (-b+cmath.sqrt(d))/(2*a)

# logging('The solution are {0} and {1}'.format(sol1,sol2))

# """

#errors = analyze_python_program(program)


# if errors:
#     print("The following semantic errors were found:")
#     for error in errors:
#         print(error)
# else:
#     print("No semantic errors were found.")

program = '#include <stdio.h>\n\nint main() {\n    int x = 5;\n    int y = 7;\n    float z = x + y;\n    printf("z = %f\\n", z);\n    return 0;\n}'
result = perform_semantic_analysis(program)
print(result)
