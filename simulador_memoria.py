###
###     S I M U L A D O R    D E    M E M Ó R I A
###
### Prof. Filipo - github.com/ProfessorFilipo/MemSim/
###

import sys


class Frame:
    def __init__(self, id_frame):
        self.id_frame = id_frame
        self.pagina_alocada = None  # Armazena o número da página ou None se estiver vazio
        # Dica para os alunos: vocês podem adicionar atributos aqui para ajudar no algoritmo (ex: timestamp, contador)


class TabelaPaginas:
    def __init__(self, num_frames):
        # Inicializa a memória física com a quantidade de frames especificada
        self.frames = [Frame(i) for i in range(num_frames)]
        self.total_page_faults = 0
        self.total_acessos = 0

    def acessar_pagina(self, numero_pagina):
        self.total_acessos += 1

        # 1. Verificar se a página já está em algum frame (Hit)
        for frame in self.frames:
            if frame.pagina_alocada == numero_pagina:
                # TODO: Se necessário para o algoritmo (ex: LRU), atualize metadados aqui.
                return True, frame.id_frame  # Retorna (Hit=True, frame_id)

        # 2. Se não encontrou, ocorreu um Page Fault!
        self.total_page_faults += 1

        # 3. Verificar se existe algum frame vazio disponível
        for frame in self.frames:
            if frame.pagina_alocada is None:
                frame.pagina_alocada = numero_pagina
                # TODO: Se necessário para o algoritmo, inicialize metadados do frame aqui.
                return False, frame.id_frame  # Retorna (Hit=False, frame_id)

        # 4. Memória cheia: Aplicar algoritmo de substituição de página
        frame_vitima_id = self.substituir_pagina(numero_pagina)
        return False, frame_vitima_id

    def substituir_pagina(self, nova_pagina):
        """
        TODO: IMPLEMENTAR PELO GRUPO
        Esta função deve escolher uma página 'vítima' para ser substituída
        com base no algoritmo escolhido (FIFO ou LRU), atualizar o frame
        escolhido com a nova_pagina e retornar o ID do frame que foi alterado.
        """
        frame_escolhido_id = 0

        # Escreva a lógica do algoritmo aqui...

        # Exemplo de atualização (substitua pela lógica real):
        # self.frames[frame_escolhido_id].pagina_alocada = nova_pagina

        return frame_escolhido_id

    def imprimir_mapa_memoria(self, passo, pagina_acessada, foi_hit, frame_alterado=None):
        """
        TODO: IMPLEMENTAR PELO GRUPO
        Esta função deve imprimir o estado atual da memória física (frames) no terminal,
        conforme o padrão visual exigido no enunciado do trabalho.
        """
        status = "Hit" if foi_hit else "Page Fault"
        print(f"\n--- Passo {passo}: Acesso à Página {pagina_acessada} ({status}) ---")

        # Exemplo de iteração sobre os frames para os alunos completarem o print:
        for frame in self.frames:
            conteudo = f"Página {frame.pagina_alocada}" if frame.pagina_alocada is not None else "[Vazio]"
            marcador = " <-- Alterado" if frame.id_frame == frame_alterado and not foi_hit else ""
            print(f"[Frame {frame.id_frame}]: {conteudo}{marcador}")

        print("-" * 40)


class Simulador:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo

    def executar(self):
        try:
            with open(self.caminho_arquivo, 'r') as arquivo:
                linhas = arquivo.readlines()
        except FileNotFoundError:
            print(f"Erro: O arquivo '{self.caminho_arquivo}' não foi encontrado.")
            return

        # Limpa linhas vazias ou comentários se houver
        linhas = [l.strip() for l in linhas if l.strip() and not l.strip().startswith('#')]

        if not linhas:
            print("Erro: Arquivo de entrada vazio.")
            return

        # A primeira linha válida define o número de frames na memória RAM simulada
        num_frames = int(linhas[0])
        tabela_paginas = TabelaPaginas(num_frames)

        print(f"Iniciando simulação com {num_frames} frames disponíveis.")
        print("=" * 40)

        # As linhas seguintes são a sequência de acessos às páginas
        passo = 1
        for linha in linhas[1:]:
            numero_pagina = int(linha)

            # Processa o acesso na tabela de páginas
            foi_hit, frame_id = tabela_paginas.acessar_pagina(numero_pagina)

            # Renderiza o mapa de memória para o aluno ver o passo a passo
            tabela_paginas.imprimir_mapa_memoria(passo, numero_pagina, foi_hit, frame_id)
            passo += 1

        # Exibição das estatísticas finais da simulação
        print("\n================ STATS FINAIS ================")
        print(f"Total de Acessos: {tabela_paginas.total_acessos}")
        print(f"Total de Page Faults: {tabela_paginas.total_page_faults}")
        if tabela_paginas.total_acessos > 0:
            taxa_faults = (tabela_paginas.total_page_faults / tabela_paginas.total_acessos) * 100
            print(f"Taxa de Page Faults: {taxa_faults:.2f}%")
        print("==============================================")


if __name__ == "__main__":
    # Permite passar o arquivo de entrada por argumento de linha de comando ou usa um padrão
    arquivo_entrada = sys.argv[1] if len(sys.argv) > 1 else "entrada.txt"
    simulador = Simulador(arquivo_entrada)
    simulador.executar()
