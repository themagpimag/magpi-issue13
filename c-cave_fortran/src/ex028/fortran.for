c     W. H. Bell
c     A fortran subroutine and function to demonstrate the
c     principle of wrapping.
c

c     A subrountine to print the values stored in the common block 
c     commons
      SUBROUTINE COMMONS
      IMPLICIT NONE
      INCLUDE 'FORTRAN.INC'

      INTEGER I,J

c     Print the contents of the INTEGER array.
      DO I=1,3
         DO J=1,2
            PRINT *,'COMMONS/INTARRAY(',I,',',J,')=',INTARRAY(I,J)
         ENDDO
      ENDDO

c     Print the contents of the REAL array.
      DO I=1,2
         DO J=1,3
            PRINT *,'COMMONS/REALARRAY(',I,',',J,')=',REALARRAY(I,J)
         ENDDO
      ENDDO

c     Print the string.
      PRINT *,'SOMESTRING=',SOMESTRING
      
      RETURN
      END


c     A function to print a string and multiply a number by calling 
c     a C function 
      FUNCTION CALL_BACK(A,NAME)
      IMPLICIT NONE
      REAL A, C, CALL_BACK, MULT_A
      CHARACTER*(*) NAME

c     Print the string passed into this function
      PRINT *,'CALL_BACK() NAME=',NAME

c     Call a C function mult_a_ to multiply A by some factor
      C = MULT_A(A)

c     Print the value of C returned from mult_a_
      PRINT *,'CALL_BACK() C=',C

c     Return the value of C.
      CALL_BACK = C
      RETURN
      END
