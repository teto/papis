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
import io

logger = logging.getLogger('fzf')

# get all get_all_documents
@click.group(
    invoke_without_command=True
)
@click.help_option('--help', '-h')
@click.version_option(version=papis.__version__)
# @click.option(
#     "--libraries",
#     help="List defined libraries",
#     default=False,
#     is_flag=True
# )
@click.option(
    "-l",
    "--lib",
    help="Choose a library name or library path (unamed library)",
    default=lambda: papis.config.get("default-library")
)
@click.option(
    "-c",
    "--config",
    help="Configuration file to use",
    default=None,
)
@click.option(
    "--log",
    help="Logging level",
    type=click.Choice(["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]),
    default="INFO"
)
@click.option(
    "--pick-lib",
    help="Pick library to use",
    default=False,
    is_flag=True
)
def run(
        config,
        log,
        lib,
        pick_lib
        ):
    lib = papis.config.get_lib()
    print(lib)
    config = papis.config.get_configuration()
    logger = logging.getLogger('cli:list')

    library = papis.config.get_lib()

    db = papis.database.get(library)

    # todo run a search on 
    # "Slave diversity: Using multiple paths to improve the accuracy of clock synchronization protocols
    # documents = db.get_all_documents()

    query = "Slave"
    documents = papis.database.get().query(query)
    if not documents:
        logger.warning(papis.strings.no_documents_retrieved_message)
        return 0
    # print(documents)


    # documents = papis.database.get_all_query_string()
    # documents = papis.database.get().query(query)
    # print("Documents", documents)
    # --with-nth
    # https://unix.stackexchange.com/questions/527163/fzf-how-to-return-id-line-numbers
    # -nth to limit search scope
    cmd = ['fzf', "--prompt=pick a doc>",
            '-d\|',
            '--with-nth=3',
            # use the preview
            # To transform the replacement string, specify field index expressions between the braces
            '--preview=cat {2}'
            ]

    # add a custom FZF_PREVIEW etc ?
    # or wrap it
    customEnv = copy.copy(os.environ)
    # stdout=, 
    # stdin="todo\nlala" 
    # stdout=subprocess.PIPE,

    # docs_fd = io.StringIO()
    # docs_fd.write("toto")
    # docs_fd.write("matt")


    # 
    header_format_path = papis.config.get('header-format-file')
    if header_format_path is not None:
        with open(os.path.expanduser(header_format_path)) as fd:
            header_format = fd.read()
    else:
        header_format = papis.config.get("header-format")

    # {doc[first_name]} {doc[last_name]}
    header_format = "{doc[title]}"
    print("Using header_format: %s" % header_format)

    print(documents[0])

    # -m for multi select
    with subprocess.Popen(
        cmd,
        # stdin=docs_fd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True,  # opens in text mode
        ) as proc:

        for i, doc in enumerate(documents[1:3]):
            formatted_doc = papis.utils.format_doc(header_format, doc)
            print(formatted_doc)
            line = "|".join([
                str(i),
                doc.get_info_file(),
                formatted_doc
                ])
            proc.stdin.write(line)
        # proc.stdin.write("o2:Matt\n")
        # proc.stdin.close()

        try:
            outs, errs = proc.communicate(timeout=15)

            print("communicated")
            print(outs)
        except subprocess.TimeoutExpired:
            print("TIMED OUT")

    # check how many documents were select

    available_cmds = papis.commands.get_scripts()
    print(available_cmds)
    # exit(1)

    print("What to do with this document ?")
    cmd = ['fzf', "--prompt=What to do>",
            # '-d\|',
            # '--with-nth=3',
            # use the preview
            # To transform the replacement string, specify field index expressions between the braces
            # '--preview=cat {2}'
            ]
    with subprocess.Popen(
        cmd,
        # stdin=docs_fd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True,  # opens in text mode
        ) as proc:

        # if there are several than "remove all"
        for i, cmd in enumerate(available_cmds.keys()):
            proc.stdin.write("{}\n".format(cmd))

