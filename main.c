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

/* ####################################
 * Refers to the sub functions
 * ####################################*/

void printCurrentFile();
void printListOfFiles();
void readFileContent();
void giveUnnecessaryMessage();
void getModificationTimeOfFile();
void deleteFile();


int main()
{
    giveUnnecessaryMessage();
    printCurrentFile();
    printListOfFiles();
    readFileContent();
    getModificationTimeOfFile();
    deleteFile();


}
/* ####################################
 * Print out current directory
 * ####################################*/
void printCurrentFile()
{
    char* buffer;
    printf("\n----------Printing Current path-------\n");
    printf("Current Directory is: ");
    // Get the current working directory:
    if( (buffer = _getcwd( NULL, 0 )) == NULL )
        perror( "_getcwd error" );
    else
    {
        printf( "%s", buffer);
        free(buffer);
    }
}

/* ####################################
 * Print out files in directory
 * ####################################*/
void printListOfFiles()
{
    DIR *d;
    struct dirent *dir;
    d = opendir("./test");
    printf("\n----------Printing files in directory-------\n");
    printf("List of files are being printed:");
    printf("\n\n");
    if (d) {
        while ((dir = readdir(d)) != NULL) {
            if (dir->d_type == DT_REG)
                printf("%s\n", dir->d_name);

        }
        closedir(d);
    }
    printf("\nList is printed.\n");
}

/* ####################################
 * Read file content
 * ####################################*/
void readFileContent()
{
    FILE *f;
    char s;
    f=fopen("./test/todo.txt","r");
    printf("\n----------Reading file content-------\n");
    printf("File text.txt as test is being read\n");
    printf("Outcome of the file is: \n");
    while((s=fgetc(f))!=EOF) {
        printf("%c",s);
    }
    fclose(f);
}
/* ####################################
 * Show access and modify time of file
 * ####################################*/
void getModificationTimeOfFile()
{
    struct stat filestat;

    stat("test.txt",&filestat);
    /* newline included in ctime() output */
    printf("\n-------Show Access and Modify time of file-----\n");
    printf(" File access time %s",
           ctime(&filestat.st_atime)
    );
    printf(" File modify time %s",
           ctime(&filestat.st_mtime)
    );
}
/* ####################################
 * Delete file based on answer
 * ####################################*/
void deleteFile()
{
    int status;
    char file_name[20];
    char directory[40] = "C:/Users/test/Downloads/test/";
    printf("\n-------Delete file based on input-----\n");
    printf("name a file you want to delete;\n");
    gets(file_name);
    strcat(directory, file_name);
    status = remove(directory);

    if (status == 0)
    {
        printf("%s file deleted successfully. \n",file_name);
    } else
    {
        printf("Unable to delete file\n");
        perror("Following error occured: ");
    }
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