/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strnstr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/16 14:24:20 by wcheung           #+#    #+#             */
/*   Updated: 2025/10/24 14:36:48 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strnstr(const char *bigstr, const char *substr, size_t len)
{
	size_t	i;
	size_t	j;

	i = 0;
	if (!*substr)
		return ((char *)bigstr);
	while (bigstr[i] && i < len)
	{
		if (bigstr[i] == substr[0])
		{
			j = 0;
			while (substr[j] && bigstr[i + j] == substr[j] && i + j < len)
			{
				if (substr[j + 1] == '\0')
					return ((char *)bigstr + i);
				j++;
			}
		}
		i++;
	}
	return (NULL);
}
// #include <stdio.h>

// int main(void)
// {
// 	const char *big = "Hello world!";
// 	const char *sub = "o";

// 	printf("ft_strnstr: %s\n", ft_strnstr(big, sub, 8));
// 	return 0;
// }
