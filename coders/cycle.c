/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   cycle.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/06 16:39:21 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/06 23:50:13 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	*cycle(void *arg)
{
	t_coder	*coder;

	coder = (t_coder *)arg;
	while (1)
	{
		// coder cycle - compile, debug, refactor
		if (coder->args->nb_compiles_required != -1 &&
			coder->nb_compiles >= coder->args->nb_compiles_required)
		{
			printf("Coder %d has completed all required compiles.\n", coder->id);
			break ;
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
