/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_striteri.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/25 12:30:03 by wcheung           #+#    #+#             */
/*   Updated: 2025/10/25 19:35:29 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_striteri(char *s, void (*f)(unsigned int, char*))
{
	unsigned int	i;

	if (!s || !f)
		return ;
	i = 0;
	while (s[i])
	{
		(*f)(i, &s[i]);
		i++;
	}
}
// void	ft_uppercase(unsigned int i, char* c)
// {
// 	if (*c >= 'a' && *c <= 'z')
// 		*c -= 32;
// }
// #include <stdio.h>

// int	main(void)
// {
// 	char a[] = "aaaaa";
// 	ft_striteri(a, ft_uppercase);
// 	printf("%s", a);
// }
