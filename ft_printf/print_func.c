/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   print_func.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/31 09:09:42 by wcheung           #+#    #+#             */
/*   Updated: 2025/11/03 11:48:29 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	print_char(int c)
{
	if (write(1, &c, 1) == -1)
		return (-1);
	return (1);
}

int	print_str(char *str)
{
	size_t	str_len;

	if (!str)
	{
		if (write(1, "(null)", 6) == -1)
			return (-1);
		return (6);
	}
	else
	{
		str_len = ft_strlen(str);
		if (write(1, str, str_len) == -1)
			return (-1);
	}
	return (str_len);
}

int	print_int(int n)
{
	char	*a;
	size_t	digits;

	a = ft_itoa(n);
	digits = ft_strlen(a);
	if (!a)
		return (-1);
	if (write (1, a, digits) == -1)
	{
		free(a);
		return (-1);
	}
	free(a);
	return (digits);
}
