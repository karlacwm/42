/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putendl_fd.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/24 15:28:20 by wcheung           #+#    #+#             */
/*   Updated: 2025/10/24 22:33:26 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void    ft_putendl_fd(char *str, int fd)
{
    ft_putstr_fd(str, fd);
    ft_putchar_fd('\n', fd);
}

// int main(void)
// {
//     char a[] = "heilbronn hauptbahnhof";
//     ft_putendl_fd(a, 1);
//     return (0);
// }