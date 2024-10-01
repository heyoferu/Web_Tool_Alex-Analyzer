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
        'LESSTHAN'
    )

    def __init__(self):
        self._resultado_lexema = []
        self.lexer = lex.lex(module=self)

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
                self._resultado_lexema.append((tok.value, "X", ""))

            if tok.type == 'ID':
                self._resultado_lexema.append((tok.value, "", "x"))

            else:
                self._resultado_lexema.append((tok.value, "", ""))
        
        return self._resultado_lexema


class AnalizadorSintactico:
    def __init__(self, analizador_lexico):
        self.analizador_lexico = analizador_lexico
        self.resultado_lexema = None
        self.tokens = analizador_lexico.tokens 
        self.parser = yacc.yacc(module=self)
        self.errormsg = []


    ### statement_for
    def p_statement_for(self, p):
        '''statement_for : FOR expr codeblock'''
    
    def p_statement_for_error(self, p):
        '''statement_for : FOR error codeblock'''
        self.errormsg.append("Error de sintaxis en la declaración 'for'. Se esperaba una expresión válida.")

    ### (expr)
    def p_expr(self, p):
        '''expr : L_PAR var_init SEMICOLON var_upto SEMICOLON inc R_PAR'''

    def p_expr_assign_error(self, p):
        '''expr : L_PAR error SEMICOLON var_upto SEMICOLON inc R_PAR'''
        self.errormsg.append("Error de sintaxis en la expresión del bucle 'for'. Se esperaba una inicialización válida.")

    def p_expr_a_error(self, p):
        '''expr : L_PAR var_init SEMICOLON error SEMICOLON inc R_PAR'''
        self.errormsg.append("Error de sintaxis en la condición del bucle 'for'. Se esperaba una condición válida.")
        
    ### int i = 1
    def p_var_init(self, p):
        '''var_init : INT ID ASSIGN NUMBER'''

    def p_var_init_error(self, p):
        '''var_init : INT error ASSIGN NUMBER'''
        self.errormsg.append("Error de sintaxis en la inicialización de la variable. Se esperaba un identificador válido.")

    ### i <= 10
    def p_var_upto(self, p):
        '''var_upto : ID LESSTHAN NUMBER'''

    def p_var_upto_error(self, p):
        '''var_upto : ID error NUMBER'''
        self.errormsg.append("Error de sintaxis en la condición del bucle 'for'. Se esperaba un operador de comparación válido.")

    ### i++
    def p_inc(self, p):
        '''inc : ID PLUS PLUS'''

    def p_inc_error(self, p):
        '''inc : ID error'''
        self.errormsg.append("Error de sintaxis en la expresión de incremento. Se esperaba '++' o un incremento válido.")

    ### {code}
    def p_codeblock(self, p):
        '''codeblock : L_BRACKET code R_BRACKET'''

    def p_codeblock_error(self, p):
        '''codeblock : L_BRACKET error R_BRACKET'''
        self.errormsg.append("Error de sintaxis en el bloque de código.")

    ### System.Out.Println("cadena")
    def p_code(self, p):
        '''code : SYSTEM DOT OUT DOT PRINTLN L_PAR args R_PAR SEMICOLON'''

    def p_code_error(self, p):
        '''code : SYSTEM DOT OUT DOT PRINTLN L_PAR error R_PAR SEMICOLON'''
        self.errormsg.append("Error de sintaxis en la declaración 'System.out.println'. Se esperaba argumentos válidos.")

    def p_args(self, p):
        '''args : STRING PLUS ID'''

    def p_args_error(self, p):
        '''args : STRING error ID'''
        self.errormsg.append("Error de sintaxis en los argumentos. Se esperaba un argumento válido.")

    def p_error(self, p):
        if p:
            self.errormsg.append(f"Error en la linea {p.lineno} y posición {p.lexpos}. Carácter no valido: {p.value}")
        else:
            self.errormsg.append("Error de sintaxis en la entrada")
        
    def analizar(self, data):
        self.parser.parse(data, lexer=self.analizador_lexico.lexer)
        self.resultado_lexema = self.analizador_lexico.analizar(data)
        return self.errormsg 
