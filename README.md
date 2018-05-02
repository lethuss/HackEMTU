## Vizualisador de tendências *Origem x Destino* por meio de análise e clusetring do histórico de bilhetagem de usuários do serviço publico de mobilidade urbana

*Projeto desenvolvido durante o HACKEMTU 2018 realizado nos dias 7 e 8 de abril de 2018 na Universidade de Campinas - Unicamp.*

Autores:
* Gabriel Teston - https://github.com/Gabriel-Teston
* Bernardo Rodrigues - https://github.com/lethuss
* Lucas Dias - https://github.com/luketis


A ideia foi criar uma ferramenta que auxiliasse a análise de gestores do ramo de mobilidade urbana, dando a eles uma forma de visualizar as tendências e padrões de movimentação dos usuários do transporte público com base em dados atuais. Essas tendências de movimentação são colhidas com precisão a cada 10 anos por meio de uma pesquisa semelhante a um censo demográfico, onde pesquisadores visitam as casas de todos os habitantes de uma região perguntando-lhes sobre suas intenções de deslocamento. Acredita-se que essa informação colhida, apesar de rica, se torna obsoleta rapidamente e por isso desenvolveu-se a ferramenta em questão para otimizar este processo, contemplando, até o momento, o modal ônibus exclusivamente.

Baseado no cruzamento dos dados de bilhetagem dos usuários e na geolocalização do ônibus, foi possível determinar quando e onde um usuário embarcou. Considerando os dados dos embarques subsequentes tentou-se estimar qual era o destino dos embarques anteriores. Por exemplo, alguém que sempre embarca em um ponto próximo a sua casa no inicio da sua jornada de trabalho diária, irá, provavelmente, embarcar no ponto mais próximo ao seu trabalho no caminho de volta para casa. Dessa forma podemos estimar o par Origem x Destino, já que esse dado não está disponível a priori (um usuário não bilheta ao desembarcar de um ônibus).

O conjunto desses pares passa por um algoritmo de clustering para se obter as macro tendências de movimentação e estas auxiliarem nos processos de tomada de decisão dos gestores, tais como: validar linhas, sugerir novas linhas, entre outros.

`O-D estimation.py` é o script que faz toda essa análise acima descrita, buscando os dados já cruzados em um banco implementado em um MongoDB local.

O script `ping.py` também foi uma prova de conceito que colheria os pares de embarque e desembarque por meio da infraestrutura de wifi do ônibus. Ao se conectar um usuário, o mesmo seria considerado "embarcado" e, ao desconectá-lo, "desembarcado". Idealmente, essa coleta de dados seria feita por meio de pacotes probe do protocolo WIFI; dessa forma somente seria necessário que os dispositivos, como smartphones, dos usuários estivessem com o WIFI habilitado e não propriamente conectados na rede do ônibus
