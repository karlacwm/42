/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/06 18:51:04 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/14 21:46:45 by wcheung          ###   ########.fr       */
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

// tv_sec = seconds
// tv_usec = microseconds
// 1 microsec = 0.000001 sec
// 1 microsec = 0.001 millisec
// 1 sec = 1000 millisec
// milliseconds = tv_sec*1000 + tv_usec/1000
