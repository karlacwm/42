/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parser2_store.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/22 00:18:31 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/25 02:02:51 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	store_numbers(char **argv, t_arg *args)
{
	if (parse_and_store(argv[1], &args->nb_coders))
		return (1);
	if (parse_and_store(argv[2], &args->time_to_burnout))
		return (1);
	if (parse_and_store(argv[3], &args->time_to_compile))
		return (1);
	if (parse_and_store(argv[4], &args->time_to_debug))
		return (1);
	if (parse_and_store(argv[5], &args->time_to_refactor))
		return (1);
	if (parse_and_store(argv[6], &args->nb_compiles_required))
		return (1);
	if (parse_and_store(argv[7], &args->dongle_cooldown))
		return (1);
	return (0);
}

static int	store_data(char **argv, t_arg *args)
{
	if (store_numbers(argv, args))
		return (1);
	if (strcmp(argv[8], "fifo") == 0)
		args->scheduler = 0;
	else
		args->scheduler = 1;
	return (0);
}

static int	validate_values(t_arg *args)
{
	if (args->nb_coders <= 0)
	{
		printf("Parsing error - should have at least one coder.\n");
		return (1);
	}
	if (args->time_to_burnout < 0 || args->time_to_compile < 0
		|| args->time_to_debug < 0 || args->time_to_refactor < 0
		|| args->dongle_cooldown < 0)
	{
		printf("Parsing error - all time values must be positive.\n");
		return (1);
	}
	if (args->nb_compiles_required < 0)
	{
		printf("Parsing error - no of compiles required must be positive.\n");
		return (1);
	}
	return (0);
}

int	parse_argv(int argc, char **argv, t_arg *args)
{
	if (argc != 9)
	{
		printf("Parsing error - invalid number of arguments.\n");
		return (1);
	}
	if (strcmp(argv[8], "fifo") != 0
		&& strcmp(argv[8], "edf") != 0)
	{
		printf("Parsing error - scheduler must be either fifo or edf.\n");
		return (1);
	}
	if (store_data(argv, args))
		return (1);
	return (validate_values(args));
}
