ANTLR=java -Xmx500M -cp "$(ANTLR_PATH):$(CLASSPATH)" org.antlr.v4.Tool
MYPY=mypy
MYPY_OPTS=--follow-imports silent
PYTHON=python

TYPECHECK=parser.py ast.py

all: parser

parser:
	$(ANTLR) -Dlanguage=Python3 -visitor FG.g4

typecheck:
	$(MYPY) $(MYPY_OPTS) $(TYPECHECK)

clean:
	rm -f *.tokens FGLexer.py FGListener.py FGParser.py FGVisitor.py

.PHONY: all clean typecheck
