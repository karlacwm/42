/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcmp.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/18 23:47:46 by wcheung           #+#    #+#             */
/*   Updated: 2025/10/23 12:19:06 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_memcmp(const void *s1, const void *s2, size_t n)
{
	unsigned const char	*str1;
	unsigned const char	*str2;

	str1 = s1;
	str2 = s2;
	while (n--)
	{
		if (*str1 != *str2)
			return (*str1 - *str2);
		str1++;
		str2++;
	}
	return (0);
}
// int	main(void)
// {
// 	char	a[] = "aaaA";
// 	char	b[] = "aaB";
// 	int	n = 4;
// 	printf("ft_memcmp = %d\n", ft_memcmp(a, b, n));
// 	printf("memcmp = %d\n", memcmp(a, b, n));
// 	return (0);
// }
