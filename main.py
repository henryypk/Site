from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configuração da SECRET_KEY
app.config['SECRET_KEY'] = 'Emillyzinha'

# Configuração do Banco de Dados
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'doceria.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração para Upload de Arquivos
UPLOAD_FOLDER = os.path.join(basedir, 'static/imagens')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Garante que a pasta exista
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Tipos permitidos
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

db = SQLAlchemy(app)

# Modelo do Produto
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Produto {self.nome}>'

# Criação do Banco de Dados
with app.app_context():
    db.create_all()

# Função para verificar extensão permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Rotas
@app.route('/')
def home():
    produtos = Produto.query.all()
    return render_template('index.html', produtos=produtos)

@app.route('/crud', methods=['GET', 'POST'])
def crud():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        imagem = request.files['imagem']

        # Verifica se um arquivo foi enviado e se é permitido
        if imagem and allowed_file(imagem.filename):
            filename = secure_filename(imagem.filename)  # Evita problemas com o nome do arquivo
            imagem_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagem.save(imagem_path)  # Salva a imagem no caminho seguro

            # Criando e salvando o produto no banco de dados
            novo_produto = Produto(nome=nome, preco=float(preco), imagem=f'static/imagens/{filename}')
            db.session.add(novo_produto)
            db.session.commit()

            return redirect(url_for('crud'))
        else:
            return "Arquivo não permitido. Envie imagens nos formatos: png, jpg, jpeg ou gif.", 400

    # Lista de produtos cadastrados
    produtos = Produto.query.all()
    return render_template('crud.html', produtos=produtos)

if __name__ == '__main__':
    app.run(debug=True)
