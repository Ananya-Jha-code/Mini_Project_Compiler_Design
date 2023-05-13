var keywords = ["auto", "break", "case", "char", "const", "continue", "default",
    "double", "else", "enum", "extern", "float", "goto", "int", "long", "register", 
    "return", "short", "signed", "sizeof", "static", "struct", "typedef", "union",
    "unsigned", "void", "volatile"];
var operators = ["+", "-", "*", "/", "=", "<", ">", "<=", ">=", "==", "!=",
    "&&", "||", "!", "++", "--", "+=", "-=", "*=", "/="];
var separators = ["(", ")", "{", "}", "[", "]", ";", ","];
var func = ["main"];
var inBuildFunctions = ["for", "do", "if", "printf", "scanf", "switch", "while"];

var BracketStack = [];
var mainAvailable = false;

function analyzeCode(code) {
    var tokens = [];
    var currentToken = "";
    var insideString = false;
    var insideComment = false;

    for (var i = 0; i < code.length; i++) {
        var c = code.charAt(i);
        var nextC = code.charAt(i + 1);
        
        if (insideString) {
            if (c == '"') {
                insideString = false;
                tokens.push({ type: "string", value: currentToken + c });
                currentToken = "";
            } else {
                currentToken += c;
            }
        } else if (insideComment) {
            if (c == "\n") {
                insideComment = false;
                tokens.push({ type: "comment", value: currentToken });
                currentToken = "";
            } else {
                currentToken += c;
            }
        } else if (c == '"') {
            insideString = true;
            currentToken += c;
        } else if (c == '/') {
            if (nextC == '/') {
                insideComment = true;
                currentToken += c + nextC;
                i++;
            } else {
                tokens.push({ type: "operator", value: c });
                currentToken = "";
            }
        } else if (operators.indexOf(c) >= 0) {
            tokens.push({ type: "operator", value: c });
            currentToken = "";
        } else if (separators.indexOf(c) >= 0) {
            tokens.push({ type: "separator", value: c });
            currentToken = "";
        } else if(func.indexOf(currentToken + c) >= 0){
            mainAvailable = true;
            tokens.push({ type: "main_function", value: currentToken + c });
            currentToken = "";
        } else if (/\s/.test(c)) {
            if (currentToken != "") {
                if (keywords.indexOf(currentToken) >= 0) {
                    tokens.push({ type: "keyword", value: currentToken });
                }else if(inBuildFunctions.indexOf(currentToken) >= 0){
                    tokens.push({ type: "inBuildFunctions", value: currentToken});
                }else {
                    tokens.push({ type: "identifier", value: currentToken });
                }
                currentToken = "";
            }
        }
        else {
            currentToken += c;
        }
    }

    if (currentToken != "") {
        if (keywords.indexOf(currentToken) >= 0) {
            tokens.push({ type: "keyword", value: currentToken });
        } else {
            tokens.push({ type: "identifier", value: currentToken });
        }
    }

    return tokens;
}


function checkBracketStack(value) {
    if ((value == ')' && BracketStack[BracketStack.length - 1] == '(') 
                || (value == '}' && BracketStack[BracketStack.length - 1] == '{') 
                    || (value == ']' && BracketStack[BracketStack.length - 1] == '[')) {
        BracketStack.pop();
    }
    else if ( value == '(' || value == '{' || value == '[' || (value == ')' || value == '}' || value == ']') && BracketStack.length == 0){
        BracketStack.push(value);
    }
}


function syntaxAnalyze(tokens) {
    for (var i = 0; i < tokens.length; i++) {
        var token = tokens[i];

        console.log(JSON.stringify(token.value));
        switch (token.type) {
            case 'separator':
                checkBracketStack(token.value);
                break;
            case 'keywords':

                break;
            default:
                break;
        }
    }


    var result = [];


    if( !mainAvailable ){
        result = 'Main Function missing';
    } else if (BracketStack.length > 0) {
        result = 'Error: unclosed parentheses/braces';
    } else{
        result = 'Syntax analysis successful';
    }
    BracketStack.length = 0;
    mainAvailable = false;

    return result;
}


function Count_Lines(code) {
    var lines = code.split("\n");
    var count = lines.length;
    return count;
}


function Convert_button() {
    var code = document.getElementById("code").value;

    if(code.length>0){

        document.getElementById("output").value = Count_Lines(code) + " Lines of code checked\n\n";


        document.getElementById("output").value +=  /* JSON.stringify(analyzeCode(code)); */ syntaxAnalyze(  analyzeCode(code)  );
    }
    else
    document.getElementById("output").value = "Code block is empty!"

}

function GenerateTokens(){
    var code = document.getElementById("code").value;
    document.getElementById("output").value =  JSON.stringify(analyzeCode(code));
}