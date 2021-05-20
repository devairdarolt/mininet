
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <sys/time.h>
#define N 3

typedef struct
{
    int **matriz;
    int m;
    int n;
}Matriz;




//FUNÇÕES DE ALOCAÇÃO E LIBERAÇÃO DE MATRIZES 

int matriz_alocar (Matriz *matriz);
int **matriz_desalocar(int linhas, int colunas, int **matriz);

//FUNÇÕES DE SOMA E MULTIPLICAÇÃO DE MATRIZES UTILIZANDO OpenMP

Matriz matriz_somar(Matriz A, Matriz B);
void matriz_mult(Matriz *A, Matriz *B, Matriz *C);
Matriz matriz_multiplicar(Matriz A, Matriz B);

//FUNÇÕES DE MULTIPLICAÇÃO EM BLOCO UTILIZANDO OpenMP

Matriz *particiona_matriz_horizontal(Matriz M, int nrParticoes);
Matriz *particiona_matriz_vertical(Matriz A,int nrParticoes);
Matriz *matriz_bloco_multiplicar(Matriz A, Matriz B,int nrParticoes);


void matriz_print(Matriz matriz);
int matriz_print_2(Matriz *matriz);
int matriz_comparar(Matriz *A, Matriz *B);

