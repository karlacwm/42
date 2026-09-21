/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/18 23:47:26 by wcheung           #+#    #+#             */
/*   Updated: 2025/10/22 15:48:11 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memchr(const void *str, int c, size_t n)
{
	unsigned const char	*ptr;
	unsigned char		a;

	ptr = str;
	a = (unsigned char) c;
	while (n > 0)
	{
		if (*ptr == a)
			return ((void *)ptr);
		ptr++;
		n--;
	}
	return (NULL);
}
// // man: c is passed as int but searched for as unsigned char
// int	main(void)
// {
// 	char	s[] = "monday";
// 	int	c = 'y';
// 	printf("ft_memchr: %p\n", ft_memchr(s, c, 9));
// 	printf("memchr: %p\n", memchr(s, c, 9));
// }
