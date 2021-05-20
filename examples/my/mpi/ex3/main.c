#include <time.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <mpi.h>
#include <string.h>

#include "tools.h"
#define TAG 0
#define MASTER 0 // Indentificador do processo master

// Funções para auxiliar debbuger do código
void print_red()
{
    printf("\033[0;31m");
}
void print_green()
{
    printf("\033[0;32m");
}
void print_blue()
{
    printf("\033[0;34m");
}
void print_reset()
{
    printf("\e[m");
}

/**
 * Função que envia uma matriz[i][j] para processo destino
 * 
 * @param m - Matriz *m, ponteiro para uma matriz que será enviada
 * @param dest  - int dest, id do processo destino que esta esperando um receive
 * 
 * @return time (segundos)-- Retorna o tempo de envio da matriz m
*/
double MPI__sender_matrix(Matriz *m, int dest)
{
    double inicio = wtime();
    int send_buffer; // = (int *)malloc(sizeof(int));
    //ENVIA O CABEÇALHO
    send_buffer = m->m;
    MPI_Send(&send_buffer, 1, MPI_INT, dest, TAG, MPI_COMM_WORLD); //Envia configuração da particao

    send_buffer = m->n;
    MPI_Send(&send_buffer, 1, MPI_INT, dest, TAG, MPI_COMM_WORLD); //Envia configuração da particao

    //ENVIA O CONTEUDO DA MATRIZ
    for (int i = 0; i < m->m; i++)
    {
        for (int j = 0; j < m->n; j++)
        {
            send_buffer = m->matriz[i][j];
            MPI_Send(&send_buffer, 1, MPI_INT, dest, TAG, MPI_COMM_WORLD); //Envia configuração da particao
        }
    }
    double fim = wtime();

    return fim - inicio;
}
/**
 * Função que recebe uma matriz[i][j] de um determinado processo source
 * @param m - Matriz *m, matriz que receberá os dados do receiver
 * @param source - id do processo que deve ser escutado 
 * 
 * @return time (segundos)-- Retorna o tempo levado para receber matriz m
*/
double MPI__receiver_matrix(Matriz *m, int source)
{
    double inicio = wtime();
    MPI_Status status;
    int receiv_buffer;

    //RECEBE O CABEÇALHO {Matriz.m, Matriz.n}
    MPI_Recv(&receiv_buffer, 1, MPI_INT, source, TAG, MPI_COMM_WORLD, &status);
    m->m = (int)receiv_buffer;

    MPI_Recv(&receiv_buffer, 1, MPI_INT, source, TAG, MPI_COMM_WORLD, &status);
    m->n = (int)receiv_buffer;

    matriz_alocar(m);
    if (m->matriz == NULL)
    {
        printf("ERRO: Não foi alocado matriz %dx%d\n", m->m, m->n);
        exit(0);
    }
    //RECEBE O CONTEUDO DA MATRIZ
    for (int i = 0; i < m->m; i++)
    {
        for (int j = 0; j < m->n; j++)
        {
            receiv_buffer = 0;
            MPI_Recv(&receiv_buffer, 1, MPI_INT, source, TAG, MPI_COMM_WORLD, &status);
            m->matriz[i][j] = receiv_buffer;
        }
    }
    double fim = wtime();

    return (fim - inicio);
}
/**
 * Função que envia tempo de processamento de um processo slave para o master
 * @param time - tempo de execução do processo
 * @param dest - id do processo destino
 * */
void MPI__sender_time_process(double time, int dest)
{
    double send_buffer = time;                                        // = (int *)malloc(sizeof(int));
    MPI_Send(&send_buffer, 1, MPI_DOUBLE, dest, TAG, MPI_COMM_WORLD); //Envia configuração da particao
}
/**
 * Função que recebe o tempo de um processo
 * @param source - id do processo da qual deseja se obter o tempo de execução
 * @return time
 * */
double MPI__receiv_time_process(int source)
{
    MPI_Status status;
    double receiv_buffer;
    MPI_Recv(&receiv_buffer, 1, MPI_DOUBLE, source, TAG, MPI_COMM_WORLD, &status);

    return receiv_buffer;
}
/**
 * 
 * @param argc - quantidade de argumentos enviados pelo terminal
 * @param *argv[] - vetor de parâmetros
 * 
 * */
