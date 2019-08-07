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
 * Refers to the functions
 * ####################################*/

void giveUnnecessaryMessage(); // Function: unnecessary loop
int countDown(int); // Function: Use countdown for loop
void list_files(); // Function: make array list
void list_filesz(); // Function: duplicate array of file names for hashing.
void start_winsock(); // Function: start winsock to use socket on Windows OS.
void create_socket(); // Function: create socket / connect to server
void socket_send(char *); // Function: send socket with message.
void encrypt_data(char *); // Function: encrypt some string with caesar cipher algorithm.

/* ####################################
 * Global Variables
 * ####################################*/
char directory[] = {"C:/Users/test/Downloads/test/"}; // directory path..
int counter, i = 0, ii = 0; // some variables used for loops...
char *filesList[254];// gives error when you use variables
char *filesList2[254]; // second array
char temp[254]; // 3th array
SOCKET s; // global variable for socket
struct sockaddr_in server; //global variable for socket

int main() {
    giveUnnecessaryMessage();
    start_winsock(); // start winsock
    create_socket(); // create the socket
    printf("\nEnter in seconds a value ot repeat the program\n"); // ask for countdown, als usable for loop.
    scanf("%d",&counter); // scan the answer and put in counter
    DIRTYLOOP: // dirty way of looping code
    countDown(counter); // use answer counter in function
    list_files(); // fill in one array
    list_filesz(); // fill in second array for manipulation (hashing)

    for(int z = 0; z<i; z++){
        char *tempx = filesList[z]; //use temp as single string for function;
        encrypt_data(tempx); // encrypt string in temp (each line in array)
    }
    for (int x = 0; x<i;x++){
        strcat(filesList[x], ";"); // add ; to seperate hash and filename
        snprintf(temp, 254, "%s%s", filesList[x], filesList2[x]); // add filename and hash together.
        socket_send(temp); // send through socket inside loop..
        create_socket(); // reconnect to send again..
        sleep(2); // sleep 2 seconds.
        goto DIRTYLOOP; // looping code of loop
    }
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

}
void list_filesz()
{
    DIR *d;
    struct dirent *dir;
    d = opendir(directory);
    //Put file names into the array
    while((dir = readdir(d)) != NULL) {
        if ( ( ii < 254) && ! ( strcmp(dir->d_name, ".") == 0 || strcmp(dir->d_name, "..") == 0))
        {
            filesList2[ii] = malloc( strlen ( dir->d_name) + 1); // allocate memory
            strcpy(filesList2[ii], dir->d_name); // put file names in to array
            ii++; // do +1 to read each single array line
        }
    }

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

    server.sin_addr.s_addr = inet_addr("192.168.2.39");
    server.sin_family = AF_INET;
    server.sin_port = htons(12345);

    if (connect(s, (struct sockaddr *)&server, sizeof(server)) < 0)
    {
        puts("connect error");
    }

}
void socket_send(char *message) {

        if(send(s, message,strlen(message), 0) < 0) {
            puts("Send failed");
        }
    puts("Data send");

}
void encrypt_data(char *encrypt)
{
    for(int z = 0; (z < 100 && encrypt[z] != '\0'); z++)
        encrypt[z] = encrypt[z] + 3;
}
void giveUnnecessaryMessage()
{
    printf("###########################################\n");
    printf("#####      Adaptive Host            #######\n");
    printf("#####      Intrusion Detection      #######\n");
    printf("#####      System Made by           #######\n");
    printf("##### Raoul Dinmohamed & Hakan Kece #######\n");
    printf("###########################################\n");
}
