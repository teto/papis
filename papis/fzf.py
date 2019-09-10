import os
import difflib
import sys
import papis
import papis.api
import papis.config
import papis.commands
import papis.database
import colorama
import logging
import subprocess
import copy


logger = logging.getLogger('fzf')

# get all get_all_documents


def main():

    documents = papis.database.get_all_query_string()
    # documents = papis.database.get().query(query)
    print("Documents", documents)
    cmd = ['fzf', ]

    # add a custom FZF_PREVIEW etc ?
    # or wrap it
    customEnv = copy.copy(os.environ)
    # stdout=, 
    subprocess.check_output(cmd, stdin="todo\nlala" , shell=True)

