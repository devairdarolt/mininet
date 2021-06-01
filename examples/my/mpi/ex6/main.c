// Author: Wes Kendall
// Copyright 2011 www.mpitutorial.com
// This code is provided freely with the tutorials on mpitutorial.com. Feel
// free to modify it for your own use. Any distribution of the code must
// either provide a link to www.mpitutorial.com or keep this header intact.
//
// MPI_Send, MPI_Recv example. Communicates the number -1 from process 0
// to process 1.
//
#include <mpi.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
    // Initialize the MPI environment
    MPI_Init(NULL, NULL);
    // Find out rank, size
    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    // We are assuming at least 2 processes for this task
    if (world_size < 2)
    {
        fprintf(stderr, "World size must be greater than 1 for %s\n", argv[0]);
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    int number;
    if (world_rank == 0)
    {
        printf("world_size %d\n", world_size);
        
        system("ip route");
        system(" pwd");

        // If we are rank 0, set the number to -1 and send it to process 1
        number = -1;

        for (int i = 1; i < world_size; i++)
        {
            number = rand() % 10;
            printf("Master send %d to slave %d\n", number, i);
            MPI_Send(
                /* data         = */ &number,
                /* count        = */ 1,
                /* datatype     = */ MPI_INT,
                /* destination  = */ i,
                /* tag          = */ 0,
                /* communicator = */ MPI_COMM_WORLD);
        }
    }
    else
    {
        
        system("ip route");
        system(" pwd");
        MPI_Recv(
            /* data         = */ &number,
            /* count        = */ 1,
            /* datatype     = */ MPI_INT,
            /* source       = */ 0,
            /* tag          = */ 0,
            /* communicator = */ MPI_COMM_WORLD,
            /* status       = */ MPI_STATUS_IGNORE);
        printf("Slave %d received number %d from master 0\n",world_rank, number);
    }
    MPI_Barrier(MPI_COMM_WORLD);
    if (world_rank == 0)
    {
        printf("Done!\n");
    }

    MPI_Finalize();
}