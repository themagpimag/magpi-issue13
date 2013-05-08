/* W. H. Bell
** A program to demonstrate fortran wrappers.
*/

#include <stdio.h>

#include "fortran.h"

void fill_common(void);

int main() {
  float a=3.14159;
  char name[]="Wrapper";
  int size;

  /* Fill common block FORCOM */
  fill_common();

  /* Print values contained in common block */
  commons_();

  /* Call the fortran function CALL_BACK(A,NAME) */
  size=sizeof(name)/sizeof(char);
  call_back__(&a,name,size);

  return 0;
}

/* A function to fill the FORTRAN common block. */
void fill_common(void) {
  int i,j;

  for(i=1;i<=2;i++) {
    for(j=1;j<=3;j++) {
      /* Fill the int array */
      forcom_.intarray[i-1][j-1] = i+j*10;

      /* Fill the float array */
      forcom_.realarray[j-1][i-1] = j+(float)i*0.001;
    }
  }
  /* Fill the character array */
  sprintf(forcom_.somestring,"C string");
}

/* A function provided for the FORTRAN function CALL_BACK to call. */
float mult_a__(float *a) {
  return (*a)*10.;
}
