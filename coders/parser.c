/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parser.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/03 18:49:21 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/21 15:30:28 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	parse_int_arg(const char *str, int *value)
{
	int		i;
	int		sign;
	long	result;
	int		digit;

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
	while (str[i] != '\0')
	{
		if (str[i] < '0' || str[i] > '9')
			return (0);
		digit = str[i] - '0';
		if (sign > 0)
		{
			if (result > 2147483647 / 10
				|| (result == 2147483647 / 10 && digit > 2147483647 % 10))
				return (0);
		}
		else
		{
			if (result > 2147483648 / 10
				|| (result == 2147483648 / 10 && digit > 2147483648 % 10))
				return (0);
		}
		result = result * 10 + digit;
		i++;
	}
	if (sign < 0)
		result = -result;
	*value = (int)result;
	return (1);
}

static int	store_data(char **argv, t_arg *args)
{
	int	value;

	if (!parse_int_arg(argv[1], &value))
	{
		printf("Parsing error - %s is not a valid integer.\n", argv[1]);
		return (1);
	}
	args->nb_coders = value;
	if (!parse_int_arg(argv[2], &value))
	{
		printf("Parsing error - %s is not a valid integer.\n", argv[2]);
		return (1);
	}
	args->time_to_burnout = value;
	if (!parse_int_arg(argv[3], &value))
	{
		printf("Parsing error - %s is not a valid integer.\n", argv[3]);
		return (1);
	}
	args->time_to_compile = value;
	if (!parse_int_arg(argv[4], &value))
	{
		printf("Parsing error - %s is not a valid integer.\n", argv[4]);
		return (1);
	}
	args->time_to_debug = value;
	if (!parse_int_arg(argv[5], &value))
	{
		printf("Parsing error - %s is not a valid integer.\n", argv[5]);
		return (1);
	}
	args->time_to_refactor = value;
	if (!parse_int_arg(argv[6], &value))
	{
		printf("Parsing error - %s is not a valid integer.\n", argv[6]);
		return (1);
	}
	args->nb_compiles_required = value;
	if (!parse_int_arg(argv[7], &value))
	{
		printf("Parsing error - %s is not a valid integer.\n", argv[7]);
		return (1);
	}
	args->dongle_cooldown = value;
	if (strcmp(argv[8], "fifo") == 0)
		args->scheduler = 0;
	else
		args->scheduler = 1;
	return (0);
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
		if (argv[i][0] == '\0')
		{
			printf("Parsing error - %s is not a valid integer.\n", argv[i]);
			return (1);
		}
		i++;
	}
	if (store_data(argv, args) != 0)
		return (1);
	if (args->nb_coders <= 0)
	{
		printf("Parsing error - should have at least one coder.\n");
		return (1);
	}
	if (args->time_to_burnout < 0
		|| args->time_to_compile < 0 || args->time_to_debug < 0
		|| args->time_to_refactor < 0 || args->dongle_cooldown < 0)
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
		(*dongles)[i].available_when = 0;
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
		(*coders)[i].id = i + 1;
		(*coders)[i].nb_compiles = 0;
		(*coders)[i].last_compile_time = 0;
		(*coders)[i].args = args;
		(*coders)[i].left_dongle = &((*dongles)[i]);
		(*coders)[i].right_dongle = &((*dongles)[(i + 1) % args->nb_coders]);
		i++;
	}
	return (0);
}

// "Try again with: ./codexion <no_of_coders> <time_to_burnout> "
// 			"<time_to_compile> <time_to_debug> <time_to_refactor> "
// 			"<no_of_compiles_required> <dongle_cooldown> <scheduler>\n"
