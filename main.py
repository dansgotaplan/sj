from models import create_tables, Atracao, AtracaoExibicao, AtracaoTags, Equipe, Evento, Exibicao, Locais, LocaisTags, Pessoa, Polo, Tag, Usuario
from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


create_tables()

app = Flask(__name__, template_folder='view')
app.secret_key = 'xavesecreta'

lm = LoginManager()
lm.init_app(app)

@lm.user_loader
def load_user(name):
    return Usuario.query.filter_by(name=name).first()

@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template('homeauth.html')
    else:
        return render_template('homenotauth.html')
    
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user = Usuario.query.filter_by(email=email).first()
        if user and user.senha == senha:
            login_user(user)
            return redirect(url_for('index'))
        else:
            return 'Falha no login. Verifique suas credenciais.'
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/atracao', methods = ['GET', 'POST'])
@login_required
def atracao():
    if request.method == 'POST':
        handle = request.form['handle']
        ordem = request.form['ordem']
        fk = request.form['fk']
        nome = request.form['nome']
        descricao = request.form['descricao']
        principal = 'principal' in request.form
        urlimagem = request.form['urlimagem']
        
        newatracao = Atracao.create(handle=handle, ordem=ordem, fk=fk, nome=nome, descricao=descricao, principal=principal, urlimagem=urlimagem)
        
        return redirect(url_for('atracao'))
    atracoes = Atracao.getall()
    return render_template('atracao.html', atracoes=atracoes)

@app.route('/equipe', methods = ['GET', 'POST'])
@login_required
def equipe():
    if request.method == 'POST':
        nome = request.form['nome']
        turma = request.form['turma']
        email = request.form['email']
        ano = request.form['ano']
        urlimagem = request.form['urlimagem']

        newequipe = Equipe.create(nome=nome, turma=turma, email=email, ano=ano, urlimagem=urlimagem)
        
        return redirect(url_for('equipe'))
    equipes = Equipe.getall()
    return render_template('equipe.html', equipes=equipes)

@app.route('/evento', methods = ['GET', 'POST'])
@login_required
def evento():
    if request.method == 'POST':
        handle = request.form['handle']
        nome = request.form['nome']
        descricao = request.form['descricao']
        inicio = request.form['inicio']
        fim = request.form0['fim']
        horario = request.form['horario']
        endereco = request.form['endereco']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        urlimagem = request.form['urlimagem']

        newevento = Evento.create(handle=handle, nome=nome, descricao=descricao, inicio=inicio, fim=fim, horario=horario, endereco=endereco, latitude=latitude, longitude=longitude, urlimagem=urlimagem)
        
        return redirect(url_for('evento'))
    eventos = Evento.getall()
    return render_template('evento.html', eventos=eventos)

@app.route('/exibicao', methods = ['GET', 'POST'])
@login_required
def exibicao():
    if request.method == 'POST':
        ordem = request.form['ordem']
        fk = request.form['fk']
        dia = request.form['dia']
        horario = request.form['horario']
        endereco = request.form['endereco']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        urlimagem = request.form['urlimagem']
        
        newexibicao = Exibicao.create(ordem=ordem, fk=fk, dia=dia, horario=horario, endereco=endereco, latitude=latitude, longitude=longitude, urlimagem=urlimagem)
        
        return redirect(url_for('exibicao'))
    exibicoes = Exibicao.getall()
    return render_template('exibicao.html', exibicoes=exibicoes)

@app.route('/locais', methods = ['GET', 'POST'])
@login_required
def locais():
    if request.method == 'POST':
        handle = request.form['handle']
        nome = request.form['nome']
        descricao = request.form['descricao']
        dias = request.form['dias']
        inicio = request.form['inicio']
        fim = request.form['fim']
        endereco = request.form['endereco']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        urlimage = request.form['urlimage']
        urlicone = request.form['urlicone']
        
        newlocal = Locais.create(handle=handle, nome=nome, descricao=descricao, dias=dias, inicio=inicio, fim=fim, endereco=endereco, latitude=latitude, longitude=longitude, urlimage=urlimage, urlicone=urlicone)
        
        return redirect(url_for('locais'))
    locais = Locais.getall()
    return render_template('locais.html', locais=locais)

@app.route('/polo', methods = ['GET', 'POST'])
@login_required
def polo():
    if request.method == 'POST':
        handle = request.form['handle']
        nome = request.form['nome']
        descricao = request.form['descricao']
        inicio = request.form['inicio']
        fim = request.form['fim']
        endereco = request.form['endereco']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        ismultilocal = request.form['ismultilocal']
        urlimagem = request.form['urlimagem']

        newpolo = Polo.create(handle=handle, nome=nome, descricao=descricao, inicio=inicio, fim=fim, endereco=endereco, latitude=latitude, longitude=longitude, ismultilocal=ismultilocal, urlimagem=urlimagem)
        
        return redirect(url_for('polo'))
    polos = Polo.getall()
    return render_template('polo.html', polos=polos)

@app.route('/pessoa', methods = ['GET', 'POST'])
@login_required
def pessoa():
    if request.method == 'POST':
        handle = request.form['handle']
        nome = request.form['nome']
        descricao = request.form['descricao']
        obras = request.form['obras']
        nascido = request.form['nascido']
        morte = request.form['morte'] if request.form['morte'] else None
        ishomenageado = request.form['ishomenageado']
        anohomenagem = request.form['anohomenagem'] if request.form['anohomenagem'] else None
        urlimagem = request.form['urlimagem']

        newpessoa = Pessoa.create(handle=handle, nome=nome, descricao=descricao, obras=obras, nascido=nascido, morte=morte, ishomenageado=ishomenageado, anohomenagem=anohomenagem, urlimagem=urlimagem)
        
        return redirect(url_for('pessoa'))
    pessoas = Pessoa.getall()
    return render_template('pessoa.html', pessoas=pessoas)

@app.route('/tag', methods = ['GET', 'POST'])
@login_required
def tag():
    if request.method == 'POST':
        handle = request.form['handle']
        nome = request.form['nome']

        newtag = Tag.create(handle=handle, nome=nome)
        return redirect(url_for('tag'))
    tags = Tag.getall()
    return render_template('tag.html', tags=tags)

@app.route('/usuario', methods = ['GET', 'POST'])
@login_required
def usuario():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        isadmin = 'isadmin' in request.form
        
        newusuario = Usuario.create(email=email, senha=senha, isadmin=isadmin)
        
        return redirect(url_for('usuario'))
    usuarios = Usuario.getall()
    return render_template('usuario.html', usuarios=usuarios)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)