/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/06 18:51:04 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/14 22:13:04 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

long	get_time_in_ms(void)
{
	struct	timeval time;

	if (gettimeofday(&time, NULL) != 0)
	{
		printf("Failed to get current time :(");
		return (0);
	}
	return ((time.tv_sec * 1000) + (time.tv_usec / 1000));
}

void	log_message(t_coder *coder, char *status)
{
	long	time_passed;

	time_passed = get_time_in_ms() - coder->args->start_time;
	pthread_mutex_lock(&coder->args->message_mutex);
	printf("%ld %d %s\n", time_passed, coder->id, status);
	pthread_mutex_unlock(&coder->args->message_mutex);
}

void	usleep_in_ms(long time_to_sleep_in_ms)
{
	long	start_time;

	start_time = get_time_in_ms();
	while ((get_time_in_ms() - start_time) < time_to_sleep_in_ms)
		usleep(500);
}

// tv_sec = seconds
// tv_usec = microseconds
// 1 microsec = 0.000001 sec
// 1 microsec = 0.001 millisec
// 1 sec = 1000 millisec
// milliseconds = tv_sec*1000 + tv_usec/1000
