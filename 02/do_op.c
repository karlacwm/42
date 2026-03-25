#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

int	main(int argc, char **argv)
{
	if (argc == 4)
	{
		int result = 0;
		if (argv[2][0] == '+')
		{
			result = atoi(argv[1]) + atoi(argv[3]);
			printf("%d", result);
		}
		else if (argv[2][0] == '-')
		{
			result = atoi(argv[1]) - atoi(argv[3]);
			printf("%d", result);
		}
		else if (argv[2][0] == '*')
		{
			result = atoi(argv[1]) * atoi(argv[3]);
			printf("%d", result);
		}
		else if (argv[2][0] == '/')
		{
			result = atoi(argv[1]) / atoi(argv[3]);
			printf("%d", result);
		}
		else if (argv[2][0] == '%')
		{
			result = atoi(argv[1]) % atoi(argv[3]);
			printf("%d", result);
		}
	}
	printf("\n");
	return (0);
}
