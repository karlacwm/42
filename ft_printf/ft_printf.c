/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/28 11:09:52 by wcheung           #+#    #+#             */
/*   Updated: 2025/11/06 12:34:34 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	ft_type(char specifier, va_list args)
{
	int	count;

	count = 0;
	if (specifier == 'c')
		count = print_char(va_arg(args, int));
	else if (specifier == 's')
		count = print_str(va_arg(args, char *));
	else if (specifier == 'p')
		count = print_pointer(va_arg(args, void *));
	else if (specifier == 'd' || specifier == 'i')
		count = print_int(va_arg(args, int));
	else if (specifier == 'u')
		count = print_unsigned_int(va_arg(args, unsigned int));
	else if (specifier == 'x')
		count = print_hex(va_arg(args, unsigned int), "0123456789abcdef");
	else if (specifier == 'X')
		count = print_hex(va_arg(args, unsigned int), "0123456789ABCDEF");
	else if (specifier == '%')
		count = print_char('%');
	return (count);
}

static int	check_format(const char **str_ptr, va_list args, int *total_count)
{
	const char	*str;

	str = *str_ptr + 1;
	if (*str == '\0')
		return (-1);
	if (ft_strchr("cspdiuxX%", *str))
		*total_count += ft_type(*str, args);
	else
	{
		write(1, --str, 1);
		(*total_count)++;
	}
	*str_ptr = str;
	return (0);
}

int	ft_printf(const char *str, ...)
{
	int		total_count;
	va_list	args;

	if (!str)
		return (-1);
	total_count = 0;
	va_start(args, str);
	while (*str)
	{
		if (*str == '%')
		{
			if (check_format(&str, args, &total_count) == -1)
				return (va_end(args), -1);
		}
		else
		{
			write(1, str, 1);
			total_count++;
		}
		str++;
	}
	va_end(args);
	return (total_count);
}
