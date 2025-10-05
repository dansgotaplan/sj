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
    with getdb() as session:
        total_atracoes = session.query(Atracao).count()
        total_equipes = session.query(Equipe).count()
        total_eventos = session.query(Evento).count()
        total_exibicoes = session.query(Exibicao).count()
        total_locais = session.query(Locais).count()
        total_polos = session.query(Polo).count()
        total_tags = session.query(Tag).count()

    return render_template(
        "home.html",
        total_atracoes=total_atracoes,
        total_equipes=total_equipes,
        total_eventos=total_eventos,
        total_exibicoes=total_exibicoes,
        total_locais=total_locais,
        total_polos=total_polos,
        total_tags=total_tags,
    )
    
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

@app.route("/atracao/<int:atracao_id>", methods=["PUT"])
def editar_atracao(atracao_id):
    data = request.get_json()
    try:
        with getdb() as db:
            # usa session.get que é o padrão nas versões 1.4+
            atracao = db.get(Atracao, atracao_id)
            if not atracao:
                return jsonify({"success": False, "error": "Atração não encontrada."}), 404

            atracao.handle = data.get("handle")
            atracao.nome = data.get("nome")
            atracao.ordem = data.get("ordem")
            atracao.descricao = data.get("descricao")
            atracao.urlimagem = data.get("urlimagem")
            atracao.principal = data.get("principal")

            # Atualizar relações: limpa e recria
            atracao.tags.clear()
            atracao.exibicoes.clear()

            if data.get("fk"):
                exibicao = db.get(Exibicao, int(data["fk"]))
                if exibicao:
                    atracao.exibicoes.append(exibicao)

            if data.get("tags"):
                for tag_id in data["tags"]:
                    tag = db.get(Tag, int(tag_id))
                    if tag:
                        atracao.tags.append(tag)

            db.commit()
        return jsonify({"success": True})
    except Exception as e:
        # se der erro tenta rollback (se session ainda aberta)
        try:
            db.rollback()
        except:
            pass
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/equipe', methods=['GET', 'POST'])
def equipe():
    if request.method == 'POST':
        data = request.get_json()  # 👈 pega JSON enviado pelo fetch
        try:
            Equipe.create(
                nome=data['nome'],
                turma=data['turma'],
                email=data['email'],
                funcao=data.get('funcao'),
                ano=data['ano'],
                urlimagem=data.get('urlimagem')
            )
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    equipes = Equipe.getall_dict()
    return render_template('equipe.html', equipes=equipes)

@app.route('/equipe/excluir/<int:equipe_id>', methods=['GET'])
def excluir_equipe(equipe_id):
    with getdb() as db:
        integrante = db.query(Equipe).get(equipe_id)
        if not integrante:
            return "Integrante não encontrado", 404
        db.delete(integrante)
        db.commit()
    return redirect(url_for('equipe'))

@app.route('/equipe/editar/<int:equipe_id>', methods=['PUT'])
def editar_equipe(equipe_id):
    data = request.get_json()
    with getdb() as db:
        integrante = db.query(Equipe).get(equipe_id)
        if not integrante:
            return jsonify({"success": False, "error": "Integrante não encontrado"}), 404

        integrante.nome = data['nome']
        integrante.turma = data['turma']
        integrante.email = data['email']
        integrante.funcao = data['funcao']
        integrante.ano = data['ano']
        integrante.urlimagem = data['urlimagem']

        db.commit()
    return jsonify({"success": True})


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

@app.route('/eventos/<int:evento_id>', methods=['PUT'])
def editar_evento(evento_id):
    data = request.get_json()
    try:
        with getdb() as db:
            evento = db.query(Evento).get(evento_id)
            if not evento:
                return jsonify({"success": False, "error": "Evento não encontrado"}), 404

            evento.handle = data['handle']
            evento.nome = data['nome']
            evento.descricao = data['descricao']
            evento.inicio = data['inicio']
            evento.fim = data['fim']
            evento.horario = data['horario']
            evento.endereco = data['endereco']
            evento.latitude = float(data['latitude'])
            evento.longitude = float(data['longitude'])
            evento.urlimagem = data['urlimagem']

            db.commit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


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

