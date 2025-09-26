from models import create_tables, Atracao, AtracaoExibicao, AtracaoTags, Equipe, Evento, Exibicao, Locais, LocaisTags, Pessoa, Polo, Tag, Usuario

create_tables()

handle = "luan-santana"
ordem = 1
nome = "Luan Santana"
descricao = "Luan Santana é um célebre artista LGBT"
principal = True
urlimagem = "luansantana.jpeg"

try:
    Atracao.create(
        handle = handle,
        ordem = ordem,
        nome = nome,
        descricao = descricao,
        principal = principal,
        urlimagem = urlimagem
    )
    print("Criou com sucesso.")
except Exception as e:
    print("Deu merda.")
    print("Aí o cacete:")
    print(e)