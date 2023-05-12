from flask import Flask, render_template
from flask import request, jsonify
from pycparser import c_parser, c_ast
import ast
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def hello_world():
    return render_template('prototype.html')

@app.route('/description')
def description():
    return render_template('description.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')
#_________________________________________________________________________________________________________
class TypeChecker(c_ast.NodeVisitor):
    def __init__(self):
        self.variables = {}

    def visit_Decl(self, node):
        if isinstance(node.type, c_ast.IdentifierType):
            typename = ' '.join(node.type.names)
            self.variables[node.name] = typename

    def visit_BinaryOp(self, node):
        if isinstance(node.left, c_ast.ID) and isinstance(node.right, c_ast.ID):
            left_var_name = node.left.name
            right_var_name = node.right.name
            if left_var_name not in self.variables:
                return f"Error: variable '{left_var_name}' not defined."
            elif right_var_name not in self.variables:
                return f"Error: variable '{right_var_name}' not defined."
            else:
                left_var_type = self.variables[left_var_name]
                right_var_type = self.variables[right_var_name]
                if left_var_type != right_var_type:
                    return f"Error: Type mismatch between variables '{left_var_name}' and '{right_var_name}'."
        return self.generic_visit(node)

def perform_semantic_analysis(program):
    errors = []
    lines = program.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.endswith(';'):
            parts = line[:-1].split('=')
            var_name = parts[0].strip()
            if len(parts) > 1 and '.' in parts[1]:
                var_type = None
                for keyword in ['int', 'char', 'short', 'long', 'bool']:
                    if keyword in line:
                        var_type = keyword
                        break
                if var_type:
                    errors.append(f"Type error: float value assigned to variable '{var_name}' of type '{var_type}'")
    print(errors)
    return errors









#_______________________________________________________________________________________________________
# def perform_semantic_analysis(program):
#     # Create an empty symbol table
#     symbol_table = {}

#     # Split the program into lines
#     lines = program.split('\n')

#     # Initialize the result string
#     result = "Semantic Analysis:\n\n"

#     # Perform semantic analysis on each line of the program
#     for i, line in enumerate(lines):
#         # Remove any whitespace from the line
#         line = line.strip()

#         # Ignore empty lines and comment lines
#         if not line or line.startswith('//'):
#             continue

#         # Check for variable declarations and add them to the symbol table
#         if 'int ' in line or 'float ' in line:
#             words = line.split()
#             var_name = words[1]
#             var_type = words[0]
#             symbol_table[var_name] = var_type

#             # Add the symbol to the result string
#             result += f"Added variable '{var_name}' of type '{var_type}' to symbol table.\n"

#         # Check for arithmetic operations and perform type checking
#         if '+' in line or '-' in line or '*' in line or '/' in line:
#             words = line.split()
#             operands = []
#             for word in words:
#                 if word in symbol_table:
#                     operands.append(symbol_table[word])
#             if len(operands) == 2 and operands[0] != operands[1]:
#                 error = f"Error at line {i+1}: invalid types in arithmetic operation ({words[1]}). Expected {operands[0]}, but got {operands[1]}."
#                 result += error + "\n"

#         # Check for printf statements and type check the argument
#         if 'printf' in line:
#             words = line.split('"')
#             format_string = words[1]
#             argument = words[2][1:-3]
#             if argument in symbol_table and symbol_table[argument] != 'float':
#                 error = f"Error at line {i+1}: invalid argument type in printf statement. Expected float, but got {symbol_table[argument]}."
#                 result += error + "\n"

#     # Add the symbol table to the result string
#     result += "\nSymbol Table:\n--------------\n"
#     result += "name    | type\n"
#     result += "------- | ----\n"
#     for name, var_type in symbol_table.items():
#         result += f"{name:<8} | {var_type}\n"

#     # Add the type checking results to the result string
#     result += "\nType Checking:\n--------------\n"
#     type_errors = [line for line in result.split('\n') if 'invalid types' in line or 'invalid argument' in line]
#     if not type_errors:
#         result += "No type errors found.\n"
#     else:
#         result += '\n'.join(type_errors) + '\n'

#     # Add the scoping results to the result string
#     result += "\nScoping:\n--------\n"
#     for name in symbol_table:
#         result += f"Variable {name} is valid in scope.\n"

#     return result
#_______________________________________________________________________________________________________________


@app.route('/analyze', methods=['POST'])
def analyze():
    app.logger.info("Got req")
    input_data = request.json
    #print(input_data)
    app.logger.info(input_data)
    output_data = perform_semantic_analysis(input_data)
    print('The output data is ',output_data)
    response = {'result': output_data}
    print(response)
    return jsonify(response)


if __name__=="main":
    app.run(debug=True)
