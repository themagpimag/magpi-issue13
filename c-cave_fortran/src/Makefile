# W. H. Bell
# A Makefile to build Wrap.exe

CC=gcc
F77=gfortran
TARGET=Wrap
OBJECTS=main.o fortran.o 

LIBS = -lgfortran

$(TARGET).exe: $(OBJECTS)
	@echo "**"
	@echo "** Linking Executable"
	@echo "**"
	$(CC) $(OBJECTS) $(LIBS) -o $(TARGET).exe

clean:
	@rm -f *.o *~

veryclean: clean
	@rm $(TARGET).exe

%.o: %.c
	@echo "**"
	@echo "** Compiling C Source" 
	@echo "**"
	$(CC) -c $(INCFLAGS) $< 

%.o: %.for
	@echo "**"
	@echo "** Compiling Fortran Source"
	@echo "**"
	$(F77) -c -m64 $<
