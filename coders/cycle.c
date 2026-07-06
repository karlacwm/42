/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   cycle.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/06 16:39:21 by wcheung           #+#    #+#             */
/*   Updated: 2026/07/06 16:52:30 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void    *cycle(void *arg)
{
    t_coder    *coder;
    
    // check if burn out -> monitor
    // request dongle -> scheduler(fifo/edf)
    // lock two dongles mutex
    // update last_compile_start
    // print "is compiling"
    // compile for time_to_compile much long
    // unlock dongle mutex and start dongle cooldown
    // nb_compiles_done++

    // print "is debugging"
    // debug for time_to_debug much long

    // print "is refactoring"
    // refactor for time_to_refactor much long
    
    // check if coder reached nb_compile total
    
    return (NULL);
}