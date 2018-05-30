CC      = gcc
CFLAGS  = -Wall -std=c99 `pkg-config --cflags python-3.4` 
CFLAGS  += -fPIC
LDFLAGS = `pkg-config --libs python-3.4`

all: audioInterop.so copy copy1

audioInterop.so: main.o
	$(CC) -shared $(LDFLAGS) $^ -o $@ -L -lbcm2835

copy:
	sudo cp audioInterop.so /usr/local/lib
copy1:
	sudo cp audioInterop.so /usr/local/lib/python3.4/dist-packages

clean:
	rm *.o