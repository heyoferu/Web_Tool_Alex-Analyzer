from flask import Flask, render_template, request
import Alex

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form.get('code', '')

        analizador = Alex.AnalizadorLexico()
        
        resultado = analizador.analizar(code)

        asena = Alex.AnalizadorSintactico(analizador)
        sintaxis = asena.analizar(code)

        return render_template('index.html', tokens=resultado, tkeys=analizador.rc, input=code, error_sena = sintaxis)
    
    return render_template('index.html', tokens=None, error_sena = None)


if __name__ == "__main__":
    app.run(debug=True)
