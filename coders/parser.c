/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parser.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/03 18:49:21 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/04 00:04:13 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

// return 0 if not a number, 1 if is a number
static int  is_number(const char *str)
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

static t_arg    *store_data(char **argv)
{
    t_arg *args;

    args = malloc(sizeof(t_arg));
    if (!args)
    {
        printf("Memory allocation error.\n");
        exit(1);
    }
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
    return (args);
}

t_arg    *parse_argv(int argc, char ** argv)
{
    int i;

    if (argc != 9)
	{
		printf("Parsing error - invalid number of arguments.\n");
		return (NULL);
	}
    if (strcmp(argv[8], "fifo") != 0 && strcmp(argv[8], "edf") != 0)
    {
        printf("Parsing error - scheduler must be either fifo or edf.\n");
        return (NULL);
    }
    i = 1;
    while (i < 8)
    {
        if (!is_number(argv[i]))
        {
            printf("Parsing error - %s is not a positive integer.\n", argv[i]);
            return (NULL);
        }
        i++;
    }
    return (store_data(argv));
}



// "Try again with: ./codexion <no_of_coders> <time_to_burnout> "
// 			"<time_to_compile> <time_to_debug> <time_to_refactor> "
// 			"<no_of_compiles_required> <dongle_cooldown> <scheduler>\n"