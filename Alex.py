import ply.lex as lex
import ply.yacc as yacc

class AnalizadorLexico:
    # Tokens reservados
    _reservada = (
        'FOR',
        'INT',
        'SYSTEM',
        'OUT',
        'PRINTLN',
        'PROGRAMA',
        'READ',
        'PRINTF',
        'END'
        )
    tokens = _reservada + (
        'ID', 
        'PLUS',
        'L_PAR',
        'R_PAR', 
        'L_BRACKET',
        'R_BRACKET',
        'NUMBER', 
        'DOT',
        'STRING', 
        'SEMICOLON', 
        'ASSIGN', 
        'LESSTHAN',
        'COMMA'
    )

    def __init__(self):
        self._resultado_lexema = []
        self.lexer = lex.lex(module=self)
        self.rc = 0

    t_L_PAR = r'\('
    t_R_PAR = r'\)'
    t_L_BRACKET = r'\{'
    t_R_BRACKET = r'\}'
    t_DOT = r'\.'
    t_PLUS = r'\+'
    t_ASSIGN = r'='
    t_LESSTHAN = r'<='
    t_SEMICOLON = r';'
    t_STRING = r'\".*?\"'
    t_ID = r'[a-zA-Z_][a-zA-Z_0-9]*'
    t_NUMBER = r'\d+'
    t_COMMA = r'\,'

    def t_FOR(self, t):
        r'for'
        return t

    def t_SYSTEM(self, t):
        r'\bSystem\b'
        return t

    def t_OUT(self, t):
        r'\bout\b'
        return t

    def t_PRINTLN(self, t):
        r'\bprintln\b'
        return t

    def t_INT(self, t):
        r'\bint\b'
        return t

    def t_PROGRAMA(self, t):
        r'\bprograma\b'
        return t

    def t_READ(self, t):
        r'\bread\b'
        return t

    def t_PRINTF(self, t):
        r'\bprintf\b'
        return t

    def t_END(self, t):
        r'\bend\b'
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        t.lexer.skip(1)

    t_ignore = '\r\t'

    def analizar(self, data):
        self._resultado_lexema.clear()  # Limpiar resultados 
        analizador = lex.lex(module=self)
        analizador.input(data)
        
        while True:
            tok = analizador.token()
            if not tok:
                break

            if tok.type in self._reservada:
                self._resultado_lexema.append((tok.value, "X", "", tok.type, tok.lineno))
                self.rc += 1

            if tok.type == 'ID':
                self._resultado_lexema.append((tok.value, "", "x", tok.type, tok.lineno))

            if tok.type != 'ID' and tok.type not in self._reservada:
                self._resultado_lexema.append((tok.value, "", "", tok.type, tok.lineno))
        
        return self._resultado_lexema


class AnalizadorSintactico:
    def __init__(self, analizador_lexico):
        self.analizador_lexico = analizador_lexico
        self.resultado_lexema = None
        self.tokens = analizador_lexico.tokens 
        self.parser = yacc.yacc(module=self)
        self.errormsg = []
        self.resultado_lexema_c = 0

    ### program grammar
    ### program statement
    ### programa def() {code}
    def p_programa_statement(self, p):
        '''programa : PROGRAMA def L_PAR R_PAR L_BRACKET code R_BRACKET'''
    
    ### producción def : acepta 'suma', o cualquier otro identificador
    def p_def(self, p):
        '''def : ID '''

    ### producción code : acepta una producción de expr 
    def p_code(self, p):
        '''code : expr'''

    ### producción expr : acepta cualquier expresión de las siguienes:
    #### 1. int a, b, c, ... z ó sólo un identificador
    #### 2. read a; ó cualquier otro identificador
    #### 3. a = b+c
    #### 4. print("")
    #### 5: end
    #### La ultima producción es recursiva, se llama así misma en caso de que sean uno o más expresiones
    def p_expr(self, p):
        '''expr : INT ids SEMICOLON
                | READ ID SEMICOLON 
                | op
                | PRINTF L_PAR STRING R_PAR
                | END SEMICOLON
                | expr expr'''

    ### producción op : acepta la sintaxis id = id + id; ejemplo c=a+b;
    def p_op(self, p):
        '''op : ID ASSIGN ID PLUS ID SEMICOLON'''

    ### producción ids: acepta multiples identificadores separados por comas, es decir i, i, i o sólo i
    def p_ids(self, p):
        '''ids : ID 
               | ids COMMA ids'''    ### recursividad
               
    def p_error(self, p):
        if p:
            self.errormsg.append(f"Error en la linea {p.lineno} y posición {p.lexpos}. Carácter no valido: {p.value}")
        else:
            self.errormsg.append("Error de sintaxis en la entrada")
        
    def analizar(self, data):
        self.parser.parse(data, lexer=self.analizador_lexico.lexer)
        self.resultado_lexema = self.analizador_lexico.analizar(data)
        self.resultado_lexema_c = self.analizador_lexico.rc
        return self.errormsg 
