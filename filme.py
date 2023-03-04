class Programa:
    def __init__(self, nome, ano):
        self.__nome = nome
        self.ano = ano
        self.__likes = 0

    @property
    def likes(self):
        return self.__likes

    def dar_like(self):
        self.__likes += 1

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, novo_nome):
        self.__nome = novo_nome.title()

    def imprime(self):
        if hasattr(self, "duracao"):
            detalhe = f"{self.duracao} min"
        else:
            detalhe = f"{self.temporadas} temporadas"
        print(f"{self.__nome} - {detalhe}: {self.__likes} likes")


class Filme(Programa):
    def __init__(self, nome, ano, duracao):
        super().__init__(nome, ano)
        self.duracao = duracao


class Serie(Programa):
    def __init__(self, nome, ano, temporadas):
        super().__init__(nome, ano)
        self.temporadas = temporadas


class Playlist:
    def __init__(self, nome, programas):
        self.nome = nome
        self.programas = programas

    def tamanho(self):
        return len(self.tamanho)


vingadores = Filme("vingadores - guerra infinita", 2018, 160)
atlanta = Serie("Atlanta", 2018, 2)
tmep = Filme("Todo mundo em pânico", 1999, 100)
demolidor = Serie("Demolidor", 2016, 2)

vingadores.dar_like()
atlanta.dar_like()
tmep.dar_like()
demolidor.dar_like()
vingadores.dar_like()
atlanta.dar_like()
tmep.dar_like()

filmes_e_series = [vingadores, atlanta, tmep, demolidor]
fim_de_semana = Playlist("fim de semana", filmes_e_series)
for programa in filmes_e_series:
    programa.imprime()
# breakpoint()
print(fim_de_semana)
