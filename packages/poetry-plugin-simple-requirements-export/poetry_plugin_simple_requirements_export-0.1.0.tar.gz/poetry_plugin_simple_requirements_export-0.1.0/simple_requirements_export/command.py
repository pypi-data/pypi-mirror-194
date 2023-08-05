from pathlib import Path
from tempfile import TemporaryDirectory

import tomli
from poetry.console.commands.group_command import GroupCommand
from poetry_plugin_export.exporter import Exporter


class SimpleRequirementsExportCommand(GroupCommand):

    name = "simple-requirements"

    def handle(self):
        bare_dependencies = self.get_original_dependencies()

        dependencies_in_pyproject = self.get_toml_dependencies()

        with open("requirements.txt", "w") as requirements_file:
            for dependency in dependencies_in_pyproject:
                if dependency in bare_dependencies:
                    requirements_file.write(bare_dependencies[dependency] + "\n")

        return 0

    def get_toml_dependencies(self):
        with open("pyproject.toml", "rb") as f:
            pyproject = tomli.load(f)
            dependencies_in_pyproject = sorted(pyproject["tool"]["poetry"]["dependencies"])
        return dependencies_in_pyproject

    def get_original_dependencies(self):
        # Piggybacking on the existing export command
        # by exporting the lock file to a temporary requirements.txt
        exporter = Exporter(self.poetry, self.io)
        exporter.with_hashes(False)
        bare_dependencies = {}
        with TemporaryDirectory() as tmp_dir:
            exporter.export("requirements.txt", Path(tmp_dir), "requirements.txt")

            with open(Path(tmp_dir) / "requirements.txt", "r") as requirements_file:
                for requirement_line in requirements_file:
                    dependency, _, extras = requirement_line.partition(";")
                    dependency_name, _, version = dependency.partition("==")
                    bare_dependencies[dependency_name] = dependency.strip()
        return bare_dependencies
