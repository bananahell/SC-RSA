#################################
##### Linux Makefile
#################################

##### Compiler
COMPILER = cc
##### Remove directories
RMDIR = rm -rdf
##### Remove files
RM = rm -f

##### Automatic dependency creation
DEP_FLAGS = -M -MT $@ -MT $(BIN_PATH)/$(*F).o -MP -MF $@
##### Linked libraries
LIBS =
##### Include path
INC_PATHS = -I$(INC_PATH)

##### Compile directives
FLAGS = -ansi -Wall -pedantic -Wextra -Werror=init-self -lm
##### Extra debugging directives
DFLAGS = -ggdb -O0 -DDEBUG -g
##### Extra release directives
RFLAGS = -O0

INC_PATH = include
SRC_PATH = src
BIN_PATH = bin
DEP_PATH = dep

##### File list by type
C_FILES = $(wildcard $(SRC_PATH)/*.c)
INC_FILES = $(wildcard $(INC_PATH)/*.h)
FILE_NAMES = $(sort $(notdir $(C_FILES:.c=)) $(notdir $(INC_FILES:.h=)))
DEP_FILES = $(addprefix $(DEP_PATH)/,$(addsuffix .d,$(FILE_NAMES)))
OBJ_FILES = $(addprefix $(BIN_PATH)/,$(notdir $(C_FILES:.c=.o)))

##### Executable name
EXEC = program.out

.PRECIOUS: $(DEP_FILES)
.PHONY: release debug cppcheck clean folders help valgrind doItAll

##### Generates executable
$(EXEC): $(OBJ_FILES)
	$(COMPILER) -o $@ $^ $(LINK_PATH) $(LIBS) $(FLAGS)

##### Generates object files
$(BIN_PATH)/%.o: $(DEP_PATH)/%.d | folders
	$(COMPILER) $(INC_PATHS) $(addprefix $(SRC_PATH)/,$(notdir $(<:.d=.c))) -c $(FLAGS) -o $@

##### Generates dependency files
$(DEP_PATH)/%.d: $(SRC_PATH)/%.c | folders
	$(COMPILER) $(INC_PATHS) $< $(DEP_FLAGS) $(FLAGS)

clean:
	-$(RMDIR) $(DEP_PATH)
	-$(RMDIR) $(BIN_PATH)
	-$(RM) $(EXEC)

execute:
	./$(EXEC)

##### Call for cppcheck
cppcheck:
	cppcheck --enable=all . -I./include --suppress=missingIncludeSystem

##### Call for valgrind
valgrind:
	valgrind --leak-check=yes -s ./$(EXEC)

doItAll:
	make clean && make debug && make cppcheck && make valgrind

release: FLAGS += $(RFLAGS)
release: $(EXEC)

debug: FLAGS += $(DFLAGS)
debug: $(EXEC)

folders:
	@mkdir -p $(DEP_PATH) $(BIN_PATH) $(INC_PATH) $(SRC_PATH)

##### Debugging rules
print-% : ; @echo $* = $($*)

help:
	@echo Available commands
	@echo - release:  Builds release version
	@echo - debug:    Builds debug version
	@echo - clean:    Cleans generated files
	@echo - cppcheck: Uses cppcheck on compiled objects
	@echo - valgrind: Uses valgrind on linked programs
	@echo - help:     Shows help
	@echo - folders:  Generates project directories

.SECONDEXPANSION:
-include $$(DEP_FILES)