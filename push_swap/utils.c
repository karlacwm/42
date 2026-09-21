/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/16 12:41:44 by wcheung           #+#    #+#             */
/*   Updated: 2026/01/16 22:04:29 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_node	*put_value(int content)
{
	t_node	*new;

	new = malloc(sizeof(t_node));
	if (!new)
		return (NULL);
	new->value = content;
	new->index = -1;
	new->next = NULL;
	new->prev = NULL;
	return (new);
}

t_node	*find_last_node(t_node *stack)
{
	if (!stack)
		return (NULL);
	while (stack->next)
		stack = stack->next;
	return (stack);
}

void	stack_add_to_end(t_node **stack, t_node *new_node)
{
	t_node	*last_node;

	if (!stack || !new_node)
		return ;
	if (*stack == NULL)
	{
		*stack = new_node;
		return ;
	}
	last_node = find_last_node(*stack);
	last_node->next = new_node;
	new_node->prev = last_node;
}

char	*combine_argv(int argc, char **argv)
{
	char	*tmp;
	char	*combined;
	int		i;

	i = 1;
	combined = ft_strdup("");
	if (!combined)
		return (NULL);
	while (i < argc)
	{
		tmp = ft_strjoin(combined, argv[i]);
		free(combined);
		combined = ft_strjoin(tmp, " ");
		free(tmp);
		i++;
	}
	return (combined);
}
