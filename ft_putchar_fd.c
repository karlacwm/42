/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putchar_fd.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/24 11:39:52 by wcheung           #+#    #+#             */
/*   Updated: 2025/10/24 15:57:52 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void    ft_putchar_fd(char c, int fd)
{
    write(fd, &c, 1);
}

// #include <stdio.h>

// int main(void)
// {
//     char a = 'h';
//     ft_putchar_fd(a, 1);    
// }