@app.route('/exibicao/<int:exibicao_id>', methods=['GET', 'PUT'])
def gerenciar_exibicao(exibicao_id):
    with getdb() as db:
        exibicao = db.query(Exibicao).get(exibicao_id)
        if not exibicao:
            return jsonify({"success": False, "error": "Exibição não encontrada"}), 404

        if request.method == 'GET':
            return jsonify({
                "ordem": exibicao.ordem,
                "fk": exibicao.fk,
                "dia": str(exibicao.dia),
                "horario": str(exibicao.horario),
                "endereco": exibicao.endereco,
                "latitude": float(exibicao.latitude),
                "longitude": float(exibicao.longitude)
            })

        elif request.method == 'PUT':
            data = request.get_json()
            try:
                exibicao.ordem = int(data['ordem'])
                exibicao.fk = int(data['fk'])
                exibicao.dia = data['dia']
                exibicao.horario = data['horario']
                exibicao.endereco = data['endereco']
                exibicao.latitude = float(data['latitude'])
                exibicao.longitude = float(data['longitude'])
                db.commit()
                return jsonify({"success": True})
            except Exception as e:
                return jsonify({"success": False, "error": str(e)}), 400

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

@app.route("/locais/<int:local_id>", methods=["PUT"])
def editar_local(local_id):
    dados = request.get_json()
    if not dados:
        return jsonify({"success": False, "error": "Dados não enviados"}), 400

    try:
        with getdb() as session:
            local = session.query(Locais).filter_by(code=local_id).first()
            if not local:
                return jsonify({"success": False, "error": "Local não encontrado"}), 404

            # Atualiza campos
            local.handle = dados.get("handle", local.handle)
            local.nome = dados.get("nome", local.nome)
            local.descricao = dados.get("descricao", local.descricao)
            local.dias = dados.get("dias", local.dias)
            local.inicio = dados.get("inicio", local.inicio)
            local.fim = dados.get("fim", local.fim)
            local.endereco = dados.get("endereco", local.endereco)
            local.latitude = dados.get("latitude", local.latitude)
            local.longitude = dados.get("longitude", local.longitude)
            local.urlimage = dados.get("urlimage", local.urlimage)
            local.urlicone = dados.get("urlicone", local.urlicone)

            # Atualiza tags
            if "tags" in dados:
                local.tags.clear()
                for tag_id in dados["tags"]:
                    tag = session.query(Tag).filter_by(code=tag_id).first()
                    if tag:
                        local.tags.append(tag)

            session.commit()
            return jsonify({"success": True, "message": "Local atualizado com sucesso"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/polo', methods=['GET', 'POST'])
def polo():
    if request.method == 'POST':
        data = request.get_json()  # <- pega JSON do JS
        try:
            # Converte valores numéricos
            latitude = float(data['latitude']) if data.get('latitude') else None
            longitude = float(data['longitude']) if data.get('longitude') else None
            ismultilocal = bool(data.get('ismultilocal', False))

            Polo.create(
                handle=data['handle'],
                nome=data['nome'],
                descricao=data['descricao'],
                inicio=data['inicio'],
                fim=data['fim'],
                endereco=data['endereco'] if not ismultilocal else None,
                latitude=latitude if not ismultilocal else None,
                longitude=longitude if not ismultilocal else None,
                ismultilocal=ismultilocal,
                urlimagem=data['urlimagem']
            )
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

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

@app.route('/polo/<int:polo_id>', methods=['PUT'])
def editar_polo(polo_id):
    data = request.get_json()
    try:
        with getdb() as db:
            polo = db.query(Polo).get(polo_id)
            if not polo:
                return jsonify({"success": False, "error": "Polo não encontrado"}), 404

            polo.handle = data['handle']
            polo.nome = data['nome']
            polo.descricao = data['descricao']
            polo.inicio = data['inicio']
            polo.fim = data['fim']
            polo.endereco = data['endereco']
            polo.latitude = data['latitude']
            polo.longitude = data['longitude']
            polo.urlimagem = data['urlimagem']
            polo.ismultilocal = data['ismultilocal']

            db.commit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


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


@app.route('/tag/<int:tag_id>', methods=['PUT'])
def editar_tag(tag_id):
    data = request.get_json()
    try:
        with getdb() as db:
            tag = db.query(Tag).get(tag_id)
            if not tag:
                return jsonify({"success": False, "error": "Tag não encontrada"}), 404

            tag.handle = data['handle']
            tag.nome = data['nome']
            db.commit()

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/tag/excluir/<int:tag_id>', methods=['GET'])
def excluir_tag(tag_id):
    with getdb() as db:
        tag = db.query(Tag).get(tag_id)
        if not tag:
            return "Tag não encontrada", 404

        # verifica vínculo com locais ou atrações
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