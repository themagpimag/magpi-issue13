/* W. H. Bell
** A C header file containing declarations of a fortran subroutine and
** function
*/

#ifndef FORTRAN_H
#define FORTRAN_H

/* The C side of the fortran common block definition. */
typedef struct {
  int intarray[2][3];
  float realarray[3][2];
  char somestring[50];
} forcom;

/* The memory is allocated by the fortran code.  Therefore used extern
   here to cause forcom_ to be resolved to the FORTRAN code at link
   time. */ 
extern forcom forcom_;

/* Fortran subroutine COMMONS */
void commons_(void);

/* Fortran function CALL_BACK */
float call_back_(float *,char *, int);

/* A function called from fortran code */
float mult_a_(float *);

#endif
