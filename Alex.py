import ply.lex as lex
import ply.yacc as yacc

class AnalizadorLexico:
    # Tokens reservados
    _reservada = ('IF', 'ELSE', 'WHILE', 'FOR', 'PRINT',
                  'RETURN', 'BREAK', 'TRUE', 'FALSE', 'INT')
    tokens = _reservada + ('identificador', 'suma', 'PARIZQ', 'PARDER', 'LLAVEIZQ',
                            'LLAVEDER','numero', 'punto','cadena', 'pcoma', 'igual', 'lessthan')

    def __init__(self):
        self._resultado_lexema = []
        self.lexer = lex.lex(module=self)
        self.rc = 0

    t_PARIZQ = r'\('
    t_PARDER = r'\)'
    t_LLAVEIZQ = r'\{'
    t_LLAVEDER = r'\}'
    t_punto = r'\.'
    t_suma = r'\+'
    t_igual = r'='
    t_lessthan = r'<='
    t_pcoma = r';'
    t_cadena = r'\".*?\"'
    t_identificador = r'[a-zA-Z_][a-zA-Z_0-9]*'
    t_numero = r'\d+'


    def t_IF(self, t):
        r'if'
        return t

    def t_ELSE(self, t):
        r'else'
        return t

    def t_WHILE(self, t):
        r'while'
        return t

    def t_FOR(self, t):
        r'\bfor\b'
        return t

    def t_INT(self, t):
        r'\bint\b'
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        # self._resultado_lexema.append((f"Token no Valido",t.value, t.lineno))
        t.lexer.skip(1)

    t_ignore = ' \t'

    def analizar(self, data):
        self._resultado_lexema.clear()  # Limpiar resultados 
        analizador = lex.lex(module=self)
        analizador.input(data)
        
        while True:
            tok = analizador.token()
            print(tok)
            if not tok:
                break
            if tok.type in self._reservada:
                self._resultado_lexema.append((f"Reservada {tok.type.capitalize()}", tok.value, tok.lineno))
                self.rc += 1
            else:
                self._resultado_lexema.append((f"{tok.type.capitalize()}", tok.value, tok.lineno))
        
        return self._resultado_lexema


class AnalizadorSintactico:
    def __init__(self, analizador_lexico):
        self.analizador_lexico = analizador_lexico
        self.tokens = analizador_lexico.tokens 
        self.parser = yacc.yacc(module=self)
        self.resultado = []

    def p_inicio(self, p):
        '''inicio : estructura_for'''
        print("Analisis exitoso del for")
    
    def p_estructura_for(self, p):
        '''estructura_for : FOR PARIZQ declaracion_inicial pcoma condicion pcoma actualizacion PARDER bloque'''

    def p_declaracion_inicial(self, p):
        '''declaracion_inicial : tipo identificador igual numero'''
        p[0] = ("Declaración inicial", p[2], p[4])

    
    def p_tipo(self, p):
        '''tipo : INT'''
    
    def p_condicion(self, p):
        '''condicion : identificador lessthan numero'''
        p[0] = ("Condición", p[1], p[3])

    def p_actualizacion(self, p):
        '''actualizacion : identificador suma suma'''
        p[0] = ("Actualización", p[1])

    def p_bloque(self, p):
        '''bloque : LLAVEIZQ instruccion LLAVEDER'''
        p[0] = "Bloque de código"
    
    def p_instruccion(self, p):
        '''instruccion : identificador punto identificador punto identificador PARIZQ cadena suma identificador PARDER pcoma'''
        p[0] = "Instrucción de impresión"

    def p_error(self, p):
        if p:
            self.resultado = f"Error de sintaxis en '{p.value}' en la línea {p.lineno}"
            
        else:
            print("Error de sintaxis en la entrada")

    def analizar(self, data):
        self.parser.parse(data, lexer=self.analizador_lexico.lexer)
        return self.resultado
