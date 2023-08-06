import json
import requests
from datetime import datetime
import nbformat
from tornado import web
from ..Fusion.REST import ApiClient

from notebook.services.contents.manager import ContentsManager
from notebook.services.contents.filecheckpoints import GenericCheckpointsMixin, Checkpoints
from traitlets import Any, Unicode, Bool, TraitError, observe, default, validate
from notebook.services.contents.filemanager import FileContentsManager


class TelexyCMCheckpoints(GenericCheckpointsMixin, Checkpoints):
    """requires the following methods:"""
    def create_file_checkpoint(self, content, format, path):
        """ -> checkpoint model"""
        print('create file checkpoint ')
        """Create a checkpoint from the current content of a file."""
        path = path.strip('/')
        # only the one checkpoint ID:
        checkpoint_id = u"checkpoint"

        return dict(
            id=checkpoint_id,
            last_modified=datetime.utcnow(),
            format=format,
            path=path
        )

    def create_notebook_checkpoint(self, nb, path):
        """ -> checkpoint model"""
        print('create notebook checkpoint ' + nb)

    def get_file_checkpoint(self, checkpoint_id, path):
        """ -> {'type': 'file', 'content': <str>, 'format': {'text', 'base64'}}"""
        print('get file checkpoint ' + checkpoint_id + ' ' + path)

    def get_notebook_checkpoint(self, checkpoint_id, path):
        """ -> {'type': 'notebook', 'content': <output of nbformat.read>}"""
        print('get notebook checkpoint ' + checkpoint_id + ' ' + path)

    def delete_checkpoint(self, checkpoint_id, path):
        """deletes a checkpoint for a file"""

    def list_checkpoints(self, path):
        """returns a list of checkpoint models for a given file,
        default just does one per file
        """
        print('listing checkpoints')
        return []
    def rename_checkpoint(self, checkpoint_id, old_path, new_path):
        """renames checkpoint from old path to new path"""
        print('renaming checkpoints')


class TelexyContentManager(ContentsManager):
    """Telexy content manager for jupyter"""


    @default('checkpoints_class')
    def _checkpoints_class_default(self):
        return TelexyCMCheckpoints

    def dir_exists(self, path):
        print(path)
        """Does a directory exist at the given path?

        Like os.path.isdir

        Override this method in subclasses.

        Parameters
        ----------
        path : string
            The path to check

        Returns
        -------
        exists : bool
            Whether the path does indeed exist.
        """
        return True

    def is_hidden(self, path):
        print(path)
        """Is path a hidden directory or file?

        Parameters
        ----------
        path : string
            The path to check. This is an API path (`/` separated,
            relative to root dir).

        Returns
        -------
        hidden : bool
            Whether the path is hidden.

        """
        return False

    def file_exists(self, path=''):
        print(path)
        """Does a file exist at the given path?

        Like os.path.isfile

        Override this method in subclasses.

        Parameters
        ----------
        path : string
            The API path of a file to check for.

        Returns
        -------
        exists : bool
            Whether the file exists.
        """
        return True

    def get(self, path, content=True, type=None, format=None):
        print('GET: ' + path)
        """Get a file or directory model."""
        api = ApiClient("http://192.168.0.11/cmjupyter")
        if(content==True):
            req = api.Post("/get", {'path': path })
        else:
            req = api.Post("/get", {'path': path, 'content': 'false'})
        return req.json()

    def save(self, model, path):
        print("saving")
        """
        Save a file or directory model to path.
        Should return the saved model with no content.  Save implementations
        should call self.run_pre_save_hook(model=model, path=path) prior to
        writing any data.
        """
        self.run_pre_save_hook(model, path)
        print(model)
        print(path)
        return None

    def delete_file(self, path):
        """Delete the file or directory at path."""
        return None

    def rename_file(self, old_path, new_path):
        print(old_path)
        print(new_path)
        """Rename a file or directory."""
        return None