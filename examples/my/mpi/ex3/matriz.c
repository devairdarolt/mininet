/***
 * @autor Devair Dener Darolt
 * @disciplina Programação paralela 2021
 * 
 * Compilar  --> make
 * rodar     --> make run
 * limpar    --> make clean
 * 
 ***/

#include "matriz.h"

/**
 * Cria uma matriz mxn zerada na memória por referência
 * @param *matriz - linha = matriz->m , coluna = matriz->n 
 * @return 0/1
 * */
int matriz_alocar(Matriz *matriz)
{
    int **newMatriz = NULL;
    newMatriz = (int **)malloc(matriz->m * sizeof(int *));

    if (!newMatriz)
    {
        printf("ERROR: Out of memory\n");
        return 1;
    }

    for (int i = 0; i < matriz->m; i++)
    {
        newMatriz[i] = (int *)malloc(matriz->n * sizeof(int));
        if (!newMatriz)
        {
            printf("ERROR: Out of memory\n");
            return 1;
        }
    }
    for (int i = 0; i < matriz->m; i++)
    {
        for (int j = 0; j < matriz->n; j++)
        {
            newMatriz[i][j] = 0;
        }
    }
    matriz->matriz = newMatriz;
    return 0;
}

/**
 * Libera o espaço da memória reservado a matriz de inteiros
 * @param linhas - Matriz.m
 * @param colunas - Matriz.n
 * @param **matriz - Matriz.matriz
 * 
 * @return NULL
 * */
int **matriz_desalocar(int linhas, int colunas, int **matriz)
{

    if (matriz == NULL)
    {
        return NULL;
    }
    if (linhas < 1 || colunas < 1)
    {
        printf("** Erro: Parametro invalido **\n");
        return (NULL);
    }
    for (int i = 0; i < linhas; i++)
    {
        //printf("%p\n", matriz->matriz[i]);
        free(matriz[i]);
    }
    free(matriz);
    return (NULL); /* retorna um ponteiro nulo */
}

/**
 * Imprime o conteúdo de matriz.matriz por referência para poupar memória em caso de matrizes grandes 
 * @param *matriz - referência da matriz a ser impressa!
 * @return 0
 * */
int matriz_print_2(Matriz *matriz)
{
    int linha, coluna;
    linha = matriz->m;
    coluna = matriz->n;

    if (linha > 15)
        linha = 15;
    if (coluna > 15)
        coluna = 15;

    for (int j = 0; j < coluna; j++)
    {
        printf("\t(%d)", j);
    }
    printf("\n");

    for (int i = 0; i < linha; i++)
    {
        printf("(%d)", i);
        for (int j = 0; j < coluna; j++)
        {
            printf("\t%d", matriz->matriz[i][j]);
        }
        printf("\n");
    }

    printf("\n \
	WARNING: Impressão truncada em 15x15! \n \
	WARNING: Último elemento matriz[%d][%d] = %d \n \
	\n",
           matriz->m - 1, matriz->n - 1, matriz->matriz[matriz->m - 1][matriz->n - 1]);

    return 0;
}

/**
 * Imprime o conteúdo de matriz.matriz
 * @param matriz - Cópia de uma Matriz
 * @return void
 * */
void matriz_print(Matriz matriz)
{
    printf("\n");
    for (int i = 0; i < matriz.m; i++)
    {
        for (int j = 0; j < matriz.n; j++)
        {
            printf("\t%d", matriz.matriz[i][j]);
        }
        printf("\n");
    }
}

/**
 *Faz a soma de forma paralela entre A + B utilizando OpenMP 
 *@param A - Matriz A
 *@param B - Matriz B
 *@return C - Matriz C
 *   */
Matriz matriz_somar(Matriz A, Matriz B)
{
    Matriz C;

    if ((A.m != B.m) || (A.n != B.n))
    {
        printf("Dimensões incompatíveis!");
        return A;
    }
    C.m = A.m;
    C.n = A.n;
    matriz_alocar(&C);

    int i, j;

    //#pragma omp parallel for private(i, j) shared(A, B, C) collapse(2)
    for (i = 0; i < A.m; i++)
    {
        for (j = 0; j < A.n; j++)
        {
            //printf("Thread:%d\n",omp_get_thread_num());
            C.matriz[i][j] = A.matriz[i][j] + B.matriz[i][j];
        }
    }
    return C;
}

/**
 * Função para fazer multiplicação alterando C por referência
 * @param *A - referência de A
 * @param *B - referência de B
 * @param *C - referência de C
 * @return void
 * */