int main(int argc, char *argv[])
{
    MPI_Init(&argc, &argv);
    int nrParticoes = 1;
    int rank, size;

    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    if (rank == MASTER)
    {
        //BASICAMENTE O MASTER IRÁ PARTICIONAR AS MATRIZES E PASSAR PARA CADA SLEVE CALCULAR A MULTIPLICAÇÃO.
        print_reset(), printf("\n\n\n[PROCESSO - %2d (MASTER)]\n", rank), print_reset();
        //Carrega as matrizes dos arquivos para a memória
        if (argc != 4)
        {
            print_reset(), printf("Qtd. parametros invalidos!...\n mpirun -hostfile hostfile -np $(NR_TOTAL_PROCESSOS) executavel $(MATRIZ_A) $(MATRIZ_B) $(NR_PARTICOES)\n"), print_reset();
            return 0;
        }
        if (!argv[4])
        {
            nrParticoes = (int)atoi(argv[3]);
            if (nrParticoes > (size - 1))
            {
                printf("O numero de particoes (%d) deve ser igual o número de processos slaves (%d).\n", nrParticoes, size - 1);
                MPI_Abort(MPI_COMM_WORLD, MPI_ERR_UNSUPPORTED_DATAREP);
                exit(0);
            }
        }
        print_reset(), printf("nrParticoes[%d]\n", nrParticoes);
        printf("nrSlaves[%d]\n", size - 1);
        printf("---------------------------------------------------- Matriz A ------------------------------------------------------\n"), print_reset();
        Matriz *A;
        A = leMatriz(argv[1]);
        matriz_print_2(A);

        print_reset(), printf("---------------------------------------------------- Matriz B ------------------------------------------------------\n"), print_reset();

        Matriz *B;
        B = leMatriz(argv[2]);
        matriz_print_2(B);

        if (A->n != B->m)
        {
            printf("Imcompativel para multiplicacao\n");
            exit(1);
        }
        print_reset(), printf("---------------------------------------------- A x B sequencial ---------------------------------------------------\n");
        double time_ini_seq = wtime();
        Matriz C_seq = matriz_multiplicar(*A, *B);
        double time_fim_seq = wtime();
        double total_time_seq = time_fim_seq - time_ini_seq;

        //print_reset(), matriz_print_2(&C_seq), print_reset();
        /////////////////////////////////////////////////// MULTIPLICAÇÃO EM BLOCO MPI    /////////////////////////////////////////////////////////////
        print_red(), printf("[PROCESSO - 0 (MASTER)] - Particionando Matrizes...\n"), print_reset();
        Matriz *A_parts;
        A_parts = particiona_matriz_vertical(*A, nrParticoes);

        Matriz *B_parts;
        B_parts = particiona_matriz_horizontal(*B, nrParticoes);

        //Agora que ja particionamos não precisamos mais de A e B
        matriz_desalocar(A->m, A->n, A->matriz);
        matriz_desalocar(B->m, B->n, B->matriz);

        MPI_Barrier(MPI_COMM_WORLD); //Faz com que os slaves esperem até que todas as partições sejam criadas
        int part_id = 0;
        double total_tempo_trafego = 0.0;
        double ini_process = wtime();   
        for (int slave_id = 1; slave_id < size; slave_id++, part_id++)
        {
            total_tempo_trafego += MPI__sender_matrix(&A_parts[part_id], slave_id);
            total_tempo_trafego += MPI__sender_matrix(&B_parts[part_id], slave_id);
        }
        
        //Libera as partições da memória pois não são mais uteis
        for (int i = 0; i < nrParticoes; i++)
        {
            matriz_desalocar(A_parts[i].m, A_parts[i].n, A_parts[i].matriz);
            matriz_desalocar(B_parts[i].m, B_parts[i].n, B_parts[i].matriz);
        }
        free(A_parts);
        free(B_parts);        
        double media_tempo_process = 0.0;
        double total_tempo_soma = 0.0;
        Matriz *C_parts_i=(Matriz *)malloc(sizeof(Matriz));
        Matriz *C=(Matriz *)malloc(sizeof(Matriz));
        
        C->m = A->m;
        C->n = B->n;
        matriz_alocar(C);
        for (int slave_id = 1, part_id = 0; slave_id < size; slave_id++, part_id++)
        {
            total_tempo_trafego += MPI__receiver_matrix(C_parts_i, slave_id);
            media_tempo_process += MPI__receiv_time_process(slave_id);
            //*C_parts_i = C_parts[part_id];
            
            //Soma: C = C_parts[0] + C_parts[1] + C_parts[2] + ... + C_parts[nrParticoes]
            // C += C_part_i
            double ini_soma = wtime();
            for(int i=0;i<C_parts_i->m;i++){
                for(int j=0;j<C_parts_i->n;j++){
                    C->matriz[i][j]+=C_parts_i->matriz[i][j];
                }

            }
            double fim_soma = wtime();
            total_tempo_soma = total_tempo_soma + (fim_soma-ini_soma);
        }
        matriz_desalocar(C_parts_i->m,C_parts_i->n,C_parts_i->matriz);
        free(C_parts_i);
        double fim_process = wtime();        
        print_red(), printf("[PROCESSO - 0 (MASTER)] - Total total para enviar e receber matrizes: [%9f] (segundos)...\n", total_tempo_trafego), print_reset();
        print_red(), printf("[PROCESSO - 0 (MASTER)] - Templo médio de processamento/slaves: [%9f] (segundos)...\n", media_tempo_process/(size-1)), print_reset();        
        print_red(), printf("[PROCESSO - 0 (MASTER)] - Tempo de soma dos blocos: [%9f] (segundos)...\n\n", total_tempo_soma), print_reset();
        print_red(), printf("[PROCESSO - 0 (MASTER)] - Tempo de solução com blocos MPI: [%9f] (segundos)...\n", fim_process-ini_process), print_reset();
        print_green(), printf("[PROCESSO - 0 (MASTER)] - Tempo de solução sequencial sem bloco: [%9f] (segundos)...\n\n\n", total_time_seq), print_reset();
        print_green(), matriz_comparar(&C_seq,C),print_reset();
        
        matriz_desalocar(C->m, C->n, C->matriz);
        free(C);
    }
    else
    {
        MPI_Barrier(MPI_COMM_WORLD); //Faz com que os slaves esperem até que o master finalize a organização do trabalho

        Matriz *A_part_i = (Matriz *)malloc(sizeof(Matriz));
        Matriz *B_part_i = (Matriz *)malloc(sizeof(Matriz));
        Matriz *C_part_i = (Matriz *)malloc(sizeof(Matriz));
        double time_comunic = 0.0;        
        time_comunic += MPI__receiver_matrix(A_part_i, 0); //recebe A_part_i do master
        time_comunic += MPI__receiver_matrix(B_part_i, 0); //recebe B_part_i do master
        print_blue(), printf("[PROCESSO - %2d (SLAVE)] - Calculando particao C_part[%d]=A_part[%d] x B_part[%d]\n", rank, rank - 1, rank - 1, rank - 1), print_reset();
        print_blue(), printf("[PROCESSO - %2d (SLAVE)] - Tempo de trafego de recebimento %9f(segundos)\n", rank, time_comunic), print_reset();

        //sleep(rank);

        double time_inicio_process = wtime();
        *C_part_i = matriz_multiplicar(*A_part_i, *B_part_i);
        double time_fim_process = wtime();
        double time_process = time_fim_process - time_inicio_process;
        print_blue(), printf("[PROCESSO - %2d (SLAVE)] - Tempo de processamento %9f\n", rank, time_process), print_reset();

        MPI__sender_matrix(C_part_i, MASTER); //devolve o resultado para o MASTER -

        //ENVIA O TEMPO
        MPI__sender_time_process(time_process, MASTER);

        //Libera espaço alocado na memória
        matriz_desalocar(A_part_i->m, A_part_i->n, A_part_i->matriz);
        free(A_part_i);
        matriz_desalocar(B_part_i->m, B_part_i->n, B_part_i->matriz);
        free(B_part_i);
        matriz_desalocar(C_part_i->m, C_part_i->n, C_part_i->matriz);
        free(C_part_i);
    }

    MPI_Finalize();

    return 0;
}
