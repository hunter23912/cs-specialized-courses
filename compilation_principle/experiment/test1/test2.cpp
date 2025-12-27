#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{
    char cwd[1024];
    if (getcwd(cwd, sizeof(cwd)) != NULL)
    {
        printf("Current working directory: %s\n", cwd);
    }
    else
    {
        perror("getcwd() error");
        return 1;
    }

    FILE *file = fopen("yourfile.txt", "r");
    if (file == NULL)
    {
        perror("Error opening file");
        return 1;
    }

    fclose(file);
    return 0;
}
