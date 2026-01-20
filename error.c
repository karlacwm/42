/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   error.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/09 19:56:49 by wcheung           #+#    #+#             */
/*   Updated: 2026/01/20 17:44:29 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	free_stack(t_node **stack)
{
	t_node	*tmp;
	t_node	*current;

	if (!stack || !*stack)
		return ;
	current = *stack;
	while (current)
	{
		tmp = current->next;
		free(current);
		current = tmp;
	}
	*stack = NULL;
}

void	free_errors(t_node **a, char **each_int)
{
	if (a && *a)
		free_stack(a);
	if (each_int)
		free_after_split(each_int);
	write(2, "Error\n", 6);
	exit(1);
}

// print error if not int, or duplicated int
// print Error\n on standard error
// exit(0): success
// exit(1): fail
// echo $?
