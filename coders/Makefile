NAME = codexion
CC = cc
CFLAG = -Wall -Wextra -Werror -pthread
RM = rm -f

SRC = main.c utils.c cycle.c queue.c dongles.c monitor.c \
	mutex_utils.c parser1_parse.c parser2_store.c parser3_init.c

OBJ = ${SRC:%.c=%.o}

all: $(NAME)

$(NAME): $(OBJ)
	$(CC) $(CFLAG) -o $(NAME) $(OBJ)

test:
	./codexion 5 500 50 50 50 3 50 fifo

val:
	valgrind ./codexion 5 500 50 50 50 3 50 fifo

hel:
	valgrind --tool=helgrind ./codexion 5 500 50 50 50 3 50 edf

clean:
	$(RM) $(OBJ)

fclean: clean
	$(RM) $(NAME)

re: fclean all

.PHONY: all clean fclean re test val hel
