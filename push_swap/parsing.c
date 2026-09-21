/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parsing.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/11 11:26:24 by wcheung           #+#    #+#             */
/*   Updated: 2026/01/19 18:36:58 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	check_integers(char *str)
{
	if (*str == '+' || *str == '-')
		str++;
	if (!*str)
		return (1);
	while (*str)
	{
		if (!ft_isdigit(*str))
			return (1);
		str++;
	}
	return (0);
}

static int	check_duplicates(t_node *a, int n)
{
	if (!a)
		return (0);
	while (a)
	{
		if (a->value == n)
			return (1);
		a = a->next;
	}
	return (0);
}

static long	ft_atol(const char *str)
{
	long	result;
	int		sign;
	int		i;

	result = 0;
	sign = 1;
	i = 0;
	while (str[i] == ' ' || (str[i] >= 9 && str[i] <= 13))
		i++;
	if (str[i] == '-' || str[i] == '+')
	{
		if (str[i] == '-')
			sign *= -1;
		i++;
	}
	while (str[i] >= '0' && str[i] <= '9')
	{
		result = result * 10 + (str[i] - '0');
		i++;
	}
	return (result * sign);
}

void	build_stack_a(t_node **a, char **single_int)
{
	int		i;
	long	n;
	t_node	*new_node;

	i = 0;
	while (single_int[i])
	{
		if (check_integers(single_int[i]))
			free_errors(a);
		n = ft_atol(single_int[i]);
		if (n > 2147483647 || n < -2147483648)
			free_errors(a);
		if (check_duplicates(*a, (int)n))
			free_errors(a);
		new_node = put_value((int)n);
		if (!new_node)
			free_errors(a);
		stack_add_to_end(a, new_node);
		i++;
	}
}
