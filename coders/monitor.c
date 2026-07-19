/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   monitor.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/18 02:33:33 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/19 23:13:03 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	monitor_check(t_coder *coders)
{
	int i;
    int all_finished;
    long time_since_last_compile;

    while (check_burnout_or_coding(coders[0].args))
    {
        i = 0;
        all_finished = 1; // Assume everyone is done until proven otherwise

        while (i < coders[0].args->nb_coders)
        {
            // Lock to safely read the coder's current status
            pthread_mutex_lock(&coders[0].args->coding_mutex);
            time_since_last_compile = get_time_in_ms() - coders[i].last_compile_time;

            // Check if this coder hasn't reached their quota yet
            if (coders[i].args->nb_compiles_required == -1 ||
                coders[i].nb_compiles < coders[i].args->nb_compiles_required)
            {
                all_finished = 0; // Someone is still working
            }
            pthread_mutex_unlock(&coders[0].args->coding_mutex);

            // --- BURNOUT CHECK ---
            if (time_since_last_compile > coders[0].args->time_to_burnout)
            {
                // 1. Flip the kill switch to stop all coders
                pthread_mutex_lock(&coders[0].args->coding_mutex);
                coders[0].args->burnout_yet = 0;
                pthread_mutex_unlock(&coders[0].args->coding_mutex);

                // 2. Print the death message. (We lock message_mutex so it doesn't garble)
                pthread_mutex_lock(&coders[0].args->message_mutex);
                printf("%ld %d burned out\n",
                       get_time_in_ms() - coders[0].args->start_time, coders[i].id);
                // Note: We intentionally do NOT unlock the message_mutex here.
                // This permanently silences the terminal so no coders can print after a death!

                // 3. Wake up any coders stuck in the waiting room so they can exit
                pthread_cond_broadcast(&coders[0].args->queue_cond);
                return ;
            }
            i++;
        }

        // --- QUOTA CHECK ---
        // If the loop finished and all coders met their quota, stop the simulation cleanly
        if (coders[0].args->nb_compiles_required != -1 && all_finished == 1)
        {
            pthread_mutex_lock(&coders[0].args->coding_mutex);
            coders[0].args->burnout_yet = 0;
            pthread_mutex_unlock(&coders[0].args->coding_mutex);

            // Wake up anyone stuck in the waiting room
            pthread_cond_broadcast(&coders[0].args->queue_cond);
            return ;
        }

        // Sleep for a tiny amount (e.g., 1ms) so the monitor doesn't fry your CPU
        usleep_in_ms(1);
    }
}
