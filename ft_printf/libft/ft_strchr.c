/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/15 17:35:51 by wcheung           #+#    #+#             */
/*   Updated: 2025/10/22 14:28:05 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strchr(const char *str, int c)
{
	while (*str && (unsigned char)*str != (unsigned char)c)
		str++;
	if ((unsigned char)*str == (unsigned char)c)
		return ((char *)str);
	return (NULL);
}

// int	main(void)
// {
// 	char	s[] = "monday tuesday wednesday thursday";
// 	int	c = 't';
// 	printf("ft_strchr: %s\n", ft_strchr(s, c));
// 	printf("strchr: %s\n", strchr(s, c));
// }
