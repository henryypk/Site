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

# Modelo do Produto com a coluna categoria
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)  # Coluna categoria

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
    produtos = Produto.query.all()  # Obtemos todos os produtos cadastrados
    return render_template('index.html', produtos=produtos)

@app.route('/crud', methods=['GET', 'POST'])
def crud():
    if request.method == 'POST':
        # Recebe os dados do formulário
        produto_id = request.form.get('id')  # Verifica se existe um ID no formulário
        nome = request.form['nome']
        preco = request.form['preco']
        imagem = request.files['imagem']
        categoria = request.form['categoria']  # Captura a categoria selecionada

        if produto_id:  # Se existir um ID, é uma edição
            produto = Produto.query.get_or_404(produto_id)
            produto.nome = nome
            produto.preco = float(preco)
            produto.categoria = categoria  # Atualiza a categoria

            if imagem and allowed_file(imagem.filename):
                filename = secure_filename(imagem.filename)
                imagem_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                imagem.save(imagem_path)
                produto.imagem = f'static/imagens/{filename}'

            db.session.commit()  # Commit para salvar as alterações
        else:  # Caso contrário, é criação de novo produto
            if imagem and allowed_file(imagem.filename):
                filename = secure_filename(imagem.filename)
                imagem_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                imagem.save(imagem_path)
                novo_produto = Produto(nome=nome, preco=float(preco), imagem=f'static/imagens/{filename}', categoria=categoria)  # Adiciona categoria
                db.session.add(novo_produto)
                db.session.commit()

        return redirect(url_for('crud'))  # Redireciona para a página de CRUD
    
    # Caso GET, renderiza a página com a lista de produtos
    produto_editar = None  # Inicializa a variável para produto editar
    produto_id = request.args.get('editar')  # Pega o parâmetro editar da URL
    
    if produto_id:  # Se houver um ID, busca o produto para editar
        produto_editar = Produto.query.get(produto_id)
    
    produtos = Produto.query.all()  # Obtém a lista de produtos
    return render_template('crud.html', produtos=produtos, produto_editar=produto_editar)

@app.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    produto = Produto.query.get_or_404(id)  # Busca o produto ou retorna 404 se não existir
    db.session.delete(produto)  # Remove o produto do banco de dados
    db.session.commit()  # Salva as alterações
    return redirect(url_for('crud'))  # Redireciona para a página de CRUD

if __name__ == '__main__':
    app.run(debug=True)
