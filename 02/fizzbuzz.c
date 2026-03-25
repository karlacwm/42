#include <unistd.h>

void	write_numbers(int n)
{
	char	c;

	if (n > 10)
		write_numbers(n / 10);
	c = (n % 10) + '0';
	write(1, &c, 1);
}

int	main()
{
	int	i;

	i = 1;
	while (i <= 100)
	{
		if (i % 3 == 0 && i % 5 == 0)
			write(1, "fizzbuzz", 8);
		else if (i % 3 == 0)
			write(1, "fizz", 4);
		else if (i % 5 == 0)
			write(1, "buzz", 4);
		else
			write_numbers(i);
		write(1, "\n", 1);
		i++;
	}
	return (0);
}
