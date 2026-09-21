#include <stdio.h>

// char	*ft_strcpy(char *s1, char *s2)
// {
// 	int	i;

// 	i = 0;
// 	if (!s1 || !s2)
// 		return (NULL);
// 	while (s2)
// 	{
// 		s1[i] = s2[i];
// 		i++;
// 	}
// 	s1[i] = '\0';
// 	return(s1);
// }

char	*ft_strcpy2(char *s1, char *s2)
{
	if (!s1 || !s2)
		return (NULL);
	while (*s2)
		*s1++ = *s2++;
	*s1 = '\0';
	return(s1);
}

int	main()
{
	char	dest[] = "";
	char	src[] = "abc";

	ft_strcpy2(dest, src);
	printf("src: %s\n", src);
	printf("dest: %s\n", dest);
	return (0);
}
