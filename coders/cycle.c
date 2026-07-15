/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   cycle.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/06 16:39:21 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/15 03:49:15 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	*cycle(void *arg)
{
	t_coder	*coder;

	coder = (t_coder *)arg;
    coder->last_compile_time = coder->args->start_time;
    while (1)
    {
        // grab dongles
        pthread_mutex_lock(&coder->left_dongle->mutex);
        log_message(coder, "has taken a dongle");

        pthread_mutex_lock(&coder->right_dongle->mutex);
        log_message(coder, "has taken a dongle");

        // compiling
        log_message(coder, "is compiling");
        coder->last_compile_time = get_time_in_ms(); // update for the monitor thread
        usleep_in_ms(coder->args->time_to_compile);
        coder->nb_compiles++;

        // release dongles
        pthread_mutex_unlock(&coder->left_dongle->mutex);
        pthread_mutex_unlock(&coder->right_dongle->mutex);

        // debug
        log_message(coder, "is debugging");
        usleep_in_ms(coder->args->time_to_debug);

        // refactoring
        log_message(coder, "is refactoring");
        usleep_in_ms(coder->args->time_to_refactor);

        // check goal
        if (coder->args->nb_compiles_required != -1 &&
            coder->nb_compiles >= coder->args->nb_compiles_required)
        {
            break;
        }
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
