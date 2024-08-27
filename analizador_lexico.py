import ply.lex as lex
from flask import Flask, render_template, request

app = Flask(__name__)

reserved = {
    'for': 'FOR',
    'while': 'WHILE',
    'if' : 'IF',
    'public' : 'PUBLIC',
    'static' : 'STATIC',
    'void' : 'VOID',
    'numero' : 'NUMERO',
    'puntocoma': 'SEMICOLON',
    'operador' : 'OPERADOR',
    'simbol' : 'SIMBOLO'
}

tokens = ['PABIERTO', 'PCERRADO','LABIERTO','LCERRADO', 'IDENTIFICADOR'] + list(reserved.values())

t_OPERADOR = r'='
t_LCERRADO = r'\}'
t_LABIERTO = r'\{'
t_PABIERTO = r'\('
t_PCERRADO = r'\)'

t_SIMBOLO = r'.'

t_ignore = ' \t\r'

t_NUMERO = r'\d+.\d+'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value) 


def t_IDENTIFICADOR(t):
    r'[A-Za-z]\w*'
    t.type = reserved.get(t.value, 'IDENTIFICADOR')
    return t

def t_error(t): 
    print('Caracter no valido', t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

@app.route('/', methods=['GET', 'POST'])
def index():
    lexer.lineno = 1
    if request.method == 'POST':
        code = request.form.get('code', '')
        lexer.input(code)
 
        tkeys = 0  
        result_lexema = []

        for token in lexer:
            if token.type in reserved.values():
                tkeys += 1  
            result_lexema.append(
                (f"Reservada {token.type.capitalize()}" if token.type in reserved.values() else
                 "IDENTIFICADOR" if token.type == 'IDENTIFICADOR' else
                 "Paréntesis de apertura" if token.type == "PABIERTO" else 
                 "Paréntesis de cierre" if token.type == "PCERRADO" else
                 'Llave de apertura' if token.type == "LABIERTO" else 
                 'Llave de cierre',
                 token.value, token.lineno)
            )
        return render_template('index.html', tokens=result_lexema, tkeys = tkeys, input = code)
    return render_template('index.html', tokens=None)
 
if __name__ == "__main__":
    app.run(debug=True)
