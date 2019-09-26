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
import click

logger = logging.getLogger('fzf')

# get all get_all_documents

@click.help_option('--help', '-h')
@click.version_option(version=papis.__version__)
@click.option(
    "--libraries",
    help="List defined libraries",
    default=False,
    is_flag=True
)
def main(libraries):
    lib = papis.config.get_lib()
    print(lib)
    config = papis.config.get_configuration()
    logger = logging.getLogger('cli:list')
    db = papis.database.get(library)
    documents = db.get_all_documents()
    print(documents)


    pick_doc()

    documents = papis.database.get_all_query_string()
    # documents = papis.database.get().query(query)
    print("Documents", documents)
    cmd = ['fzf', ]

    # add a custom FZF_PREVIEW etc ?
    # or wrap it
    customEnv = copy.copy(os.environ)
    # stdout=, 
    # stdin="todo\nlala" 
    # stdout=subprocess.PIPE,

    with subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            universal_newlines=True,  # opens in text mode
                            ) as proc:
        out = subprocess.Popen(cmd, shell=True)

