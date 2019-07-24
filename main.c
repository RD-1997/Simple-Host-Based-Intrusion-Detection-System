#include <stdio.h>
#include <dirent.h>
#include <stdlib.h>
#include <windows.h> // Works on Windows OS.
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdio.h>
#include <time.h>
#include <string.h>
#include <direct.h>
#include <winsock2.h>
#include <ws2tcpip.h>

#pragma comment(lib, "ws2_32.lib") //library winsock

/* ####################################
 * Refers to the sub functions
 * ####################################*/

void giveUnnecessaryMessage();
int countDown(int);
void list_files();
void start_winsock();
void create_socket();
void socket_send(char *);


/* global variables */
char directory[] = {"C:/Users/test/Downloads/test/"};
int counter, i = 0, j = 0, k = 0, l = 254, n = 0;
char *filesList[254];// gives error when you use variables
SOCKET s;
struct sockaddr_in server;

char *makeonstring(size_t size, char *array[size], const char *joint){
    size_t jlen, lens[size];
    size_t i, total_size = (size-1) * (jlen=strlen(joint)) + 1;
    char *result, *p;


    for(i=0;i<size;++i){
        total_size += (lens[i]=strlen(array[i]));
    }
    p = result = malloc(total_size);
    for(i=0;i<size;++i){
        memcpy(p, array[i], lens[i]);
        p += lens[i];
        if(i<size-1){
            memcpy(p, joint, jlen);
            p += jlen;
        }
    }
    *p = '\0';
    return result;
}

int main() {
    giveUnnecessaryMessage();
    start_winsock();
    create_socket();
    printf("Enter in seconds a value ot repeat the program\n");
    scanf("%d",&counter); // scan the answer and put in counter
    //loop
    countDown(counter); // use answer counter in function
    list_files(); //update array
    char *cat = makeonstring(i, filesList, ";");
    puts(cat);
    socket_send(cat);

    return 0;
}
/* function for counting down */
int countDown(int a)
{
    while (a != 0) // loop for counter.
    {
        printf("\n%d before scanning again..", a);
        sleep(1);
        a--;
    }
    printf("\nTimer has been expired..\n");
}
/* return array */
void list_files()
{
    DIR *d;
    struct dirent *dir;
    d = opendir(directory);
    //Put file names into the array
    while((dir = readdir(d)) != NULL) {
        if ( ( i < 254) && ! ( strcmp(dir->d_name, ".") == 0 || strcmp(dir->d_name, "..") == 0))
        {
            filesList[i] = malloc( strlen ( dir->d_name) + 1); // allocate memory
            strcpy(filesList[i], dir->d_name); // put file names in to array
            i++; // do +1 to read each single array line
        }
    }
//    for(n = 0; n < i;n++){
//        printf("%s\n", filesList[n]);
//    }
//    for(n = 0; n < i;n++){
//        free ( filesList[n]);
//    }
}
void start_winsock()
{
    WSADATA wsa;
    printf("\nInitializing Winsock..");
    if (WSAStartup(MAKEWORD(2,2),&wsa) != 0)
    {
        printf("Failed to start. Error Code: %d", WSAGetLastError());
    }
    printf("\nInitialization successful..");
}
void create_socket()
{
    if ((s= socket(AF_INET, SOCK_STREAM, 0 )) == INVALID_SOCKET)
        printf("Could not create socket: %d", WSAGetLastError);

    printf("\nSocket Has been created successfully..");
    server.sin_addr.s_addr = inet_addr("192.168.2.39");
    server.sin_family = AF_INET;
    server.sin_port = htons(12345);

    if (connect(s, (struct sockaddr *)&server, sizeof(server)) < 0)
    {
        puts("connect error");
    }

    puts("\nSuccessfully connected to the server..\n");
}
void socket_send(char *message) {

        if(send(s, message,strlen(message), 0) < 0) {
            puts("Send failed");
        }


    puts("Data send");

}
/* ####################################
 * Message displayed when launching program
 * ####################################*/
void giveUnnecessaryMessage()
{
    printf("###########################################\n");
    printf("#####      Adaptive Host            #######\n");
    printf("#####      Intrusion Detection      #######\n");
    printf("#####      System Made by           #######\n");
    printf("##### Raoul Dinmohamed & Hakan Kece #######\n");
    printf("###########################################\n");
}


