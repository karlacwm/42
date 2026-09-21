int main(void)
{
    int     fd;
    char    *line = NULL;
    
    while ((line = get_next_line(fd)))
    {
        printf("%s", line);
        free(line);
        line = NULL;
    }
    return (0);
}