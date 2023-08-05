# Jupyter Extension points
def _jupyter_nbextension_paths():
    return [dict(
        section="notebook",
        src="static",
        # directory in the `nbextension/` namespace
        dest="writefile",
        # _also_ in the `nbextension/` namespace
        require="writefile/main")]

def load_jupyter_server_extension(nbapp):
    nbapp.log.info("my module enabled!")