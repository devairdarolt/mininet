#include <time.h>
#include <stdio.h>
#include <stdlib.h>
//#include <process.h>
#include <unistd.h>

int main(int argc, char const **argv) {

  printf("\n\nINICIO\n");
  //(char*)0
  //execl("/bin/ping","ping", "-c5", "google.com",NULL);
  system("iperf -s >> log &");

  printf("\n\nFIM\n");
  return 0;
}
