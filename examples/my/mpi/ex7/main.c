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
#include <unistd.h>

int main(int argc, char **argv)
{

    MPI_Init(NULL, NULL);
    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);


    int number;
    //Download 1 hop distance
    /*switch (world_rank+1) {
      case 1: // master
        system("iperf -s > h001s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD); //1
        printf("Servers started\n" );
        printf("h001 download from h002\n" );
        system("iperf -c 10.0.0.2 > h001c.log");//start server iperf on master
        printf("h001 download finished\n" );
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 2: // slave1
        system("iperf -s > h002s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 3: // slave1
        system("iperf -s > h003s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        printf("h003 download from h004\n" );
        system("iperf -c 10.0.0.4 > h003c.log");//start server iperf on master
        printf("h003 download finished\n" );
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 4: // slave1
        system("iperf -s > h004s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 5: // slave1
        system("iperf -s > h005s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        printf("h005 download from h006\n" );
        system("iperf -c 10.0.0.6 > h005c.log");//start server iperf on master
        printf("h005 download finished\n" );
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 6: // slave1
        system("iperf -s > h006s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 7: // slave1
        system("iperf -s > h007s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        printf("h007 download from h008\n" );
        system("iperf -c 10.0.0.8 > h007c.log");//start server iperf on master
        printf("h007 download finished\n" );
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 8: // slave1
        system("iperf -s > h008s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 9: // slave1
        system("iperf -s > h009s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        printf("h009 download from h010\n" );
        system("iperf -c 10.0.0.10 > h009c.log");//start server iperf on master
        printf("h010 download finished\n" );
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 10: // slave1
        system("iperf -s > h010s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 11: // slave1
        system("iperf -s > h011s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        printf("h011 download from h012\n" );
        system("iperf -c 10.0.0.12 > h011c.log");//start server iperf on master
        printf("h011 download finished\n" );
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 12: // slave1
        system("iperf -s > h012s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 13: // slave1
        system("iperf -s > h013s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        printf("h013 download from h014\n" );
        system("iperf -c 10.0.0.14 > h013c.log");//start server iperf on master
        printf("h013 download finished\n" );
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 14: // slave1
        system("iperf -s > h014s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 15: // slave1
        system("iperf -s > h015s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        printf("h015 download from h016\n" );
        system("iperf -c 10.0.0.16 > h015c.log");//start server iperf on master
        printf("h015 download finished\n" );
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 16: // slave1
        system("iperf -s > h016s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;

    }
    MPI_Barrier(MPI_COMM_WORLD);// init teste 2
    */

    MPI_Barrier(MPI_COMM_WORLD);

    switch (world_rank+1) {
      case 1: // master
        system("iperf -s > h001s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD); //1
        sleep(2*(world_rank-1));//1
        printf("h001 download from h003\n" );
        system("iperf -c 10.0.0.3 -t 60 -i 5 -e > h001c.log");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 2: // slave1
        system("iperf -s > h002s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        sleep(2*(world_rank-1)); //3
        printf("h002 download from h004\n" );
        system("iperf -c 10.0.0.4 -t 60 -i 5 -e > h002c.log");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 3: // slave1
        system("iperf -s > h003s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 4: // slave1
        system("iperf -s > h004s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 5: // slave1
        system("iperf -s > h005s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        sleep(2*(world_rank-1));
        printf("h005 download from h007\n" );
        system("iperf -c 10.0.0.7 -t 60 -i 5 -e > h005c.log");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 6: // slave1
        system("iperf -s > h006s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        sleep(2*(world_rank-1));
        printf("h006 download from h008\n" );
        system("iperf -c 10.0.0.8 -t 60 -i 5 -e > h006c.log");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 7: // slave1
        system("iperf -s > h007s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 8: // slave1
        system("iperf -s > h008s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 9: // slave1
        system("iperf -s > h009s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        sleep(2*(world_rank-1));
        printf("h009 download from h011\n" );
        system("iperf -c 10.0.0.11 -t 60 -i 5 -e > h009c.log");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 10: // slave1
        system("iperf -s > h010s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        sleep(2*(world_rank-1));
        printf("h010 download from h012\n" );
        system("iperf -c 10.0.0.12 -t 60 -i 5 -e > h010c.log");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 11: // slave1
        system("iperf -s > h011s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 12: // slave1
        system("iperf -s > h012s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 13: // slave1
        system("iperf -s > h013s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        sleep(2*(world_rank-1));
        printf("h013 download from h015\n" );
        system("iperf -c 10.0.0.15 -t 60 -i 5 -e > h013c.log");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 14: // slave1
        system("iperf -s > h014s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        sleep(2*(world_rank-1));
        printf("h014 download from h016\n" );
        system("iperf -c 10.0.0.16 -t 60 -i 5 -e > h014c.log");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 15: // slave1
        system("iperf -s > h015s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;
      case 16: // slave1
        system("iperf -s > h016s.log &");//start server iperf on master
        MPI_Barrier(MPI_COMM_WORLD);//1
        MPI_Barrier(MPI_COMM_WORLD);//2
        break;

    }


    //sleep(60);
    //MPI_Barrier(MPI_COMM_WORLD);
    if (world_rank == 0)
    {
        printf("\nkill process" );
        system("sudo kill -9 $(pgrep -f iperf)");
        printf("Done!\n");
    }

    MPI_Finalize();
}
