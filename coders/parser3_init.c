/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parser3.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/22 00:24:01 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/22 00:28:42 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	init_dongles(t_arg *args, t_dongle *dongles)
{
	int	i;

	i = 0;
	while (i < args->nb_coders)
	{
		dongles[i].id = i;
		dongles[i].available_when = 0;
		if (pthread_mutex_init(&dongles[i].mutex, NULL) != 0)
			return (1);
		i++;
	}
	return (0);
}

static void	init_coders(t_arg *args, t_coder *coders, t_dongle *dongles)
{
	int	i;

	i = 0;
	while (i < args->nb_coders)
	{
		coders[i].id = i + 1;
		coders[i].nb_compiles = 0;
		coders[i].last_compile_time = 0;
		coders[i].args = args;
		coders[i].left_dongle = &dongles[i];
		coders[i].right_dongle = &dongles[(i + 1) % args->nb_coders];
		i++;
	}
}

int	init_data(t_arg *args, t_coder **coders, t_dongle **dongles)
{
	*dongles = malloc(sizeof(t_dongle) * args->nb_coders);
	if (!*dongles)
		return (1);
	*coders = malloc(sizeof(t_coder) * args->nb_coders);
	if (!*coders)
	{
		free(*dongles);
		return (1);
	}
	if (init_dongles(args, *dongles))
	{
		free(*coders);
		free(*dongles);
		return (1);
	}
	init_coders(args, *coders, *dongles);
	return (0);
}
