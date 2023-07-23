[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/kLaYap_r)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-718a45dd9cf7e7f842a935f5ebbe5719a5e09af4491e668f4dbf3b35d5cca122.svg)](https://classroom.github.com/online_ide?assignment_repo_id=11026504&assignment_repo_type=AssignmentRepo)
# Visualização de Terreno MDT. 

## Edilton de Jesus Damasceno

## Justificativa:

inicialmente pensei em usar uma AVL e ir balanceando, mas isso bagunçava a ordem dos triângulos, então utilizei uma arvore binaria simples, dividindo o quadrado inicial e passando o triângulo inferior para root.left e o superior para o root.right, fui cortando o triangulo e passando os dois triângulos menores como filhos, desse modo consegui criar uma arvore balanceada e que mantia a ordem de fatiamento dos triângulos. Essa foi a melhor forma que encontrei para resolver
o problema.

## Analise da complexidade dos principais métodos utilizados:

### Árvore:

- ### _calculaErro():

A complexidade da função está principalmente relacionada com o acesso à matriz amostra. O tempo necessário para acessar os valores da matriz é proporcional ao tamanho da matriz, que é determinada pelas dimensões da imagem do terreno. Portanto, a complexidade da função é linear em relação ao tamanho da imagem do terreno. A complexidade da função é O(n), onde n é o tamanho da imagem do terreno.

- ### _populaArvoreRecursivo():

A complexidade do método é determinada pela recursão em si. O método faz uma chamada recursiva para o filhos esquerdo e uma para o direito do nó atual, diminuindo o valor de n a cada chamada. A quantidade total de chamadas recursivas depende do valor inicial de n e da divisão repetida pela metade do valor de n em cada nível da árvore. Se a divisão for feita pela metade a cada chamada do método, ele pode ser considerado como O(2^n), onde n é o nível máximo da arvore.

### Terreno:

- ### criaTriangulacao():

A complexidade da função depende do número de nós na árvore. No caso do tipo de visualização ser por erro (tipo == 'E'), a função verifica se o erro do nó atual satisfaz a condição. Caso satisfaça, são criados três shapes de linha representando o triângulo, nesse caso a complexidade  é constante. No caso do tipo de visualização ser por nível (tipo != 'E'), independentemente do nível do nó, também são criados três shapes de linha representando o triângulo.
Dessa maneira a complexidade da função criaTriangulacao() é linear em relação ao número de nós na árvore binária. Com complexidade O(n) sendo n a quantidade de nós. 

- ### calculaElevacoes():

A complexidade da função calculaElevacoes é linear em relação ao número de pixels na imagem do terreno. Se a imagem tiver N pixels, a complexidade será O(N).
