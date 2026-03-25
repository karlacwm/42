#include <stdio.h>

int	ft_atoi(const char *str)
{
	int	sign = 1;
	unsigned int	result = 0;

	while (*str == ' ' || (*str >= 9 && *str <= 13))
		str++;
	if (*str == '+' || *str == '-')
	{
		if (*str == '-')
			sign *= -1;
		str++;
	}
	while (*str >= '0' && *str <= '9')
	{
		result = result * 10 + (*str - '0');
		str++;
	}
	return (result * sign);
}

int	main()
{
	char  a[]= "2345";
	int b = ft_atoi(a);
	printf("%d", b);
}
