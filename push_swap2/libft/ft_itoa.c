/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/24 15:10:33 by wcheung           #+#    #+#             */
/*   Updated: 2025/10/26 13:12:41 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static size_t	ft_digit_count(long n)
{
	size_t	n_len;

	n_len = 0;
	if (n == 0)
		return (1);
	if (n < 0)
	{
		n_len++;
		n = -n;
	}
	while (n > 0)
	{
		n = n / 10;
		n_len++;
	}
	return (n_len);
}

char	*ft_itoa(int n)
{
	size_t	n_len;
	long	num;
	char	*str;

	num = n;
	n_len = ft_digit_count(num);
	str = (char *)malloc(sizeof(char) * (n_len + 1));
	if (!str)
		return (NULL);
	str[n_len] = '\0';
	n_len--;
	if (num == 0)
		str[0] = '0';
	if (num < 0)
	{
		str[0] = '-';
		num = -num;
	}
	while (num > 0)
	{
		str[n_len] = (num % 10) + '0';
		num = num / 10;
		n_len--;
	}
	return (str);
}

// #include <stdio.h>

// int	main(void)
// {
// 	int test = -987654;

// 	char *str = ft_itoa(test);
// 	if (str)
// 	{
// 		printf("ft_itoa(%d) = %s\n", test, str);
// 		free(str);
// 	}
// 	else
// 		printf("malloc failed %d\n", test);
// 	return (0);
// }
