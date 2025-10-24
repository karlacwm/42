/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putstr_fd.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/24 15:28:31 by wcheung           #+#    #+#             */
/*   Updated: 2025/10/24 16:01:26 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void    ft_putstr_fd(char *str, int fd)
{
    if (!str)
        return ;
    while (*str)
    {
        write(fd, str, 1);
        str++;
    }
}

// #include <stdio.h>

// int main(void)
// {
//     char a[] = "hihihihi";
//     ft_putstr_fd(a, 1);
//     return (0);
// }