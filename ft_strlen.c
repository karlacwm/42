#include <stdio.h>

int	ft_strlen(char *str)
{
	int	str_len = 0;
	while (str[str_len])
		str_len++;
	return (str_len);
}
