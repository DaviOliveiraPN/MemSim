###
###     S I M U L A D O R    D E    M E M Ó R I A
###
### Prof. Filipo - github.com/ProfessorFilipo/MemSim/
###
### Grupo 11 - Algoritmos implementados: Segunda Chance (Clock) e Ótimo (OPT)
###

import sys


class Frame:
    def __init__(self, id_frame):
        self.id_frame = id_frame
        self.pagina_alocada = None  # Armazena o número da página ou None se estiver vazio

        # Atributos auxiliares usados pelos algoritmos de substituição:
        self.bit_referencia = 0   # usado pelo algoritmo Segunda Chance (Clock)
        self.timestamp_carga = -1  # ordem (sequencial) em que a página foi carregada no frame,
                                    # usado para desempates (qual página está há mais tempo na memória)


class TabelaPaginas:
    """
    Classe base: contém a lógica comum a qualquer algoritmo de substituição
    (detecção de hit/fault, ocupação de frames vazios, contabilização de
    estatísticas e impressão do mapa de memória).

    Cada algoritmo específico (Segunda Chance, Ótimo, etc.) deve herdar desta
    classe e implementar o método `substituir_pagina`.
    """

    def __init__(self, num_frames):
        # Inicializa a memória física com a quantidade de frames especificada
        self.frames = [Frame(i) for i in range(num_frames)]
        self.total_page_faults = 0
        self.total_acessos = 0
        self._contador_carga = 0  # "relógio lógico" que marca a ordem de carregamento das páginas

    def acessar_pagina(self, numero_pagina):
        self.total_acessos += 1

        # 1. Verificar se a página já está em algum frame (Hit)
        for frame in self.frames:
            if frame.pagina_alocada == numero_pagina:
                self._ao_acertar(frame)
                return True, frame.id_frame  # Retorna (Hit=True, frame_id)

        # 2. Se não encontrou, ocorreu um Page Fault!
        self.total_page_faults += 1

        # 3. Verificar se existe algum frame vazio disponível
        for frame in self.frames:
            if frame.pagina_alocada is None:
                self._carregar_pagina(frame, numero_pagina)
                return False, frame.id_frame  # Retorna (Hit=False, frame_id)

        # 4. Memória cheia: Aplicar algoritmo de substituição de página
        frame_vitima_id = self.substituir_pagina(numero_pagina)
        return False, frame_vitima_id

    def _carregar_pagina(self, frame, pagina):
        """Carrega 'pagina' em 'frame' e atualiza os metadados comuns."""
        frame.pagina_alocada = pagina
        frame.bit_referencia = 1
        frame.timestamp_carga = self._contador_carga
        self._contador_carga += 1

    def _ao_acertar(self, frame):
        """Hook chamado quando ocorre um Hit. Subclasses podem sobrescrever
        para atualizar metadados próprios (ex: bit de referência no Clock)."""
        frame.bit_referencia = 1

    def substituir_pagina(self, nova_pagina):
        """
        Deve escolher uma página 'vítima' para ser substituída, atualizar o
        frame escolhido com 'nova_pagina' e retornar o ID do frame alterado.
        """
        raise NotImplementedError("Cada algoritmo deve implementar substituir_pagina().")

    def imprimir_mapa_memoria(self, passo, pagina_acessada, foi_hit, frame_alterado=None):
        status = "Hit" if foi_hit else "Page Fault"
        print(f"\n--- Passo {passo}: Acesso à Página {pagina_acessada} ({status}) ---")

        for frame in self.frames:
            conteudo = f"Página {frame.pagina_alocada}" if frame.pagina_alocada is not None else "[Vazio]"
            marcador = " <-- Alterado" if frame.id_frame == frame_alterado and not foi_hit else ""
            print(f"[Frame {frame.id_frame}]: {conteudo}{marcador}")

        print("-" * 40)


class TabelaPaginasSegundaChance(TabelaPaginas):

    def __init__(self, num_frames):
        super().__init__(num_frames)
        self.ponteiro = 0

    def substituir_pagina(self, nova_pagina):
        n = len(self.frames)

        while True:
            frame_atual = self.frames[self.ponteiro]

            if frame_atual.bit_referencia == 0:
                frame_atual.pagina_alocada = nova_pagina
                frame_atual.bit_referencia = 1
                frame_atual.timestamp_carga = self._contador_carga
                self._contador_carga += 1

                vitima_id = frame_atual.id_frame
                self.ponteiro = (self.ponteiro + 1) % n
                return vitima_id
            else:
                frame_atual.bit_referencia = 0
                self.ponteiro = (self.ponteiro + 1) % n

    def imprimir_mapa_memoria(self, passo, pagina_acessada, foi_hit, frame_alterado=None):
        status = "Hit" if foi_hit else "Page Fault"
        print(f"\n--- Passo {passo}: Acesso à Página {pagina_acessada} ({status}) ---")

        for frame in self.frames:
            conteudo = f"Página {frame.pagina_alocada}" if frame.pagina_alocada is not None else "[Vazio]"
            marcador = " <-- Alterado" if frame.id_frame == frame_alterado and not foi_hit else ""
            ponteiro_marca = " (Ponteiro do Relógio)" if frame.id_frame == self.ponteiro else ""
            print(f"[Frame {frame.id_frame}]: {conteudo}{marcador}{ponteiro_marca}")

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
        tabela_paginas = TabelaPaginasSegundaChance(num_frames)

        print(f"Iniciando simulação com {num_frames} frames disponíveis.")
        print("=" * 40)

        # As linhas seguintes são a sequência de acessos às páginas
        passo = 1
        for linha in linhas[1:]:
            numero_pagina = int(linha)

            foi_hit, frame_id = tabela_paginas.acessar_pagina(numero_pagina)
            tabela_paginas.imprimir_mapa_memoria(passo, numero_pagina, foi_hit, frame_id)
            passo += 1

        print("\n================ STATS FINAIS ================")
        print(f"Total de Acessos: {tabela_paginas.total_acessos}")
        print(f"Total de Page Faults: {tabela_paginas.total_page_faults}")
        if tabela_paginas.total_acessos > 0:
            taxa_faults = (tabela_paginas.total_page_faults / tabela_paginas.total_acessos) * 100
            print(f"Taxa de Page Faults: {taxa_faults:.2f}%")
        print("==============================================")


if __name__ == "__main__":
    arquivo_entrada = sys.argv[1] if len(sys.argv) > 1 else "entrada.txt"
    simulador = Simulador(arquivo_entrada)
    simulador.executar()

