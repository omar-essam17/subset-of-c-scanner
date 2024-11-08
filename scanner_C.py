import re
import tkinter as tk
from tkinter import scrolledtext

c_keywords = {
    "continue", "sizeof", "while", "case", "union", "printf", "unsigned", "if", "switch", "static", "return",
    "for", "default", "do", "struct", "signed", "float", "char", "break", "else", "double", "scanf", "typedef",
    "int", "void", "const"
}


tokens_regex = [
    ('keyword', r'#\s*include\s*<[^>]+>'),
    ('comment', r'//.*|/\*[\s\S]*?\*/'),
    ('character_constant', r"'([^'\\]|\\.)'|\"([^\"\\]|\\.)*\""),
    ('numerical_constant', r'\d+(\.\d*)?([eE][+-]?\d+)?'),
    ('identifier', r'[A-Za-z_]\w*'),
    ('operator', r'&&|\|\||==|!=|<=|>=|<|>|[+\-*/%&|=]'),
    ('special_character', r'[(){},;]'),
    ('whitespace', r'[ \t]+'),
    ('newline', r'\n'),
    ('unknown', r'.'),
]

tok_regex = '|'.join(f"(?P<{name}>{pattern})" for name, pattern in tokens_regex)

def code_tokenization(code):
    tokens = []
    line_num = 1
    for match_obj in re.finditer(tok_regex, code):
        token_type = match_obj.lastgroup
        token_value = match_obj.group()

        if token_type == 'newline':
            line_num += 1
            continue
        elif token_type == 'identifier' and token_value in c_keywords:
            token_type = 'keyword'
        elif token_type == 'whitespace':
            continue
        elif token_type == 'unknown':
            raise RuntimeError(f'Unexpected character {token_value} on line {line_num}')

        tokens.append((token_type, token_value))

    return tokens

def c_code_analysis():
    code_content = code_text.get("1.0", tk.END)
    try:
        tokens = code_tokenization(code_content)
        result_text.delete("1.0", tk.END)
        for token_type, token_value in tokens:
            result_text.insert(tk.END, f"{token_type}: {token_value}\n")
    except RuntimeError as error:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, str(error))

root = tk.Tk()
root.title("Scanner of Sbubest of C")

tk.Label(root, text="enter the code:").pack()
code_text = scrolledtext.ScrolledText(root, width=60, height=12)
code_text.pack()

analyze_button = tk.Button(root, text="scan the code", command=c_code_analysis)
analyze_button.pack()

tk.Label(root, text="Tokens:").pack()
result_text = scrolledtext.ScrolledText(root, width=60, height=17)
result_text.pack()

root.mainloop()
