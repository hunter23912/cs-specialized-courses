#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>

int main(int argc, char *argv[])
{
    char s[1024];
    FILE *fp1, *fp2, *fp3;
    if ((fp1 = fopen(argv[1], "r")) == (FILE *)0)
    {
        fprintf(stderr, "file1 open error.\n");
        exit(1);
    }
    else if ((fp2 = fopen(argv[2], "r")) == (FILE *)0)
    {
        fprintf(stderr, "file2 open error.\n");
        exit(1);
    }
    else if ((fp3 = fopen(argv[3], "w")) == (FILE *)0)
    {
        fprintf(stderr, "file2 open error.\n");
        exit(1);
    }
    else
    {
        while ((fgets(s, 1024, fp1)) != (char *)0)
            fputs(s, fp3); // 显示缓冲区
        printf("%s", s);
        while ((fgets(s, 1024, fp2)) != (char *)0)
            fputs(s, fp3); // 显示缓冲区
        printf("%s", s);
    }
    chmod(argv[3], 00755); // 修改文件为指定的属性
    fclose(fp1);
    fclose(fp2);
    fclose(fp3);
    exit(0);
}