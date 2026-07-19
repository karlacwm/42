NAME = codexion
CC = cc
CFLAG = -Wall -Wextra -Werror -pthread
RM = rm -f

SRC = main.c parser.c cycle.c utils.c queue.c dongles.c monitor.c

OBJ = ${SRC:%.c=%.o}

all: $(NAME)

$(NAME): $(OBJ)
	$(CC) $(CFLAG) -o $(NAME) $(OBJ)

clean:
	$(RM) $(OBJ)

fclean: clean
	$(RM) $(NAME)

re: fclean all

.PHONY: all clean fclean re
