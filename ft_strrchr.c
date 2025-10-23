/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strrchr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/16 11:52:08 by wcheung           #+#    #+#             */
/*   Updated: 2025/10/23 12:16:23 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strrchr(const char *str, int c)
{
	long	len;

	len = ft_strlen(str);
	while (len >= 0)
	{
		if (str[len] == (char)c)
			return ((char *)(str + len));
		len--;
	}
	return (0);
}
// int	main(void)
// {
// 	char	s[] = "monday tuesday wednesday thursday";
// 	int	c = 't';
// 	printf("ft_strrchr: %s\n", ft_strrchr(s, c));
// 	printf("strrchr: %s\n", strrchr(s, c));
// }
