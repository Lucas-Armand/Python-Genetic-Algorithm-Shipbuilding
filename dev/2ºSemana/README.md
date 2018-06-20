# Discrição das atividades da segunda semana:

Nesse ponto se iniciou uma busca por uma maneira de se gerar ordenações aleatórias que fosse fisicamente possiveis de serem contruidas. O desafio é construir uma maneira lógica de gerar sequencia de construção de blocos, mas sem produzir sequências fisicamente impossiveis (como uma sequencia que comece pelos blocos de deck) e ao mesmo tempo sem excluir sequencias viáveis (como um método que só gere construção em camadas).

Inicialmente estudamos as principais ordenações de construção, com uma ótica aonde os blocos transitam entre três estados: O estado de "off" (a onde o bloco não pode ser selecionado), o modo "standby" (a onde o bloco fica disponivel para ser selecionado) e modo "on" (os blocos já selecionados). Para a ordenação ser possivel é escolhido um bloco inicial e apartir dessa escolhas são liberados para seleção os blocos que podem ser construidos em sequencia, a ordenação esta concluida quando todos os blocos foram selecionados. 

![Fig.1.](https://github.com/Lucas-Armand/genetic-algorithm/blob/master/2%C2%BASemana/IMAGES/ilustra%C3%A7%C3%A3o.png)
- Fig.1 - Ilustração demonstrando um possivel arranjo de releção entre blocos. Os 'bloco 1' e 'bloco 2' & 'bloco 1' e 'bloco 3' são ligados por um relação de liberação plena, mas os 'bloco 2'-'bloco 4' e 'bloco 3'-'bloco 4' são ligados por uma relação de liberação parcial.

A imagem (1) a cima ilustra um rede de blocos simples. Seja por exemplo o "bloco 1" o primeiro a ser selecionado. As setas indicam que a seleção desse bloco libera os "blocos 2" e "bloco 3", ou seja nesse estado podemos somente selecionar ou o "bloco 2" ou o "bloco 3". Podemos supor então que seja, por exemplo, o "bloco 3" o novo escolhido. Nesse caso o conjunto dos blocos para seleção não muda, isso porque a seta que liga o "bloco 3" ao "bloco 4" é uma seta clara ( o que segnifica 'liberação parcial'), em outras palavras o único bloco que pode ser selecionado agora é o "bloco 2" que uma vez selecionado libera o "bloco 4" ( o "bloco 4" por que todos os blocos que estão ligados a ele com setas de liberação parcial foram selecionados). Por fim selecionamos o 'bloco 4' e a ordem é definida: 'bloco 1', 'bloco 3', 'bloco 2' e 'bloco 4'.

Inicialmente, para entender como es contruimos diagramas que representavam a progreção dentro de uma determinada regra de construção a partir de uma escolha qualquer de um bloco inicial. Segue os esquemas para construção em grandes blocos (2) e construção em camadas (3).

![Fig.2.](https://github.com/Lucas-Armand/genetic-algorithm/blob/master/2%C2%BASemana/IMAGES/Proposta%20-%20Grandes%20Blocos.png)
- Fig.2 - Esquema de Contrução em Grandes Blocos - As setas mostram os blocos liberados para seleção a partir da seleção de um determinado bloco, é possivel gerar uma ordenação de edificação em grandes blocos qualquer partindo de um bloco de fundo escolhido de forma arbitrária. As setas escuras indicam uma liberação completa, já as setas claras uma liberação parcial. Ou seja, para que um bloco qualquer [Bj] (com execção do escolhido inicialmente) possa ser selecionado é necessário que, ou que um bloco, 
![Fig.3.](https://github.com/Lucas-Armand/genetic-algorithm/blob/master/2%C2%BASemana/IMAGES/Proposta%20-%20Camadas.png)
- Fig.3 - Esquema de Contrução em Camadas, perceba que os dois blocos de todo de cada grande anel foram unidos num unico nóe para facilitar a represetanção.

A partir dai os autores buscaram uma maneira de escrever as regras de uma contrusção geral que respeitasse somente dois paramentros

* Uma construção fisicamente coerente (os blocos que sustentados não devem vir antes dos que sustentam)
* Uma construção continuada (um bloco só deve ser edificado se ao lado for edificado)

Porem chegouse a conclusão de que não era possivel realizar tal representação através do modelo proposto pelo seguinte motivo. Dentro das regras propostas existe uma transição de estados que é especial. A verdade é que o primeiro bloco de cada tipo deve transitar entre estados de forma especial, ou seja, a segunda restrição implicava que para eu poder construir o castado deveria haver um bloco de costado ao lado do bloco que eu iria construir, mas se é isso, como construir o primeiro bloco de costado? 

Muitas tentativas foram feitas a fim de se contornar essa situação, mas no fim decediu-se por executar a ordenação só sobre a primeira restrição e utilizar uma função punitiva para penalizar ordenação descontinuadas.
