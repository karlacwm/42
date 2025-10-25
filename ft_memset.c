/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memset.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/14 15:52:00 by wcheung           #+#    #+#             */
/*   Updated: 2025/10/25 13:00:41 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memset(void *str, int c, size_t n)
{
	unsigned char	*ptr;

	ptr = str;
	while (n > 0)
	{
		*ptr = c;
		ptr++;
		n--;
	}
	return (str);
}
// you cannot directly dereference a void pointer
// ptr = s -- ptr will point to the same memory location as s
// ptr++ moving it to the next memory location
// but *ptr++ would deference the pointer
// return (s) -- return to original pointer to the modified data
