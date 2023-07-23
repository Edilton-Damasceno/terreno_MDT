# ###############################################
# Desenhando Terrenos (MDTs e Imagens)
# ###############################################

import pyglet
from pyglet.window import key
import cArvoreBinaria
import math
import os
path = os.path.join(os.path.dirname(__file__), 'DEMs')

drawMDT = True

# *******************************************************
# ***                                                 ***
# *******************************************************
def leImagem(arq):

	img = pyglet.image.load(arq)
	return img

# *******************************************************
# ***                                                 ***
# *******************************************************

def calculaElevacoes(MDT):

	# Retorna a matriz das amostras.
	format = 'I'
	pitch = MDT.width * len(format)
	amostras = MDT.get_image_data().get_data(format, pitch)

	return amostras

# *******************************************************
# ***                                                 ***
# *******************************************************

def criaTriangulacao(erro, tipo, node, triangles, bat, fill=True):

	if node is not None:
		if tipo == 'E':
			# No caso do tipo ser por erro, imprime apenas os triângulos que satisfazem o erro.
			if node.erro >= erro:
				tri = pyglet.shapes.Line(node.desenharX1, node.desenharY1, node.desenharX2, node.desenharY2, color=(255, 0, 255, 255), batch=bat)
				triangles.append(tri)

				tri = pyglet.shapes.Line(node.desenharX2, node.desenharY2, node.desenharX3, node.desenharY3, color=(255, 0, 255, 255), batch=bat)
				triangles.append(tri)

				tri = pyglet.shapes.Line(node.desenharX3, node.desenharY3, node.desenharX1, node.desenharY1, color=(255, 0, 255, 255), batch=bat)
				triangles.append(tri)

		else:
			# No caso do tipo ser por nivel, imprime todos os triângulos do nivel.
			tri = pyglet.shapes.Line(node.desenharX1, node.desenharY1, node.desenharX2, node.desenharY2, color=(255, 0, 255, 255), batch=bat)
			triangles.append(tri)

			tri = pyglet.shapes.Line(node.desenharX2, node.desenharY2, node.desenharX3, node.desenharY3, color=(255, 0, 255, 255), batch=bat)
			triangles.append(tri)

			tri = pyglet.shapes.Line(node.desenharX3, node.desenharY3, node.desenharX1, node.desenharY1, color=(255, 0, 255, 255), batch=bat)
			triangles.append(tri)

		# Chama a funçao recursivamente passando os nós filhos.
		criaTriangulacao(erro, tipo, node.left, triangles, bat, fill=False)
		criaTriangulacao(erro, tipo, node.right, triangles, bat, fill=False)

# *******************************************************
# ***                                                 ***
# *******************************************************
if __name__ == '__main__':

	global window, MDT_Image, MDT_Triang

	# Lendo a imagem.
	img = f"{path}/Terreno0.5K.jpg"
	MDT_Image = leImagem(img)

	# Obtendo as dimenções da imagem.
	WIN_X = MDT_Image.width
	WIN_Y = MDT_Image.height

	# Definindo o nível máximo com base nas dimenssões da imagem.
	nivelMax = (math.log2(WIN_X*WIN_Y)-1)
	nivelMax = int(nivelMax)

	nivel = 0
	erro = 0

	# Controlando a entrada do usuário.
	tipo = input('Deseja Visualizar por nivel ou por erro? [N/E]: ').upper()
	while tipo != 'N' and tipo != 'E':
		print('Opção inválida! Escolha N ou E!')
		tipo = input('Deseja Visualizar por nivel ou por erro? [N/E]: ').upper()

	if tipo == 'N':
		nivel = int(input(f'Escolha um nivel de detalhe entre 0 e {nivelMax}: '))
		while nivel < 0 or nivel > nivelMax:
			print(f'\nNivel inválido! Escolha um nivel entre 0 e {nivelMax}!')
			nivel = int(input(f'Escolha um nivel de detalhe entre 0 e {nivelMax}: '))
	else:
		erro = float(input(f'Escolha um limite de erro entre 0.1 e 0.5: '))
		while erro < 0 or erro > 1:
			print(f'\nLimite inválido! Escolha um limite entre 0.1 e 0.5!')
			erro = float(input(f'Escolha um limite de erro entre 0.1 e 0.5'))
		nivel = nivelMax

	# Coletando as amostras.
	amostra = calculaElevacoes(MDT_Image)

	# Criando a arvore e passando os dados.
	arvore = cArvoreBinaria.ArvoreBinaria(tipo, nivel, WIN_X, WIN_Y, amostra)
	arvore.populaArvore()

	# As funções a seguir criam uma janela gráfica para desenho.
	window = pyglet.window.Window(WIN_X, WIN_Y)
	window.set_caption('Visualizando um Modelo Digital de Terreno')

	# Um "lote" de objetos gráficos é criado no Pyglet para que possamos
	# preencher com o que deve ser desenhado a cada "frame"
	MDT_Triang = pyglet.graphics.Batch()

	# A lista dos "shapes" do Pyglet a serem desenhados começa vazia
	tri = []

	# Essa função cria os "shapes" do Pyglet armazendo a lista tri e adicionando no "lote" MDT_Triang
	criaTriangulacao(erro, tipo, arvore.root, tri, MDT_Triang, True)

	# Usando o "decorator" do Python é possível associar funções a eventos do ambiente de janelas
	# Abaixo dois tipos de eventos são associados a funções:
	# on_draw() => função chamada sempre que a tela precisa ser redesenhada.
	# on_key_press() => função chamada sempre que uma tecla for pressionada no teclado

	@window.event
	def on_draw():
		global drawMDT

		# Limpa a janela de desenho
		window.clear()

		# com base no valor armazenado em "drawMDT" decide se será mostrada a imagem do terreno ou
		# sua representação como uma triangulação
		if drawMDT:
			MDT_Image.blit(0, 0, 0)
		else:
			MDT_Triang.draw()

	# key press event
	@window.event
	def on_key_press(symbol, modifier):
		global drawMDT

		# Mapeia as teclas que deverão gerar alguma ação dentro da aplicação
		# No caso a tecla 'I' chaveia entre a imagem e a triangulação
		# enquanto que a tecla 'T' recria os elementos de desenho alternando
		# entre triangulos preenchidos ou só com o contorno.
		# O parametro "modifier" indica se a tecla "SHIFT" estava acionada
		# permitindo diferenciar entre 'I' e 'i'
		if symbol == key.I:
			drawMDT = True
		elif symbol == key.T:
			drawMDT = False
			criaTriangulacao(erro, tipo, arvore.root, tri, MDT_Triang, modifier & key.MOD_SHIFT)

	# Aqui a aplicação entra no loop de eventos e só retorna quando a tecla 'ESC' for pressionada
	pyglet.app.run()

	# Atenção que todos os comandos colocados a partir desse ponto só serão executados ao
	# final da aplicação.
	print("Só passo aqui no final da aplicação!")