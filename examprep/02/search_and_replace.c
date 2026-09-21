#include <unistd.h>
#include <stdlib.h>

int	ft_strlen(char *str)
{
	int	str_len = 0;
	while (str[str_len])
		str_len++;
	return (str_len);
}

int	main(int argc, char **argv)
{
	if(argc == 4)
	{
		int	i = 0;
		char *str = argv[2];
		char *str2 = argv[3];
		if (ft_strlen(str) > 2)
		{
			write(1, "\n", 1);
			return (0);
		}
		if (ft_strlen(str2) > 2)
		{
			write(1, "\n", 1);
			return (0);
		}
		while (argv[1][i])
		{
			if (argv[1][i] == argv[2][0])
				argv[1][i] = argv[3][0];
			write(1, &argv[1][i], 1);
			i++;
		}
	}
	write(1, "\n", 1);
	return (0);
}
