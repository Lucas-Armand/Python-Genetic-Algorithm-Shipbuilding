# Genetic Algorithm in Python to Solve Block Ordering in Shipbuilding

A realistic analysis of the potential of this optimization method to shipbuilding in shipyards is presented and the difficulties of its implementation are discussed. A review of optimization techniques used in shipbuilding was carried out and was verified that this kind of work representing an breakthrough to the area. A genetic algorithm model was developed and implemented for different ordering strategies, obtaining results that prove the effectiveness of this method. Finally, a discussion on the limitations and potentialities of genetic algorithm models and possible applications for naval engineering are presented.

# Algorítimo Genético em Python para Resolver a Ordenação dos Blocos na Edificação de Navios

O trabalho apresenta uma análise realista do potencial do método de otimização do processo de edificação de blocos de navios em estaleiros de construção naval e discute as dificuldades para sua implementação. Foi realizada um uma revisão teórica do problema edificação e das técnicas de otimização nele empregados, verificando-se que o método aqui proposto vem a prencher uma lacuna, representando uma contribuição importante para solução de problemas dessa naturaza. Foi desenvolvido e implementado um modelo de algoritmo genético para o caso de ordenação da edificação para diferentes estratégias tendo-se obtidos resultados que comprovam a eficacia do método. Por fim, apresenta-se uma discussão sobre as limitações e potencialidades do método e são apresentadas propostas para aperfeiçoamente e possíveis aplicações para área da engenharia naval.

## Requisitos

* Python 2.7 
* NumPy 1.10.4
* MatPlotLib 2.2.2 

## Input:

* GeometriaNavio.csv - Arquivo com a geometria do navio: Número de blocos, tamanho e posição.

<p float="left">
<img src="https://github.com/Lucas-Armand/genetic-algorithm/blob/master/img/ship.png" width="85%">
<img src="https://github.com/Lucas-Armand/genetic-algorithm/blob/master/img/ship_blocks.png" width="15%">
</p>

* EstructuralLoP.csv - Arquivo com as relações de precedência entre os blocos. Restrições físicas.
<img src="https://github.com/Lucas-Armand/genetic-algorithm/blob/master/img/ordenation.png"/>

* Matriz de correlação entre tempos de edificação. Representa interações positivas e negativas nos recursos utilizados para a construção dos blocos.
!(Aqui talvez seja mais de uma foto)[link2]


## Output:

O resultado do programa apresenta o tempo total de construção do návio em "unidades de tempo", com
