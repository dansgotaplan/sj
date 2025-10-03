from models import create_tables, Atracao, AtracaoExibicao, AtracaoTags, Equipe, Evento, Exibicao, Locais, LocaisTags, Pessoa, Polo, Tag, Usuario
from flask import Flask, redirect, render_template, request, url_for, jsonify, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from config.database import getdb 
from sqlalchemy.orm import joinedload


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
            # Abrindo sessão manualmente
            with getdb() as session:
                # Cria a atração
                newatracao = Atracao(
                    handle=data['handle'],
                    ordem=int(data['ordem']),
                    nome=data['nome'],
                    descricao=data['descricao'],
                    principal=bool(data['principal']),
                    urlimagem=data['urlimagem']
                )
                session.add(newatracao)
                session.flush()  # Gera o code sem commitar ainda

                # Relacionamento com Exibicao
                if data.get('fk'):
                    session.add(AtracaoExibicao(
                        fkatracao=newatracao.code,
                        fkexibicao=int(data['fk'])
                    ))

                # Relacionamento com Tags
                if data.get('tags'):
                    for tag_code in data['tags']:
                        session.add(AtracaoTags(
                            fkatracao=newatracao.code,
                            fktag=int(tag_code)
                        ))

                session.commit()  # Salva tudo junto

            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    atracoes = Atracao.getall_with_rel()
    exibicoes = Exibicao.getall_dict()
    tags = Tag.getall_dict()
    return render_template('atracao.html', atracoes=atracoes, exibicoes=exibicoes, tags=tags)

@app.route('/atracao/excluir/<int:atracao_id>', methods=['GET'])
#@login_required
def excluir_atracao(atracao_id):
    with getdb() as db:
        atracao = db.query(Atracao).get(atracao_id)
        if not atracao:
            return "Atração não encontrada", 404

        # Remove vínculos com Exibições e Tags
        atracao.exibicoes = []
        atracao.tags = []

        # Exclui a atração
        db.delete(atracao)
        db.commit()

    return redirect(url_for('atracao'))


@app.route('/equipe', methods = ['GET', 'POST'])
def equipe():
    if request.method == 'POST':
        nome = request.form['nome']
        turma = request.form['turma']
        email = request.form['email']
        funcao = request.form['funcao']  # capturando função
        ano = request.form['ano']
        urlimagem = request.form['urlimagem']

        newequipe = Equipe.create(
            nome=nome,
            turma=turma,
            email=email,
            funcao=funcao, 
            ano=ano,
            urlimagem=urlimagem
        )
        
        return redirect(url_for('equipe'))

    equipes = Equipe.getall_dict()
    return render_template('equipe.html', equipes=equipes)

@app.route('/equipe/excluir/<int:equipe_id>', methods=['GET'])
#@login_required
def excluir_equipe(equipe_id):
    with getdb() as db:
        integrante = db.query(Equipe).get(equipe_id)
        if not integrante:
            return "Integrante não encontrado", 404

        db.delete(integrante)
        db.commit()
    return redirect(url_for('equipe'))

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
            Evento.create(
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
    eventos = Evento.getall_dict()
    return render_template('eventos.html', eventos=eventos)

@app.route('/eventos/excluir/<int:evento_id>', methods=['GET'])
#@login_required
def excluir_evento(evento_id):
    with getdb() as db:
        evento = db.query(Evento).get(evento_id)
        if not evento:
            return "Evento não encontrado", 404

        db.delete(evento)
        db.commit()
    return redirect(url_for('evento'))



@app.route('/exibicao', methods=['GET', 'POST'])
def exibicao():
    if request.method == 'POST':
        data = request.get_json()
        try:
            Exibicao.create(
                ordem=int(data['ordem']),
                fk=int(data['fk']),
                dia=data['dia'],
                horario=data['horario'],
                endereco=data['endereco'],
                latitude=float(data['latitude']),
                longitude=float(data['longitude'])
            )
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    # GET → pega exibicoes e polos como dicionários já com polo carregado
    exibicoes = Exibicao.getall_with_rel()
    polos = Polo.getall_dict()

    return render_template('exibicao.html', exibicoes=exibicoes, polos=polos)

@app.route('/exibicao/excluir/<int:exibicao_id>', methods=['GET'])
#@login_required
def excluir_exibicao(exibicao_id):
    with getdb() as db:
        exibicao = db.query(Exibicao).get(exibicao_id)
        if not exibicao:
            return "Exibição não encontrada", 404

        # opcional: verificar vínculos com atrações
        if exibicao.atracoes:
            return "Não é possível excluir uma exibição vinculada a atrações.", 400

        db.delete(exibicao)
        db.commit()
    return redirect(url_for('exibicao'))



@app.route('/locais', methods=['GET', 'POST'])
def locais():
    if request.method == 'POST':
        data = request.get_json()
        try:
            with getdb() as session:
                newlocal = Locais(
                    handle=data['handle'],
                    nome=data['nome'],
                    descricao=data['descricao'],
                    dias=data['dias'],
                    inicio=data['inicio'],
                    fim=data['fim'],
                    endereco=data['endereco'],
                    latitude=float(data['latitude']),
                    longitude=float(data['longitude']),
                    urlimage=data['urlimage'],
                    urlicone=data['urlicone']
                )
                session.add(newlocal)
                session.flush()

                if data.get('tags'):
                    for tag_code in data['tags']:
                        session.add(LocaisTags(
                            fklocal=newlocal.code,
                            fktag=int(tag_code)
                        ))
                session.commit()
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    locais = Locais.getall_with_rel()
    tags = Tag.getall_dict()
    return render_template('locais.html', locais=locais, tags=tags)

@app.route('/locais/excluir/<int:local_id>', methods=['GET'])
#@login_required
def excluir_local(local_id):
    with getdb() as db:
        local = db.query(Locais).get(local_id)
        if not local:
            return "Local não encontrado", 404

        # Remove apenas os vínculos com tags (não exclui as tags)
        local.tags = []

        # Exclui o local
        db.delete(local)
        db.commit()

    return redirect(url_for('locais'))


@app.route('/polo', methods=['GET', 'POST'])
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

        Polo.create(
            handle=handle,
            nome=nome,
            descricao=descricao,
            inicio=inicio,
            fim=fim,
            endereco=endereco,
            latitude=latitude,
            longitude=longitude,
            ismultilocal=ismultilocal,
            urlimagem=urlimagem
        )
        
        return redirect(url_for('polo'))

    polos = Polo.getall_dict()
    return render_template('polo.html', polos=polos)

# Excluir Polo
@app.route('/polo/excluir/<int:polo_id>', methods=['GET'])
#@login_required
def excluir_polo(polo_id):
    with getdb() as db:
        polo = db.query(Polo).get(polo_id)
        if not polo:
            return "Polo não encontrado", 404
        db.delete(polo)
        db.commit()
    return redirect(url_for('polo'))



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

    tags = Tag.getall_dict()
    return render_template('tag.html', tags=tags)

@app.route('/tag/excluir/<int:tag_id>', methods=['GET'])
#@login_required
def excluir_tag(tag_id):
    with getdb() as db:
        tag = db.query(Tag).get(tag_id)
        if not tag:
            return "Tag não encontrada", 404

        # verifica vinculo com locais ou atrações
        if tag.locais or tag.atracoes:
            return "Não é possível excluir uma tag vinculada a locais ou atrações.", 400

        db.delete(tag)
        db.commit()
    return redirect(url_for('tag'))



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