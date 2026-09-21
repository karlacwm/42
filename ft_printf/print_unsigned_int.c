/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   print_unsigned_int.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/31 09:09:47 by wcheung           #+#    #+#             */
/*   Updated: 2025/11/03 11:33:41 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static size_t	ft_digit_count_unsigned(unsigned int n)
{
	size_t	n_len;

	n_len = 0;
	if (n == 0)
		return (1);
	while (n > 0)
	{
		n = n / 10;
		n_len++;
	}
	return (n_len);
}

static char	*ft_unsigned_itoa(unsigned int n)
{
	size_t			n_len;
	char			*str;

	n_len = ft_digit_count_unsigned(n);
	str = (char *)malloc(sizeof(char) * (n_len + 1));
	if (!str)
		return (NULL);
	str[n_len] = '\0';
	n_len--;
	if (n == 0)
		str[0] = '0';
	while (n > 0)
	{
		str[n_len] = (n % 10) + '0';
		n = n / 10;
		n_len--;
	}
	return (str);
}

int	print_unsigned_int(unsigned int n)
{
	char	*a;
	size_t	digits;

	a = ft_unsigned_itoa(n);
	if (!a)
		return (-1);
	digits = ft_strlen(a);
	if (write (1, a, digits) == -1)
	{
		free(a);
		return (-1);
	}
	free(a);
	return (digits);
}
