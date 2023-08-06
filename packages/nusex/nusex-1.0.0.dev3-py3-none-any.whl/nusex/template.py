# Copyright (c) 2021, Ethan Henderson
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
from pathlib import Path

from nusex import TEMP_DIR, TEMPLATE_DIR
from nusex.builders import PythonBuilder
from nusex.errors import BuildError, TemplateError
from nusex.helpers import run, validate_name
from nusex.spec import NSXSpecIO

ATTRS = (
    "PROJECTNAME",
    "PROJECTAUTHOR",
    "PROJECTAUTHOREMAIL",
    "PROJECTURL",
    "PROJECTVERSION",
    "PROJECTDESCRIPTION",
    "PROJECTLICENSE",
    "PROJECTYEAR",
    "LICENSEBODY",
    "PROJECTBASEEXC",
)


class Template:
    """A class in which to create, load, modify, and save templates.

    Args:
        name (str): The name of the template. If the template does not
            exist, a new one is created, otherwise an existing one is
            loaded.

    Keyword Args:
        installs (list[str]): A list of dependancies to be installed
            when the template is deployed.

    Attributes:
        path (pathlib.Path): The complete filepath to the template.
        data (dict[str, Any]): The data for the template.
        installs (list[str]): A list of dependencies the template will
            install when deployed.
    """

    __slots__ = ("path", "data", "installs")

    def __init__(self, name, *, installs=[]):
        self.path = TEMPLATE_DIR / f"{name}.nsx"
        self.installs = installs

        if not os.path.isfile(self.path):
            return self.create_new(name)

        self.load()

    def __str__(self):
        return self.path.stem

    def __repr__(self):
        return (
            f"<Template name={self.name!r} files={len(self.data['files'])!r}>"
        )

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name

    def __getitem__(self, key):
        return self.data["files"][key]

    @property
    def name(self):
        """The name of the template.

        Returns:
            str
        """
        return self.path.stem

    @property
    def exists(self):
        """Whether the template exists on disk.

        Returns:
            bool
        """
        return self.path.is_file()

    def create_new(self, name):
        """Create a new template.

        Args:
            name (str): The name of the template.
        """
        validate_name(name, self.__class__.__name__)
        self.data = {
            "files": {},
            "installs": [],
            "as_extension_for": "",
        }

    def load(self):
        """Load an existing template. This should never need to be
        called as templates are loaded automatically when necessary upon
        object creation.

        Raises:
            FileNotFoundError: The template does not exist on disk.
        """
        self.data = NSXSpecIO().read(self.path)

    def save(self):
        """Save this profile.

        Raises:
            TemplateError: The profile data has been improperly
                modified.
        """
        try:
            NSXSpecIO().write(self.path, self.data)
        except KeyError:
            raise TemplateError(
                "The template data has been improperly modified"
            ) from None

    def delete(self):
        """Delete this template.

        Raises:
            FileNotFoundError: The template does not exist on disk.
        """
        os.remove(self.path)

    def rename(self, new_name):
        """Rename this template.

        Args:
            new_name (str): The new name for the template.

        Raises:
            FileNotFoundError: The template does not exist on disk.
        """
        new_path = f"{self.path}".replace(self.path.stem, new_name)
        self.path = self.path.rename(new_path)

    @classmethod
    def from_cwd(cls, name, *, ignore_exts=set(), ignore_dirs=set()):
        """Create a template using files from the current working
        directory.

        Args:
            name (str): The name of the template.

        Keyword Args:
            ignore_exts (set[str]): A set of file extensions to ignore.
                Defaults to an empty set.
            ignore_dirs (set[str]): A set of directories to ignore.
                Defaults to an empty set.

        Returns:
            Template: The newly created template.
        """
        c = cls(name)
        c.build(
            ignore_exts=ignore_exts,
            ignore_dirs=ignore_dirs,
        )
        return c

    @classmethod
    def from_dir(cls, name, path, *, ignore_exts=set(), ignore_dirs=set()):
        """Create a template using files from a specific directory.

        Args:
            name (str): The name of the template.
            path (str | os.PathLike): The path to the files to build the
                template with.

        Keyword Args:
            ignore_exts (set[str]): A set of file extensions to ignore.
                Defaults to an empty set.
            ignore_dirs (set[str]): A set of directories to ignore.
                Defaults to an empty set.

        Returns:
            Template: The newly created template.
        """
        c = cls(name)
        c.build(
            root_dir=path,
            ignore_exts=ignore_exts,
            ignore_dirs=ignore_dirs,
        )
        return c

    @classmethod
    def from_repo(cls, name, url, *, ignore_exts=set(), ignore_dirs=set()):
        """Create a template using files from a GitHub repository.

        Args:
            name (str): The name of the template.
            url (str): The URL of the GitHub repository to clone.

        Keyword Args:n
            ignore_exts (set[str]): A set of file extensions to ignore.
                Defaults to an empty set.
            ignore_dirs (set[str]): A set of directories to ignore.
                Defaults to an empty set.

        Returns:
            Template: The newly created template.

        Raises:
            BuildError: Cloning the repository failed.
        """
        os.makedirs(TEMP_DIR, exist_ok=True)
        os.chdir(TEMP_DIR)

        output = run(f"git clone {url}")
        if output.returncode == 1:
            raise BuildError(
                "Cloning the repo failed. Is Git installed? Is the URL "
                "correct?"
            )

        os.chdir(TEMP_DIR / url.split("/")[-1].replace(".git", ""))
        return cls.from_cwd(
            name, ignore_exts=ignore_exts, ignore_dirs=ignore_dirs
        )

    def get_file_listing(
        self, root_dir, *, ignore_exts=set(), ignore_dirs=set()
    ):
        """Get a list of files to include in this template.

        Args:
            root_dir (str): The root directory that nusex will search
                from.

        Keyword Args:
            ignore_exts (set[str]): A set of file extensions to ignore.
                Defaults to an empty set.
            ignore_dirs (set[str]): A set of directories to ignore.
                Defaults to an empty set.

        Returns:
            list[Path]: A list of filepaths.
        """

        def is_valid(path):
            return (
                path.is_file()
                and all(i not in path.parts for i in true_dir_ignores)
                and all(i[1:] not in f"{path}" for i in wild_dir_ignores)
                and all(i != path.suffix[1:] for i in ignore_exts)
            )

        wild_dir_ignores = set(
            filter(lambda x: x.startswith("*"), ignore_dirs)
        )
        true_dir_ignores = ignore_dirs - wild_dir_ignores
        files = filter(lambda p: is_valid(p), Path(root_dir).rglob("*"))
        return list(files)

    def build(self, project_name=None, files=[], root_dir=".", **kwargs):
        """Build this template. View the
        :doc:`template guide <../guide/templates>` to see what this
        command does in more detail.

        Keyword Args:
            project_name (str): The name of the project. If this is None
                the project name is set to the name of the parent
                folder. Defaults to None.
            files (list[str]): The list of files to include in this
                template. If no files are specified, the file listing
                is automatically retrieved.
            root_dir (str): The root directory that nusex will search
                from. Defaults to the current directory.
            **kwargs (Any): Arguments for the :code:`get_file_listing`
                method.
        """

        def resolve_key(path):
            path = "/".join(f"{path.resolve()}".split(os.sep)[nparts:])
            return path.replace(project_name, "PROJECTNAME")

        if not project_name:
            project_name = Path(root_dir).resolve().parts[-1]

        if not files:
            files = self.get_file_listing(
                root_dir,
                ignore_exts=kwargs.pop("ignore_exts", set()),
                ignore_dirs=kwargs.pop("ignore_dirs", set()),
            )

        nparts = len(Path(root_dir).resolve().parts)
        data = {
            "files": {resolve_key(f): f.read_bytes() for f in files},
            "installs": self.installs,
            "as_extension_for": "",
        }

        builder = PythonBuilder(project_name, data)
        self.data = builder().data

    def check(self):
        """Check the template manifest, including line changes.

        Returns:
            dict[str, list[tuple[int, str]]]: The template manifest. The
            keys are always file names, and the values are tuples
            of the line numbers and line values that have been changed.
            This may not always be present.
        """
        manifest = {}

        for file, data in self.data["files"].items():
            manifest.update({file: []})

            try:
                for i, line in enumerate(data.decode().split("\n")):
                    if any(a in line for a in ATTRS):
                        manifest[file].append((i + 1, line))
            except UnicodeDecodeError:
                # If it errors here, no modifications could have been
                # made.
                ...

        return manifest
