# Genetic Algorithm in Python to Solve Block Ordering in Shipbuilding

A realistic analysis of the potential of this optimization method to shipbuilding in shipyards is presented and the difficulties of its implementation are discussed. A review of optimization techniques used in shipbuilding was carried out and was verified that this kind of work representing an breakthrough to the area. A genetic algorithm model was developed and implemented for different ordering strategies, obtaining results that prove the effectiveness of this method. Finally, a discussion on the limitations and potentialities of genetic algorithm models and possible applications for naval engineering are presented.

# Algorítimo Genético em Python para Resolver a Ordenação dos Blocos na Edificação de Navios

O trabalho apresenta uma análise realista do potencial do método de otimização do processo de edificação de blocos de navios em estaleiros de construção naval e discute as dificuldades para sua implementação. Foi realizada um uma revisão teórica do problema edificação e das técnicas de otimização nele empregados, verificando-se que esse tipo de trabalho representa um avanço a área. Para esse artifo o autor desenvolveu e implementou toda a modelação do problema e cada um dos "operadores genéticodos" do alogrítimo aplicando-os diferentes casos de restrições de edificação tendo-se obtidos resultados que comprovam a eficacia do método. Por fim, apresenta-se uma discussão sobre as limitações e potencialidades do método e são apresentadas propostas para aperfeiçoamente e possíveis aplicações para área da engenharia naval.

## Requisitos

* Python 2.7 
* NumPy 1.10.4
* MatPlotLib 2.2.2 

## Funcionalidade:

Para executar o algorítimo basta rodar o programa "**Genetic Alghoritmic (1 crane).py**". 

O programa foi construido em cima de uma classe deniminada "genetic" que é básicamente toda a programação do algorítimo genético orientado a objetos. Os principais métodos dessa classe são:

genetic
∟ run = executa o algorítimo genético
∟ gen_chromosome = gera um chromosomo de maneira aleatória, respeitando as restrições
∟ mutation = pega um cromossomo e tenta fazer uma mutação (alteração minima)
∟ crossover = recombina dois chromossomos gerando "indivíduos ordenações" novos
∟ time = calcula o tempo de uma ordenação (score)
∟ new_population =  gera um nova população de 'n' cromossomos novos, baseados nos melhores individuos da população anterior

### Input:
Os inputs do programa são dois arquivos do tipo csv, que contem os dados que caracterizam as retrições do problema, e uma matriz que é definida dentro do próprio código:

* **GeometriaNavio.csv** - Arquivo com a geometria do navio: Número de blocos, tamanho e posição. No navio usado ao todo são 16 blocos
de convés, 16 blocos de costado, 32 blocos de fundo e 6 de cofferdam (são blocos estanques que dividem o tanque) totalizando 70 blocos.

<p float="left" >
<img src="https://github.com/Lucas-Armand/genetic-algorithm/blob/master/img/ship.png" width="80%">
<img src="https://github.com/Lucas-Armand/genetic-algorithm/blob/master/img/ship_blocks.png" width="15%">
</p>

* **EstructuralLoP.csv** - Arquivo com as relações de precedência entre os blocos. Restrições físicas. O esquema a seguir representa as restições utilizadas na implementação. Os blocos mais abaixo são blocos de fundo, os blocos na meia altura são blocos de costado ou de cofferdam e os blocos mais acima do esquema são blocos de topo. É possível perceber oito "grupos de blocos" que são inter conectados entre si, na embarcação eles correspondem ao chamados "aneis gigantes", cada anel gigante possui dois blocos de topo (que são suportados pelos blocos de costado), dois blocos de costado (que são suportados pelo blocos do fundo, mas que só podem ser fixados depois do bloco de cofferdam se existir), alguns anéis tem um bloco de cofferdam e por fim (sustentando todos os blocos a cima) os quatro blocos de fundo.  

<img src="https://github.com/Lucas-Armand/genetic-algorithm/blob/master/img/ordenation.png"/>

* Matriz de correlação entre tempos de edificação: Representa interações positivas e negativas nos recursos utilizados para a construção dos blocos. Nas imagens a seguir temos um exemplo de Matriz de correlação e um esquema representando as etapas de contrução de dois blocos de um navio, aonde a última etapa é edificação e, dependendo da ordem em que eles são feitos, a edificação de um pode ser feita imeditamente após a do outro, ou será necessário esperar um tempo para o termino das etapas anteriores (esse efeito que os fatores de correlação pretendem capturar).

<p float="left" >
<img src="https://github.com/Lucas-Armand/genetic-algorithm/blob/master/img/time_correlation_matrix.png" width="45%">
<img src="https://github.com/Lucas-Armand/genetic-algorithm/blob/master/img/blocks_const.png" width="45%">
</p>

### Output:

Os resultados do programa são apresentado pelo o tempo total de construção do návio, da melhor ordenação obtida pelo programa, em "unidades de tempo" por geração, ou seja, os valores mostram, geração á geração, a convergência para o resultado ótimo do problema:
<img src="https://github.com/Lucas-Armand/genetic-algorithm/blob/master/img/terminal.png" width="80%">

### Vizulização dos resultados:

O resultado (cromossomo) é a sequencia dos "id"s dos blocos em ordem de edificação, mas como a forma como a resposta é construida tornaa de dificil comprienção  eu criei dois modos de vizualização dessas respostas:

<p float="left" >
<img src="https://github.com/Lucas-Armand/genetic-algorithm/blob/master/img/test.gif" width="45%">
<img src="https://github.com/Lucas-Armand/genetic-algorithm/blob/master/img/test1.png" width="45%">
</p>

As duas imagens acima são representações de uma mesma ordenação (ordenaçãod e construção pirmidal partindo do centro), o gráfico em calor tenta sintetizar em uma representação estática a sequência representada na animação através de uma escala de cor.  

Para gerar as vizualizações acima, basta usar os programas a seguir e entrar com a ordenação desejada:
 * [3DcolorShip](https://github.com/Lucas-Armand/genetic-algorithm/blob/master/vis/3DcolorShip.py)
 * [3DsequenceShip](https://github.com/Lucas-Armand/genetic-algorithm/blob/master/vis/3DsequenceShip.py)
