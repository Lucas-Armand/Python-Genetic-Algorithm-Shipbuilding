# Genetic Algorithm in Python to Solve Block Ordering in Shipbuilding

A realistic analysis of the potential of the method of optimization of the process of building blocks of ships in shipbuilding yards is presented and discusses the difficulties of their implementation. A theoretical review of the problem of building and of the optimization techniques used in it was carried out. It was verified that the method proposed here is filling a gap, representing an important contribution to solving problems of this nature. A genetic algorithm model was developed and implemented for the case of ordering the building for different strategies, obtaining results that prove the effectiveness of the method. Finally, a discussion on the limitations and potentialities of the method is presented and proposals are presented for the best and possible applications for naval engineering.

# Algorítimo Genético em Python para Resolver a Ordenação dos Blocos na Edificação de Navios

O trabalho apresenta uma análise realista do potencial do método de otimização do processo de edificação de blocos de navios em estaleiros de construção naval e discute as dificuldades para sua implementação. Foi realizada um uma revisão teórica do problema edificação e das técnicas de otimização nele empregados, verificando-se que o método aqui proposto vem a prencher uma lacuna, representando uma contribuição importante para solução de problemas dessa naturaza. Foi desenvolvido e implementado um modelo de algoritmo genético para o caso de ordenação da edificação para diferentes estratégias tendo-se obtidos resultados que comprovam a eficacia do método. Por fim, apresenta-se uma discussão sobre as limitações e potencialidades do método e são apresentadas propostas para aperfeiçoamente e possíveis aplicações para área da engenharia naval.

## Requisitos

* Python 2.7 
* NumPy 1.10.4
* MatPlotLib 2.2.2 

## Input:

* GeometriaNavio.csv - Arquivo com a geometria do navio: Número de blocos, tamanho e posição.
!(Imagem dos Blocos da Embarcação)[link1]
* EstructuralLoP.csv - Arquivo com as relações de precedência entre os blocos. Restrições físicas.
!(Esquema de precdência dos Blocos)[link2]
* Matriz de correlação entre tempos de edificação. Representa interações positivas e negativas nos recursos utilizados para a construção dos blocos.
!(Aqui talvez seja mais de uma foto)[link2]


## Output:

O resultado do programa apresenta o tempo total de construção do návio em "unidades de tempo", com
