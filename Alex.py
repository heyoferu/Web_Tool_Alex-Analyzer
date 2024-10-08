import ply.lex as lex
import ply.yacc as yacc

class AnalizadorLexico:
    # Tokens reservados
    _reservada = (
        'INCLUDE',
        'IOSTREAM',
        'NAMESPACE',
        'INT',
        'RETURN',
        'COUT',
        'STD',
        'MAIN',
        'USING'
        )
    tokens = _reservada + (
        'ID',
        'L_PAR',
        'R_PAR', 
        'L_BRACKET',
        'R_BRACKET',
        'NUMBER', 
        'STRING', 
        'SEMICOLON', 
        'IN',
        'HASH',
        'LESSTHAN',
        'GREATERTHAN'    
)

    def __init__(self):
        self._resultado_lexema = []
        self.lexer = lex.lex(module=self)
        self.rc = 0

    t_L_PAR = r'\('
    t_R_PAR = r'\)'
    t_L_BRACKET = r'\{'
    t_R_BRACKET = r'\}'
    t_SEMICOLON = r';'
    t_STRING = r'\".*?\"'
    t_ID = r'[a-zA-Z_][a-zA-Z_0-9]*'
    t_NUMBER = r'\d+'
    t_HASH = r'\#'
    t_LESSTHAN = r'\<'
    t_GREATERTHAN = r'\>'
    t_IN = r'\<\<'


    def t_INCLUDE(self, t):
        r'include'
        return t
    

    def t_IOSTREAM(self, t):
        r'iostream'
        return t
    
    def t_NAMESPACE(self, t):
        r'namespace'
        return t
    
    def t_RETURN(self, t):
        r'return'
        return t
    
    def t_COUT(self, t):
        r'cout'
        return t

    def t_STD(self, t):
        r'std'
        return t

    def t_MAIN(self, t):
        r'main'
        return t

    def t_INT(self, t):
        r'\bint\b'
        return t

    def t_USING(self, t):
        r'using'
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
                self.rc += 1

            if tok.type != 'ID' and tok.type not in self._reservada:
                self._resultado_lexema.append((tok.value, "", "", tok.type, tok.lineno))
                self.rc += 1

        
        return self._resultado_lexema


class AnalizadorSintactico:
    def __init__(self, analizador_lexico):
        self.analizador_lexico = analizador_lexico
        self.resultado_lexema = None
        self.tokens = analizador_lexico.tokens 
        self.parser = yacc.yacc(module=self)
        self.errormsg = []
        self.__vars = []
        self.resultado_lexema_c = 0

    def p_statement(self, p):
        '''statement : imports ns INT MAIN L_PAR R_PAR L_BRACKET code R_BRACKET'''

    def p_statement_error(self, p):
        '''statement : imports error INT MAIN L_PAR R_PAR L_BRACKET code R_BRACKET'''
        self.errormsg.append("Error en el namespace.")

    def p_statement_error_2(self, p):
        '''statement : error ns INT MAIN L_PAR R_PAR L_BRACKET code R_BRACKET'''
        self.errormsg.append("Error en la importación.")

    def p_statement_error_3(self, p):
        '''statement : imports ns INT MAIN L_PAR R_PAR L_BRACKET error R_BRACKET'''
        self.errormsg.append("Expresiones de código no válidas.")

    def p_imports(self, p):
        '''imports : HASH INCLUDE LESSTHAN IOSTREAM GREATERTHAN'''

    def p_ns(self, p):
        '''ns : USING NAMESPACE STD SEMICOLON'''
    
    def p_code(self, p):
        '''code : COUT IN STRING SEMICOLON
                | RETURN NUMBER SEMICOLON
                | code code'''
    
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




""""
#include <iostream>
using namespace std;
int main() {
    cout << "Hello, World!";
    return 0;
}

"""