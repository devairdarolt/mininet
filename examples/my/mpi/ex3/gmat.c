#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tools.h"
//#include "matriz.h"

int mgerar(Matriz *matriz, int valor);

int main(int argc, char **argv) {
	FILE *fmat0, *fmat1;
	Matriz mma0,mma1;
	int linha, coluna;
	char filename [100];
	int *vet_line = NULL;
	

	if (argc != 3){
		printf ("ERRO: Numero de parametros %s <nr_linhas> <nr_colunas>", argv[0]);
		exit (1);
	}

	linha =  atoi(argv[1]);
	coluna = atoi(argv[2]);
	sprintf (filename, "%dx%d-mat.map", linha, coluna);

	fmat0 = fopen(filename,"w");
  if (fmat0 == NULL) {
		puts("Error: Na abertura dos arquivos.");
		exit(1);
  }

	mma0.matriz = NULL;
	mma0.m = linha;
	mma0.n = coluna;
	
	/**if (matriz_alocar(&mma0)) {	//
	// printf("##### Arquivo %dx%d-mat.map: VERIFICADO! #####\n", linha, coluna);

		puts("ERROR: Out of memory.");
	}*/
	
	matriz_alocar(&mma0);
	mgerar(&mma0, -9999);
	matriz_print_2(&mma0);
	

	printf("\t\t**** PRINT mat_c NxM(%d,%d) **** \n", linha, coluna);
	fileout_matriz(&mma0, fmat0);	
	matriz_desalocar(mma0.m,mma0.n,mma0.matriz);
	printf("#####\n Arquivo com a matriz gerada (%dx%d-mat.map).\n#####\n", linha, coluna);
	fclose(fmat0);

	fmat1 = fopen(filename,"r");
	if (fmat1 == NULL) {
		puts("Error: Na abertura dos arquivos.");
		exit(1);
	}
	
	mma1 = *leMatriz(filename);
	printf("Testado!\n");
	matriz_print_2(&mma1);	
	matriz_desalocar(mma1.m,mma1.n,mma1.matriz);
	
	
	free(vet_line);
	
  	fclose(fmat1);
	printf("##### Arquivo %dx%d-mat.map: VERIFICADO! #####\n", linha, coluna);
  return 0;
}
// Popular uma matriz ja criada
int mgerar(Matriz *matriz, int valor){
	srand( (unsigned)time(NULL) );

	for (int i=0; i < matriz->m; i++){
		for (int j=0; j < matriz->n; j++){
			if (valor == -9999) matriz->matriz[i][j] = rand() % 10;
			else matriz->matriz[i][j] = valor;
		}
	}

	return 0;
}