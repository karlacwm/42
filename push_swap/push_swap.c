/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/08 17:35:25 by wcheung           #+#    #+#             */
/*   Updated: 2026/01/20 13:38:28 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	is_sorted(t_node *a)
{
	if (!a)
		return (1);
	while (a->next)
	{
		if (a->value > a->next->value)
			return (0);
		a = a->next;
	}
	return (1);
}

static void	free_after_split(char **each_int)
{
	int	i;

	i = 0;
	if (!each_int)
		return ;
	while (each_int[i])
	{
		free(each_int[i]);
		i++;
	}
	free(each_int);
}

static void	sorting(t_node **a, t_node **b, int size)
{
	if (size == 2)
		sort_two(a);
	else if (size == 3)
		sort_three(a);
	else if (size == 4)
		sort_four(a, b);
	else if (size == 5)
		sort_five(a, b);
	else
		k_sort(a, b, size);
}

int	main(int argc, char **argv)
{
	t_node	*a;
	t_node	*b;
	char	*join_all;
	char	**each_int;
	int		size;

	a = NULL;
	b = NULL;
	if (argc < 2 || !argv)
		return (0);
	join_all = combine_argv(argc, argv);
	each_int = ft_split(join_all, ' ');
	free(join_all);
	build_stack_a(&a, each_int);
	free_after_split(each_int);
	if (is_sorted(a))
		return (0);
	indexing(a);
	size = stack_size(a);
	sorting(&a, &b, size);
	return (0);
}

// ./push_swap "1 4 3 5 2"
// ./push_swap 1 5 2 3 4
// ./push_swap 3 1 "2 4" 5
