/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   cycle.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/06 16:39:21 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/25 01:53:52 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	wait_for_start(t_coder *coder)
{
	pthread_mutex_lock(&coder->args->queue_mutex);
	coder->args->ready_coders++;
	if (coder->args->ready_coders == coder->args->nb_coders)
	{
		coder->args->start_ready = 1;
		pthread_cond_broadcast(&coder->args->queue_cond);
	}
	while (!coder->args->start_ready && check_burnout_or_coding(coder->args))
		pthread_cond_wait(&coder->args->queue_cond, &coder->args->queue_mutex);
	pthread_mutex_unlock(&coder->args->queue_mutex);
}

static void	compile_start(t_coder *coder)
{
	pthread_mutex_lock(&coder->args->coding_mutex);
	coder->last_compile_time = get_time_in_ms();
	pthread_mutex_unlock(&coder->args->coding_mutex);
	log_message(coder, "has taken a dongle");
	log_message(coder, "has taken a dongle");
	log_message(coder, "is compiling");
	usleep_in_ms(coder->args->time_to_compile);
}

static int	compile_done(t_coder *coder)
{
	pthread_mutex_lock(&coder->args->coding_mutex);
	coder->nb_compiles++;
	if (coder->args->nb_compiles_required != -1
		&& coder->nb_compiles >= coder->args->nb_compiles_required)
	{
		pthread_mutex_unlock(&coder->args->coding_mutex);
		release_dongles(coder);
		return (1);
	}
	pthread_mutex_unlock(&coder->args->coding_mutex);
	return (0);
}

static void	debug_refactor(t_coder *coder)
{
	release_dongles(coder);
	log_message(coder, "is debugging");
	usleep_in_ms(coder->args->time_to_debug);
	log_message(coder, "is refactoring");
	usleep_in_ms(coder->args->time_to_refactor);
}

void	*cycle(void *arg)
{
	t_coder	*coder;

	coder = (t_coder *)arg;
	wait_for_start(coder);
	while (check_burnout_or_coding(coder->args))
	{
		if (request_dongles(coder) == 0)
			break ;
		compile_start(coder);
		if (compile_done(coder))
			break ;
		debug_refactor(coder);
	}
	return (NULL);
}

// check if burn out -> monitor
// request dongle -> scheduler(fifo/edf)
// lock two dongles mutex
// update last_compile_start
// print "is compiling"
// compile for time_to_compile much long
// unlock dongle mutex and start dongle cooldown
// nb_compiles_done++
//
// print "is debugging"
// debug for time_to_debug much long
//
// print "is refactoring"
// refactor for time_to_refactor much long
//
// check if coder reached nb_compile total
