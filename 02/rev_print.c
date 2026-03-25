#include <unistd.h>

// int	ft_strlen(char *str)
// {
// 	int	str_len = 0;
// 	while (str[str_len])
// 		str_len++;
// 	return (str_len);
// }

// int	main(int argc, char**argv)
// {
// 	if (argc == 2)
// 	{
// 	int	i = ft_strlen(argv[1]);
// 		while (i >= 0)
// 		{
// 			write(1, &argv[1][i--], 1);
// 		}

// 	}
// 	write(1, "\n", 1);
// 	return (0);
// }

int	main(int argc, char**argv)
{
	int	i = 0;
	if (argc == 2)
	{
		while (argv[1][i])
			i++;
		while (i--)
			write(1, &argv[1][i], 1);
	}
	write(1, "\n", 1);
	return (0);
}
