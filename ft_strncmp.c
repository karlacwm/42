/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strncmp.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/16 13:53:46 by wcheung           #+#    #+#             */
/*   Updated: 2025/10/18 20:35:31 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_strncmp(const char *s1, const char *s2, size_t n)
{
	while (n > 0 && *s1 && (*s1 == *s2))
	{
		s1++;
		s2++;
		n--;
	}
	if (n == 0)
		return (0);
	return ((unsigned char)*s1 - (unsigned char)*s2);
}
// int	main(void)
// {
// 	char	a[] = "aaa";
// 	char	b[] = "aa";
// 	int	n = 4;
// 	printf("ft_strncmp = %d\n", ft_strncmp(a, b, n));
// 	printf("strncmp = %d\n", strncmp(a, b, n));
// 	return (0);
// }
