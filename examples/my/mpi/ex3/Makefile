# GNU Makefile

GCC = gcc
MPICC = mpicc 
CCFLAGS = -Wall -O3
LDFLAGS = #-llmpe -lmpe
TARGET = cls clean gmat compile

NR_TOTAL_PROCESSOS=3 	# O numero total de processos (MASTER + SLAVES)
NR_PARTICOES = 2	# Número de partições deve ser igual o número de slaves


MATRIZ_A = 4x4-mat.map #nome do arquivo da matriz A
MATRIZ_B = 4x4-mat.map #nome do arquivo da matriz B
all: $(TARGET)
	

%.o: %.c
	$(CC) $(CCFLAGS) -c $<
	echo "export OMP_NUM_THREADS=4

%: %.o
	$(CC) $(LDFLAGS) $^ -o $@ 

cls:
	clear

compile: 
		$(MPICC) $(CCFLAGS) main.c matriz.c tools.c $(LDFLAGS) -o  executavel

gmat:
	$(GCC) $(CCFLAGS) gmat.c matriz.c tools.c -o  gmat
run:
	mpirun --hostfile hostfile -np $(NR_TOTAL_PROCESSOS) executavel $(MATRIZ_A) $(MATRIZ_B) $(NR_PARTICOES)
	
clean:
	rm -f *.o *~ $(TARGET) executavel gmat
