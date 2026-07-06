/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parser.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/03 18:49:21 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/06 23:49:01 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

// return 0 if not a number, 1 if is a number
static int	is_number(const char *str)
{
	if (!*str)
		return (0);
	while (*str)
	{
		if (*str < '0' || *str > '9')
			return (0);
		str++;
	}
	return (1);
}

static void	store_data(char **argv, t_arg *args)
{
	// check INT MAX???
	args->nb_coders = atoi(argv[1]);
	args->time_to_burnout = atoi(argv[2]);
	args->time_to_compile = atoi(argv[3]);
	args->time_to_debug = atoi(argv[4]);
	args->time_to_refactor = atoi(argv[5]);
	args->nb_compiles_required = atoi(argv[6]);
	args->dongle_cooldown = atoi(argv[7]);
	if (strcmp(argv[8], "fifo") == 0)
		args->scheduler = 0;
	else
		args->scheduler = 1;
}

int	parse_argv(int argc, char **argv, t_arg *args)
{
	int	i;

	if (argc != 9)
	{
		printf("Parsing error - invalid number of arguments.\n");
		return (1);
	}
	if (strcmp(argv[8], "fifo") != 0 && strcmp(argv[8], "edf") != 0)
	{
		printf("Parsing error - scheduler must be either fifo or edf.\n");
		return (1);
	}
	i = 1;
	while (i < 8)
	{
		if (!is_number(argv[i]))
		{
			printf("Parsing error - %s is not a positive integer.\n", argv[i]);
			return (1);
		}
		i++;
	}
	store_data(argv, args);
	return (0);
}

int	init_data(t_arg *args, t_coder **coders, t_dongle **dongles)
{
	int	i;

	*dongles = malloc(sizeof(t_dongle) * args->nb_coders);
	if (!*dongles)
		return (1);
	*coders = malloc(sizeof(t_coder) * args->nb_coders);
	if (!*coders)
	{
		free(*dongles);
		return (1);
	}
	i = 0;
	while (i < args->nb_coders)
	{
		(*dongles)[i].id = i;
		(*dongles)[i].cooldown_until = 0;
		if (pthread_mutex_init(&(*dongles)[i].mutex, NULL) != 0)
		{
			free(*coders);
			free(*dongles);
			return (1);
		}
		i++;
	}
	i = 0;
	while (i < args->nb_coders)
	{
		// Coders must be numbered from 1 to number_of_coders[cite: 1]
		(*coders)[i].id = i + 1;
		(*coders)[i].nb_compiles = 0;
		(*coders)[i].last_compile_time = 0;
		(*coders)[i].args = args; // Hand them the rulebook
		// Link the left and right dongles
		(*coders)[i].left_dongle = &((*dongles)[i]);
		(*coders)[i].right_dongle = &((*dongles)[(i + 1) % args->nb_coders]);
		i++;
	}
	return (0);
}

// "Try again with: ./codexion <no_of_coders> <time_to_burnout> "
// 			"<time_to_compile> <time_to_debug> <time_to_refactor> "
// 			"<no_of_compiles_required> <dongle_cooldown> <scheduler>\n"
