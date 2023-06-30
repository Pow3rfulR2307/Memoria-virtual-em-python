import os
from random import choice, randint
import math

diretorio = ""
paginas_liberadas = []
index_proximo = -1

relatorio = open("relatorioGeral.txt", "w")

class MemoriaFisica:
    def __init__(self):
        self.memoriaFisica = {}
        self.tamanhoFisica = 250
        self.tamanhoAtual = 0

    def escrever(self, endereco_virtual, endereco_fisico, conteudo, id_bloco):
        self.memoriaFisica[endereco_fisico] = {"conteudo": conteudo, "Id_bloco": id_bloco}
        self.tamanhoAtual += 1

        relatorio.write(f"| Endereco Virtual: {endereco_virtual} | Endereco Fisico: {endereco_fisico} | Tamanho: {len(conteudo)} | id: {id_bloco}\n")

        print(f"| Endereco Virtual: {endereco_virtual} | Endereco Fisico: {endereco_fisico} | Tamanho: {len(conteudo)} | id: {id_bloco}")


class MemoriaVirtual:
    def __init__(self, tamanhoVirtual=100*1024, tamanhoPagina = 4*1024):
        self.tamanhoVirtual = tamanhoVirtual
        self.memoriaFisica = None
        self.tamanhoPagina = tamanhoPagina
        self.swap = "arquivo_swap.bin"


    def criar_memoria_fisica(self, memoria_fisica):
        self.memoriaFisica = memoria_fisica
    
    def encontrar_endereco_fisico_livre(self, offset_pagina, id_bloco):

        global pagina_aleatoria, index_proximo

        if self.memoriaFisica.tamanhoAtual < self.memoriaFisica.tamanhoFisica:
    
            for endereco in range(self.memoriaFisica.tamanhoFisica):

                if endereco not in self.memoriaFisica.memoriaFisica.keys():
                    return (endereco << 12) + offset_pagina
                
        else:
            if len(paginas_liberadas) > index_proximo+1:
                index_proximo+=1
                return paginas_liberadas[index_proximo]
            
            paginas_liberadas.clear()
            index_proximo = -1

            pagina_aleatoria = choice(list(self.memoriaFisica.memoriaFisica.keys()))
            bloco = self.memoriaFisica.memoriaFisica[pagina_aleatoria]["Id_bloco"]

            for i in self.memoriaFisica.memoriaFisica.keys():

                if self.memoriaFisica.memoriaFisica[i]["Id_bloco"] == bloco:
                    
                    mmu_swap_escrever(self.memoriaFisica.memoriaFisica[i]["conteudo"])

                    del self.memoriaFisica.memoriaFisica[i]["conteudo"]

                    paginas_liberadas.append(i)

                    relatorio.write(f"Bloco de id {bloco} da página {i} swap-out para o disco\n")

                    print(f"Bloco de id {bloco} da página {i} swap-out para o disco")


            return pagina_aleatoria #self.memoriaFisica.memoriaFisica[pagina_aleatoria]

    def traduzir_endereco(self, endereco_virtual, tabela_pagina, id_bloco):
        offset_pagina = endereco_virtual & 0xFFF

        if endereco_virtual in tabela_pagina:
            endereco_fisico = tabela_pagina[endereco_virtual]

        else:

            endereco_fisico = self.encontrar_endereco_fisico_livre(offset_pagina, id_bloco)
            tabela_pagina[endereco_virtual] = endereco_fisico

            return endereco_fisico 

    def ler_pagina(self, endereco_virtual, arquivo, tabela_pagina, id_bloco):

        endereco_fisico = self.traduzir_endereco(endereco_virtual, tabela_pagina, id_bloco)

        self.memoriaFisica.escrever(endereco_virtual, endereco_fisico, arquivo, id_bloco)

        return arquivo

def mmu_swap_escrever(conteudo: bytes):
    arquivo_swap = open("arquivo_swap.bin", "ab")
    arquivo_swap.write(conteudo)
    arquivo_swap.close()

if __name__ == "__main__":
    memoria_fisica = MemoriaFisica()

    mmu_tabela_pagina = {}

    paginaVirtual= -1

    id_bloco = 0

    for i in range(20):

        memoria_virtual = MemoriaVirtual()

        memoria_virtual.criar_memoria_fisica(memoria_fisica)

        file_size = randint(60 * 1024, 100 * 1024)  # entre 60KB e 100KB

        binary_file_path = os.path.join(diretorio, f"binary_file_{i}.txt") 

        with open(binary_file_path, "wb") as file:
            file.write(os.urandom(file_size))
        
        id_bloco += 1


        for j in range(math.ceil(os.path.getsize(binary_file_path)/memoria_virtual.tamanhoPagina)):

            with open(binary_file_path, "rb") as f:

                pagina_conteudo = f.read(memoria_virtual.tamanhoPagina)

            paginaVirtual+=1

            pagina = int(bin(paginaVirtual)[2:])

            memoria_virtual.ler_pagina(pagina, pagina_conteudo, mmu_tabela_pagina, id_bloco)

    relatorio.close()