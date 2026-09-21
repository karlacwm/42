/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   monitor.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/18 02:33:33 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/25 02:09:17 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	coder_burned_out(t_coder *coders, int i)
{
	pthread_mutex_lock(&coders[0].args->queue_mutex);
	pthread_mutex_lock(&coders[0].args->coding_mutex);
	coders[0].args->burnout_yet = 0;
	pthread_mutex_unlock(&coders[0].args->coding_mutex);
	pthread_mutex_lock(&coders[0].args->message_mutex);
	printf("%ld %d burned out\n",
		get_time_in_ms() - coders[0].args->start_time, coders[i].id);
	pthread_mutex_unlock(&coders[0].args->message_mutex);
	pthread_cond_broadcast(&coders[0].args->queue_cond);
	pthread_mutex_unlock(&coders[0].args->queue_mutex);
}

static int	check_coder(t_coder *coders, int i, int *all_finished)
{
	long	last_compile;
	long	elapsed;
	int		nb_compiles;

	pthread_mutex_lock(&coders[0].args->coding_mutex);
	last_compile = coders[i].last_compile_time;
	nb_compiles = coders[i].nb_compiles;
	pthread_mutex_unlock(&coders[0].args->coding_mutex);
	elapsed = get_time_in_ms() - last_compile;
	if (coders[i].args->nb_compiles_required == -1
		|| nb_compiles < coders[i].args->nb_compiles_required)
		*all_finished = 0;
	if (elapsed > coders[0].args->time_to_burnout)
	{
		coder_burned_out(coders, i);
		return (1);
	}
	return (0);
}

void	monitor_check(t_coder *coders)
{
	int	i;
	int	all_finished;

	while (check_burnout_or_coding(coders[0].args))
	{
		i = 0;
		all_finished = 1;
		while (i < coders[0].args->nb_coders)
		{
			if (check_coder(coders, i, &all_finished))
				return ;
			i++;
		}
		if (coders[0].args->nb_compiles_required != -1 && all_finished)
		{
			pthread_mutex_lock(&coders[0].args->queue_mutex);
			pthread_mutex_lock(&coders[0].args->coding_mutex);
			coders[0].args->burnout_yet = 0;
			pthread_mutex_unlock(&coders[0].args->coding_mutex);
			pthread_cond_broadcast(&coders[0].args->queue_cond);
			pthread_mutex_unlock(&coders[0].args->queue_mutex);
			return ;
		}
		usleep_in_ms(1);
	}
}
