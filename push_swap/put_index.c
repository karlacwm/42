/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   put_index.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/11 16:37:29 by wcheung           #+#    #+#             */
/*   Updated: 2026/01/19 18:40:42 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	stack_size(t_node *stack)
{
	int		i;
	t_node	*current;

	i = 0;
	current = stack;
	while (current)
	{
		current = current->next;
		i++;
	}
	return (i);
}

static int	*stack_to_array(t_node *stack, int size)
{
	int	*array;
	int	i;

	size = stack_size(stack);
	array = malloc(sizeof(int) * size);
	if (!array)
		return (NULL);
	i = 0;
	while (stack)
	{
		array[i++] = stack->value;
		stack = stack->next;
	}
	return (array);
}

static void	*bubble_sort(int *array, int size)
{
	int	i;
	int	j;
	int	tmp;

	i = 0;
	while (i < size - 1)
	{
		j = 0;
		while (j < size - i - 1)
		{
			if (array[j] > array[j + 1])
			{
				tmp = array[j];
				array[j] = array[j + 1];
				array[j + 1] = tmp;
			}
			j++;
		}
		i++;
	}
	return (array);
}

void	indexing(t_node *stack)
{
	int		size;
	int		*array;
	int		i;
	t_node	*tmp;

	size = stack_size(stack);
	array = stack_to_array(stack, size);
	bubble_sort(array, size);
	tmp = stack;
	while (tmp)
	{
		i = 0;
		while (i < size)
		{
			if (array[i] == tmp->value)
				tmp->index = i;
			i++;
		}
		tmp = tmp->next;
	}
	free(array);
}

// total number of integers
// bubble sort
// put index according to rank in array
// sort array wont count as operations
