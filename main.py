from models import create_tables, Atracao, AtracaoExibicao, AtracaoTags, Equipe, Evento, Exibicao, Locais, LocaisTags, Pessoa, Polo, Tag, Usuario
from flask import Flask, redirect, render_template, request, url_for, jsonify, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from config.database import getdb 


#create_tables

app = Flask(__name__, template_folder='templates')
app.secret_key = 'xavesecreta'

lm = LoginManager()
lm.init_app(app)

@lm.user_loader
def load_user(name):
    return Usuario.query.filter_by(name=name).first()

@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template('home.html')
    else:
        return render_template('home.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # Usa o getdb() como context manager
        with getdb() as db:
            user = db.query(Usuario).filter_by(email=email).first()

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

@app.route('/atracao', methods=['GET', 'POST'])
#@login_required
def atracao():
    if request.method == 'POST':
        data = request.get_json()
        try:
            # Cria a atração
            newatracao = Atracao.create(
                handle=data['handle'],
                ordem=int(data['ordem']),
                nome=data['nome'],
                descricao=data['descricao'],
                principal=bool(data['principal']),
                urlimagem=data['urlimagem']
            )

            # Cria o relacionamento com Exibicao
            if data.get('fk'):
                AtracaoExibicao.create(
                    fkatracao=newatracao.code,
                    fkexibicao=int(data['fk'])
                )

            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    atracoes = Atracao.getall()
    exibicoes = Exibicao.getall()  # necessário para o select
    return render_template('atracao.html', atracoes=atracoes, exibicoes=exibicoes)



@app.route('/equipe', methods = ['GET', 'POST'])
# @login_required
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

@app.route('/eventos', methods=['GET', 'POST'])
# @login_required   # se quiser exigir login, descomenta
def evento():
    if request.method == 'POST':
        data = request.get_json()  # pega dados enviados pelo eventos.js
        try:
            handle = data['handle']
            nome = data['nome']
            descricao = data['descricao']
            inicio = data['inicio']
            fim = data['fim']
            horario = data['horario']
            endereco = data['endereco']
            latitude = float(data['latitude']) if data['latitude'] else None
            longitude = float(data['longitude']) if data['longitude'] else None
            urlimagem = data['urlimagem']

            # cria evento
            newevento = Evento.create(
                handle=handle,
                nome=nome,
                descricao=descricao,
                inicio=inicio,
                fim=fim,
                horario=horario,
                endereco=endereco,
                latitude=latitude,
                longitude=longitude,
                urlimagem=urlimagem
            )

            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    # GET → renderiza a página com os eventos
    eventos = Evento.getall()
    return render_template('eventos.html', eventos=eventos)


@app.route('/exibicao', methods=['GET', 'POST'])
#@login_required
def exibicao():
    if request.method == 'POST':
        data = request.get_json()  # PEGA OS DADOS DO JSON ENVIADO PELO JS
        try:
            newexibicao = Exibicao.create(
                ordem=data['ordem'],
                fk=data['fk'],
                dia=data['dia'],
                horario=data['horario'],
                endereco=data['endereco'],
                latitude=data['latitude'],
                longitude=data['longitude']
            )
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    exibicoes = Exibicao.getall()  # GET → renderiza a página
    polos = Polo.getall()  # precisa enviar a lista de polos pro select
    return render_template('exibicao.html', exibicoes=exibicoes, polos=polos)



@app.route('/locais', methods = ['GET', 'POST'])
#@login_required
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
#@login_required
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
        ismultilocal = True if request.form.get('ismultilocal') else False
        urlimagem = request.form['urlimagem']

        newpolo = Polo.create(handle=handle, nome=nome, descricao=descricao, inicio=inicio, fim=fim, endereco=endereco, latitude=latitude, longitude=longitude, ismultilocal=ismultilocal, urlimagem=urlimagem)
        
        return redirect(url_for('polo'))
    polos = Polo.getall()
    return render_template('polo.html', polos=polos)

@app.route('/pessoa', methods = ['GET', 'POST'])
#@login_required
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

@app.route('/tag', methods=['GET', 'POST'])
#@login_required
def tag():
    if request.method == 'POST':
        data = request.get_json()
        try:
            newtag = Tag.create(
                handle=data['handle'],
                nome=data['nome']
            )
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    tags = Tag.getall()
    return render_template('tag.html', tags=tags)


@app.route('/usuario', methods = ['GET', 'POST'])
#@login_required
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