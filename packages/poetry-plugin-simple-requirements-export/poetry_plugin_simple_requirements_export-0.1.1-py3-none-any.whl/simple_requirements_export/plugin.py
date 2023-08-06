from poetry.plugins import ApplicationPlugin

from simple_requirements_export.command import SimpleRequirementsExportCommand


def factory():
    return SimpleRequirementsExportCommand()


class SimpleRequirementsExportPlugin(ApplicationPlugin):
    def activate(self, application):
        application.command_loader.register_factory(SimpleRequirementsExportCommand.name, factory)
