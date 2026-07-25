/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parser1_parse.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/03 18:49:21 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/25 02:16:13 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	check_int_overflow(long result, int digit, int sign)
{
	if (sign > 0)
	{
		if (result > 2147483647 / 10)
			return (0);
		if (result == 2147483647 / 10 && digit > 2147483647 % 10)
			return (0);
	}
	else
	{
		if (result > 2147483648 / 10)
			return (0);
		if (result == 2147483648 / 10 && digit > 2147483648 % 10)
			return (0);
	}
	return (1);
}

static int	parse_digits(const char *str, int i, int sign, long *result)
{
	int	digit;

	while (str[i] != '\0')
	{
		if (str[i] < '0' || str[i] > '9')
			return (0);
		digit = str[i] - '0';
		if (!check_int_overflow(*result, digit, sign))
			return (0);
		*result = *result * 10 + digit;
		i++;
	}
	return (1);
}

static int	parse_int_arg(const char *str, int *value)
{
	int		i;
	int		sign;
	long	result;

	if (!str || !*str)
		return (0);
	i = 0;
	sign = 1;
	result = 0;
	if (str[i] == '+')
		i++;
	else if (str[i] == '-')
	{
		sign = -1;
		i++;
	}
	if (str[i] == '\0')
		return (0);
	if (!parse_digits(str, i, sign, &result))
		return (0);
	if (sign < 0)
		result = -result;
	*value = (int)result;
	return (1);
}

int	parse_and_store(char *str, int *field)
{
	int	value;

	value = 0;
	if (!parse_int_arg(str, &value))
	{
		printf("Parsing error - %s is not a valid integer.\n", str);
		return (1);
	}
	*field = value;
	return (0);
}

// ./codexion <no_of_coders> <time_to_burnout> <time_to_compile>
// <time_to_debug> <time_to_refactor> <no_of_compiles_required>
// <dongle_cooldown> <edf/fifo>
