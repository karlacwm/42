/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wcheung <wcheung@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/29 12:38:46 by wcheung           #+#    #+#             */
/*   Updated: 2025/11/04 15:00:19 by wcheung          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H

# include <unistd.h>
# include <stdlib.h>
# include <stdarg.h>
# include "libft/libft.h"

int	ft_printf(const char *str, ...);
int	print_char(int c);
int	print_str(char *str);
int	print_int(int n);
int	print_hex(unsigned int n, char *base);
int	print_unsigned_int(unsigned int n);
int	print_pointer(void *ptr);

#endif
