import Node

class ArvoreBinaria:
    def __init__(self, tipo: str, parametro, WIN_X, WIN_Y, amostra):
        self.tipo = tipo.upper()
        self.parametro = parametro + 1  # Nivel ou erro
        self.amostra = amostra  # Niveis de cinza
        self.WIN_X = WIN_X
        self.WIN_Y = WIN_Y
        self.root = Node.Node()

    def calculaErro(self, xaa, yaa, xbb, ybb, xcc, ycc):

        # mudando para usar como indice
        if yaa == 0:
            yaa += 1
        if ybb == 0:
            ybb += 1
        if ycc == 0:
            ycc += 1

        # Vetor
        pontos = [0] * 6
        pontos[0] = xaa
        pontos[1] = yaa
        pontos[2] = xbb
        pontos[3] = ybb
        pontos[4] = xcc
        pontos[5] = ycc

        pitch = self.WIN_X

        total = 0

        # Obtendo a elevação em cada vertice.
        for c in range(0, 6, 2):
            elevacao = self.amostra[((pontos[c + 1] - 1) * pitch + pontos[c]) - 1]
            total += elevacao
        media_elevacoes = total / 3

        # Calculando onde o ponto médio tá e obtendo a sua elevação.
        ponto_medio_x = (xaa + xbb + xcc) // 3
        ponto_medio_y = (yaa + ybb + ycc) // 3
        elevacao_ponto_medio = self.amostra[((ponto_medio_y - 1) * pitch + ponto_medio_x) - 1]


        erro = 0
        # Retornando o percentual de erro.
        if media_elevacoes >= elevacao_ponto_medio:
            if media_elevacoes == 0:
                media_elevacoes = 1
            erro = (media_elevacoes - elevacao_ponto_medio) / media_elevacoes

        else:
            erro = (elevacao_ponto_medio - media_elevacoes) / elevacao_ponto_medio

        return erro

    def populaArvore(self):
        n = 2 ** (self.parametro)  # é o nivel
        self.root.left = Node.Node()
        self.root.right = Node.Node()
        self._populaArvoreRecursivo(self.root.left, 0, 0, self.WIN_X, 0, self.WIN_X, self.WIN_Y, n - 2)
        self._populaArvoreRecursivo(self.root.right, 0, 0, 0, self.WIN_Y, self.WIN_X, self.WIN_Y, n - 2)
        self.pre_order(self.root.left)

    def _populaArvoreRecursivo(self, no, xA, yA, xB, yB, xC, yC, n):
        if n < 0:
            return

        # Calcula a hipotenusa do triangulo cortado no meio.
        h1 = (((xA - xB) ** 2 + (yA - yB) ** 2) ** (1 / 2)) // 1
        h2 = (((xA - xC) ** 2 + (yA - yC) ** 2) ** (1 / 2)) // 1
        h3 = (((xB - xC) ** 2 + (yB - yC) ** 2) ** (1 / 2)) // 1

        # Caso a aresta AB = AC quer dizer que o traço tem que ser do ponto A até o meio da BC.
        if (h1 == h2) or (h1 - 1 == h2) or (h1 + 1 == h2):

            # Calcula o ponto do meio da reta.
            xM = (xB + xC) // 2
            yM = (yB + yC) // 2

            # salva os pontos que o nó deve desenhar.
            desenharX1 = xA
            desenharY1 = yA
            desenharX2 = xB  # Nesse caso AB == AC usa o vertice A.
            desenharY2 = yB
            desenharX3 = xC
            desenharY3 = yC

            no.desenharX1 = desenharX1
            no.desenharY1 = desenharY1
            no.desenharX2 = desenharX2
            no.desenharY2 = desenharY2
            no.desenharX3 = desenharX3
            no.desenharY3 = desenharY3

            # Se por erro de aproximação.
            if self.tipo == 'E':

                # calcula o erro.
                erro = self.calculaErro(xA, yA, xB, yB, xC, yC)
                no.erro = erro

            # Quando divide um triângulo são criados dois triângulos.
            if n > 0:
                n_left = n // 2
                n_right = n - n_left

                # Triângulo 1
                no.left = Node.Node()
                if n_left > 0:
                    self._populaArvoreRecursivo(no.left, xA, yA, xM, yM, xC, yC, n_left - 1)

                # Triângulo 2
                no.right = Node.Node()
                if n_right > 0:
                    self._populaArvoreRecursivo(no.right, xA, yA, xM, yM, xB, yB, n_right - 1)

        # AB = BC -> Semelhante a função de cima.
        elif h1 == h3 or (h1 - 1 == h3) or (h1 + 1 == h3):
            xM = (xA + xC) // 2
            yM = (yA + yC) // 2

            desenharX1 = xA
            desenharY1 = yA
            desenharX2 = xB
            desenharY2 = yB
            desenharX3 = xC
            desenharY3 = yC

            no.desenharX1 = desenharX1
            no.desenharY1 = desenharY1
            no.desenharX2 = desenharX2
            no.desenharY2 = desenharY2
            no.desenharX3 = desenharX3
            no.desenharY3 = desenharY3

            if self.tipo == 'E':
                erro = self.calculaErro(xA, yA, xB, yB, xC, yC)
                no.erro = erro

            if n > 0:
                n_left = n // 2
                n_right = n - n_left

                no.left = Node.Node()
                if n_left > 0:
                    self._populaArvoreRecursivo(no.left, xA, yA, xM, yM, xB, yB, n_left - 1)

                no.right = Node.Node()
                if n_right > 0:
                    self._populaArvoreRecursivo(no.right, xB, yB, xM, yM, xC, yC, n_right - 1)

        # AC = BC -> Semelhante a função de cima.
        elif h2 == h3 or (h2 - 1 == h3) or (h2 + 1 == h3):
            xM = (xA + xB) // 2
            yM = (yA + yB) // 2

            desenharX1 = xA
            desenharY1 = yA
            desenharX2 = xB
            desenharY2 = yB
            desenharX3 = xC
            desenharY3 = yC

            no.desenharX1 = desenharX1
            no.desenharY1 = desenharY1
            no.desenharX2 = desenharX2
            no.desenharY2 = desenharY2
            no.desenharX3 = desenharX3
            no.desenharY3 = desenharY3

            if self.tipo == 'E':
                erro = self.calculaErro(xA, yA, xB, yB, xC, yC)
                no.erro = erro

            if n > 0:
                n_left = n // 2
                n_right = n - n_left

                no.left = Node.Node()
                if n_left > 0:
                    self._populaArvoreRecursivo(no.left, xA, yA, xM, yM, xB, yB, n_left - 1)

                no.right = Node.Node()
                if n_right > 0:
                    self._populaArvoreRecursivo(no.right, xB, yB, xM, yM, xC, yC, n_right - 1)

    def pre_order(self, node):
        if node is not None:
            self.pre_order(node.left)
            self.pre_order(node.right)
