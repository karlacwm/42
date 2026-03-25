#include <unistd.h>

// int	main(int argc, char**argv)
// {
// 	int	i = 0;

// 	if (argc == 2)
// 	{
// 		char *str = argv[1];

// 		while (str[i])
// 		{
// 			//if (argv[1][i] >= 65 && argv[1][i] <= 90)
// 			int indexpos = str[i] - 'a';
// 			int j = 0;
// 			while (j <= indexpos)
// 			{
// 				write(1, &str[i], 1);
// 				j++;
// 			}
// 			i++;
// 		}
// 	}
// 	write(1, "\n", 1);
// 	return (0);
// }

int	main(int argc, char**argv)
{
	int	i = 0;
	int	count = 0;

	if (argc == 2)
	{
		while (argv[1][i])
		{
			if (argv[1][i] >= 65 && argv[1][i] <= 90)
				count = argv[1][i] - 'A';
			while (count > 0)
			{
				write(1, &argv[1][i], 1);
				count--;
			}
			if (argv[1][i] >= 'a' && argv[1][i] <= 'z')
			{
				count = argv[1][i] - 'a';
				while (count > 0)
				{
					write(1, &argv[1][i], 1);
					count--;
				}
			}
			else
				write(1, &argv[1][i], 1);
			i++;
		}
	}
	write(1, "\n", 1);
	return (0);
}