void matriz_mult(Matriz *A, Matriz *B, Matriz *C)
{
    if (A->n != B->m)
    {
        printf("Imcompativel para multiplicacao\n");
        exit(0);
    }
    if (C == NULL)
    {
        C = (Matriz *)malloc(sizeof(Matriz));
    }
    C->m = A->m;
    C->n = B->n;

    matriz_alocar(C);
    //matriz_print_2(A);
    //matriz_print_2(B);

    for (int i = 0; i < A->m; i++)
    {
        for (int k = 0; k < B->n; k++)
        {
            C->matriz[i][k] = (int)0;
            for (int j = 0; j < A->n; j++)
            {
                C->matriz[i][k] += (int)(A->matriz[i][j] * B->matriz[j][k]);
                //printf("%d ", omp_get_thread_num());
            }
        }
    }
}

/**
 * C= AxB --- Multiplica matriz A por matriz B  
 * @param A - Matriz A
 * @param B - Matriz B
 * @return C - Matriz C
 * */
Matriz matriz_multiplicar(Matriz A, Matriz B)
{
    Matriz *C = NULL;
    C = (Matriz *)malloc(sizeof(Matriz));
    //C = (Matriz *) calloc(1,sizeof(Matriz));
    C->m = A.m;
    C->n = B.n;
    if (A.n != B.m)
    {
        printf("Dimensões incompatíveis!");
        return *C;
    }
    matriz_alocar(C); //cria matriz zerada
    //matriz_print_2(&A);
    //matriz_print_2(&B);
    for (int i = 0; i < A.m; i++)
    {
        for (int j = 0; j < B.n; j++)
        {
            for (int k = 0; k < A.n; k++)
            {

                C->matriz[i][j] += A.matriz[i][k] * B.matriz[k][j];
            }
        }
    }
    return *C;
}
/**
 * Faz o particionamento horizontal de uma matriz
 * @param M - Matriz M
 * @param nrParticoes - número de partições horizontais de M
 * @return M_part[nrParticoes] - retorna vetor de partições de M
 * */
Matriz *particiona_matriz_horizontal(Matriz M, int nrParticoes)
{
    if (nrParticoes > M.m)
    {
        printf("O numero de particoes nao pode ser maior que a quantidade colunas matriz A, ou a quantidade de linhas de B.\n");
        return NULL;
    }
    int linhas = M.m;
    int colunas = M.n;
    int resto = linhas % nrParticoes;
    int tamanho_particao = (linhas - resto) / nrParticoes;
    Matriz *M_part = (Matriz *)malloc(nrParticoes * sizeof(Matriz));
    int part_i, i, ii = 0, j;
    for (part_i = 0; part_i < nrParticoes; part_i++)
    {
        //caso seja a ultima particao e ela tiver resto precisa ajustar a quantidade de linhas
        if (resto && (part_i + 1) == nrParticoes)
        {
            //printf("ajustando nr linhas da ultima particao de %d para %d\n", tamanho_particao, tamanho_particao + resto);
            tamanho_particao = tamanho_particao + resto;
        }
        M_part[part_i].m = tamanho_particao;
        M_part[part_i].n = colunas;
        matriz_alocar(&M_part[part_i]);
        //M_part[part_i].matriz = matriz_alocar(M_part[part_i].m, M_part[part_i].n);
        for (i = 0; i < tamanho_particao; i++, ii++)
        {
            for (j = 0; j < colunas; j++)
            {
                //printf("M_part[%d].matriz[%d][%d]=A.matriz[%d][%d] -- %d;\n", part_i, i, j, ii, j, M.matriz[ii][j]);
                M_part[part_i].matriz[i][j] = M.matriz[ii][j];
            }
        }
    }

    return M_part;
}

/**
 * Faz o particionamento verticais de uma matriz
 * @param M - Matriz M
 * @param nrParticoes - número de partições verticais de M
 * @return M_part[nrParticoes] - retorna vetor de partições de M
 * */
Matriz *particiona_matriz_vertical(Matriz M, int nrParticoes)
{
    if (nrParticoes > M.n)
    {
        printf("O numero de particoes nao pode ser maior que a quantidade colunas matriz A, ou a quantidade de linhas de B.\n");
        return NULL;
    }
    int linhas = M.m;
    int colunas = M.n;
    int resto = colunas % nrParticoes;
    int tamanho_particao = (colunas - resto) / nrParticoes;
    //printf("\n\nParticionamento Vertical\n\nA %dx%d\nnrParticoes %d\ntam_particao %d\nresto %d\n", linhas, colunas, nrParticoes, tamanho_particao, resto);
    Matriz *M_part = (Matriz *)malloc(nrParticoes * sizeof(Matriz));

    int part_i, i, jj = 0, j;
    for (part_i = 0; part_i < nrParticoes; part_i++)
    {
        //caso seja a ultima particao e ela tiver resto precisa ajustar a quantidade de linhas
        if (resto && (part_i + 1) == nrParticoes)
        {
            //printf("ajustando nr colunas da ultima particao de %d para %d\n", tamanho_particao, tamanho_particao + resto);
            tamanho_particao = tamanho_particao + resto;
        }
        M_part[part_i].m = linhas;
        M_part[part_i].n = tamanho_particao;
        matriz_alocar(&M_part[part_i]);
        //M_part[part_i].matriz = matriz_alocar(M_part[part_i].m, M_part[part_i].n);
        for (j = 0; j < tamanho_particao; j++, jj++)
        {
            for (i = 0; i < linhas; i++)
            {
                //printf("%d",M.matriz[i][j]);
                //printf("M_part[%d].matriz[%d][%d]=A.matriz[%d][%d] -- %d;\n", part_i, i, j, i, jj, M.matriz[i][jj]);
                M_part[part_i].matriz[i][j] = M.matriz[i][jj];
            }
        }
    }
    return M_part;
}

