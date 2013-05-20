#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/sysinfo.h>
#include "histogram.h"
int main() {
  int i, ramUsed;
  char gnuplotCmd[250], systemCmd[350];
  FILE *outPtr = 0;
  char fileName[50];
  sprintf(fileName,"data.txt"); /* The name of the output file. */
  struct sysinfo info; /* A sysinfo struct to hold the status. */
  outPtr = fopen(fileName,"w"); /* Open the output file. */
  if(!outPtr) return 1; /* If the output file cannot be opened return error */
  Histogram h;
  initHist(&h,10,0.,10.); 
  for(i=0;i<60;i++) {
    sysinfo(&info);  /* Get the system information */
    ramUsed = info.totalram - info.freeram;
    fprintf(outPtr,"%d %d\n", i, ramUsed); /* Write the ram used. */
    fillHist(&h, ramUsed,1.0); /* Histogram each value. */ 
    usleep(500000); /* Sleep for 1/2 a second. */
  }
  fclose(outPtr); /* Close the output file. */ 
 
  printf("Mean=%f\n",histMean(&h)); /* Mean value. */
  printf("StdDev=%f\n",histStdDev(&h)); /* Standard deviation. */
  saveHist(&h,"Hist.txt"); /* Save the histogram. */
 
  /* Now plot the data */
  sprintf(gnuplotCmd, "plot \'%s\'\n", fileName); /* Build the plot command. */
  
  /* Create the full command, including the pipe to gnuplot */
  sprintf(systemCmd,"echo \"%s\" | gnuplot --persist",gnuplotCmd);
  
  system(systemCmd); /* Execute the system command. */
  return 0; /* Return success to the system. */
}
