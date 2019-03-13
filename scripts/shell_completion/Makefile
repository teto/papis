
all: dist/bash-completion.sh

dist/bash-completion.sh:
	./tools/bash.sh

zsh:
	# from a zsh shell
	# prepend a "#compdef papis" directive
	echo "#compdef papis" > _papis
	_PAPIS_COMPLETE=source_zsh papis >> _papis

clean:
	rm -rf dist