/**
 * Recebe vetores contendo partições de A e B
 * 
 * */
void imprimir_particoes(Matriz *A_parts, Matriz *B_parts, Matriz A, Matriz B, int nrParticoes)
{
    if (A.m > 10 || B.n > 10)
    {
        return;
    }
    printf("\n\nParticoes verticais de A\n");
    for (int i = 0; i < A.n; i++)
    {
        printf("-----------------");
    }
    printf("\n");

    for (int i = 0; i < A_parts[0].m; i++)
    {

        for (int j = 0; j < nrParticoes; j++)
        {
            printf("  |");
            for (int k = 0; k < A_parts[j].n; k++)
            {
                printf("\t%d\t", A_parts[j].matriz[i][k]);
            }
        }
        printf("|\n");
    }
    for (int i = 0; i < A.n; i++)
    {
        printf("-----------------");
    }

    printf("\n\nParticoes horizontais de B\n");
    printf("--------------------------------------------------------------\n");

    for (int k = 0; k < nrParticoes; k++)
    {
        matriz_print(B_parts[k]);
        printf("    ");
        for (int j = 0; j < B.n; j++)
        {

            printf("--------");
        }
        printf("\n");
    }
}
/**
 * Recebe matriz A e B, particiona as matrizes conforme nrParticoes realiza multipĺicação e soma os blocos em uma matriz C
 * C = sum(A_part * B_part)
 * */
Matriz *matriz_bloco_multiplicar(Matriz A, Matriz B, int nrParticoes)
{
    if (A.n != B.m)
    {
        printf("Matrizes incompatíveis para multiplicação!\n");
        return NULL;
    }

    /**
      A 4x5    B 5x4
          ^      ^      
    **/

    Matriz *C = (Matriz *)malloc(sizeof(Matriz));
    C->m = A.m;
    C->n = B.n;
    matriz_alocar(C);
    //C.matriz = matriz_alocar(C.m, C.n);
    Matriz *A_parts; //contém todas as submatrizes de A
    Matriz *B_parts; //contém todas as submatrizes de B
    A_parts = particiona_matriz_vertical(A, nrParticoes);
    B_parts = particiona_matriz_horizontal(B, nrParticoes);
    //imprimir_particoes(A_parts, B_parts, A, B, nrParticoes);

    // Agora basta fazer a multiplicação bloco por bloco
    //  C[0]=A[0]*B[0]
    //  Depois somar todas as partições de C[] ----> C=C[0]+C[1]+...+C[n]
    Matriz *C_parts = (Matriz *)malloc(nrParticoes * sizeof(Matriz)); //Vetor para as várias partições de A*B
    for (int i = 0; i < nrParticoes; i++)
    {

        C_parts[i].m = A_parts[i].m;
        C_parts[i].n = B_parts[i].n;
        matriz_alocar(&C_parts[i]);
        //Cada partição de C recebe as respectivas multiplicações de partições A e B
        C_parts[i] = matriz_multiplicar(A_parts[i], B_parts[i]);
    }

    for (int i = 0; i < nrParticoes; i++)
    {
        printf("C_parts[%d]\n", i);
        matriz_print_2(&C_parts[i]);
    }
    for (int i = 0; i < C->m; i++)
    {
        for (int j = 0; j < C->n; j++)
        {
            for (int k = 0; k < nrParticoes; k++)
            {
                C->matriz[i][j] += C_parts[k].matriz[i][j];
            }
        }
    }
    return C;
}

/**
 * Recebe a referência de duas matrizes e as compara.
 * */
int matriz_comparar(Matriz *A, Matriz *B)
{
    if (A->m != B->m)
    {
        printf("Matrizes diferente!\n");
        return 1;
    }
    if (A->n != B->n)
    {
        printf("Matrizes diferente!\n");
        return 1;
    }
    for (int i = 0; i < A->m; i++)
    {
        for (int j = 0; j < A->n; j++)
        {
            if (A->matriz[i][j] != B->matriz[i][j])
            {
                printf("Matrizes diferente!\n");
                return 1;
            }
        }
    }
    printf("Matrizes identicas!\n");
    return 0;
}