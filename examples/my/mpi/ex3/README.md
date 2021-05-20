# OpemMPI---Multiplica-o-de-Matrizes
Multiplicação de Matrizes de forma paralela utilizando OpenMPI

O código presente tem como objetivo o calcular a multiplicação de matrizes muito grande utilizando multiplicação em blocos e paralelização.

A multiplicação por bloco é feita da senguinte maneira, Supondo uma multiplicação normal:

        A           B
    | 1 2 3 |   | 1 2 3 |
    | 4 5 6 | X | 4 5 6 | = C
    | 7 8 9 |   | 7 8 9 |
  
  
Ao utilizarmos bloco temos A e B subdivididas em partições, A1, A2, A3...An e B1, B2, B3,...Bn Obtemos partições C1, C2, C3,...Cn. De forma que o nrParticoes seja sempre equivalente a quantidades de processadores paralelos de um computado.


      A1   A2
    | 1 | 2 3 |   |_1_2_3_|->B1     (C1 = A1 x B1)      
    | 4 | 5 6 | X | 4 5 6 |      ==>                 C = C1 + C2;   
    | 7 | 8 9 |   | 7 8 9 |->B2     (C2 = A2 x B2)
  
  
Dessa forma temos que para essa divisão de 2 blocos, obtemos C1 = A1xB1, C2 = A2xB2, portanto C = C1+C2. Paralelizando o problema podemos ganhar em tempo de desempenho na obtenção dos resultados. No caso de MPI o Número de partições pode ser equivalente ao montante de processadores/threads disponíveis em uma rede.

O presente repositório busca resolver esse problema de multiplicação de matrizes parallelizado com:

###################################################
### Disciplina de Programação Paralela          ###
###################################################

Alunos: Devair Dener Darolt
Professor: Maurício Pillon

###################################################

* Compilação
    $ make

* Execução
    $make run
    

* Limpar arquivos compilados
    - executar:
    $ make clean

###################################################
##             Passo a passo                     ##
###################################################

1    $make gmat              - Criar executável que gera matriz
2    $./gmat 100 100         - Cria matriz 100x100-mat.map
3    $make                   - Executa o comando --> mpicc  -Wall -O3 main.c matriz.c tools.c  -o  executavel
4    $make run               - Executa o comando --> mpirun -hostfile hostfile -np 4  executavel 10x10-mat.map  10x10-mat.map  3
                                                        |                 |        |      |            |            |           |
                    Programa que executa o compilado____|                 |        |      |            |            |           |
      Arquivo com a configuração de slots e maquinas______________________|        |      |            |            |           |
                                 Numero de processos_______________________________|      |            |            |           |
                          Nome do programa compilado______________________________________|            |            |           |
Nome do arquivo contendo a matriz A gerada no ./gmat___________________________________________________|            |           |
Nome do arquivo contendo a matriz B gerada no ./gmat________________________________________________________________|           |
                                                                                                                                |
nrParticoes: Número de partições, precisa ser igual                                                                             |
(nrProcesso -1) de modo que cada slave recebe uma partição______________________________________________________________________|
