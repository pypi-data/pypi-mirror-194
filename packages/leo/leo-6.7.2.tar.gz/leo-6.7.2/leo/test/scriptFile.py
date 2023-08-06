#@+leo-ver=5-thin
#@+node:ekr.20131016083406.16724: * @button make-sphinx
"""
Run this script from the `gh-pages` branch.

1. Generate intermediate files for all headlines in the table.
2. Run `make clean` and `make html` from the leo/doc/html directory.

After running this script, copy files from leo/doc/html/_build/html to leo-editor/docs
"""


g.cls()
import os
trace = False
headlines = [
    "Leo's Documentation"
]

#@+others  # define helpers
#@+node:ekr.20230111164618.1: ** get_paths
def get_paths():
    """
    Return paths to leo-editor/leo/doc/html and leo-editor/docs.
    """
    docs_path = g.os_path_finalize_join(g.app.loadDir,'..','..','docs')
    if not os.path.exists(docs_path):
        g.es_print(f"Not found: {docs_path!r}")
        return None, None
    html_path = g.os_path_finalize_join(g.app.loadDir,'..','doc','html')
    if not os.path.exists(html_path):
        g.es_print(f"Not found: {html_path!r}")
        return None, None
    return docs_path, html_path
#@+node:ekr.20230228105847.1: ** run
def run():

    if g.gitBranchName() != 'gh-pages':
        g.es_print('Run `make-sphinx` from `gh-pages` branch')
        return

    old_p = c.p
    try:
        docs_path, html_path = get_paths()
        if html_path:
            os.chdir(html_path)
            if write_intermediate_files():
                g.execute_shell_commands([
                    'make clean',
                    'make html',
                    'echo.',
                    'echo copy files from html/_build/html to /docs',
                ],trace=trace)
    finally:
        c.selectPosition(old_p)
#@+node:ekr.20230111165336.1: ** write_intermediate_files
def write_intermediate_files():
    for headline in headlines:
        p = g.findTopLevelNode(c, headline)
        if p:
            c.selectPosition(p)
            c.rstCommands.rst3()
        else:
            g.es_print(f"Not found: {headline!r}")
            return False
    return True
#@-others

if c.isChanged():
    c.save()
run()

#@-leo
