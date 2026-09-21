/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strrchr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/16 11:52:08 by wcheung           #+#    #+#             */
/*   Updated: 2025/10/25 16:20:17 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strrchr(const char *str, int c)
{
	long	str_len;

	str_len = ft_strlen(str);
	while (str_len >= 0)
	{
		if ((unsigned char)str[str_len] == (unsigned char)c)
			return ((char *)(str + str_len));
		str_len--;
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
