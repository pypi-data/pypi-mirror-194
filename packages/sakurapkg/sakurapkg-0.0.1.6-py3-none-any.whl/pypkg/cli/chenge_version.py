import toml
from cleo.commands.command import Command
from cleo.helpers import argument, option
import logging, os

logger = logging.getLogger(__name__)
logging.basicConfig()

class chenge_version(Command):
    name = "chenge-version"
    description = "chenge version"
    options = [
        option(
            "testing",
            "t",
            description="install testing version sakurapkg",
            flag=True
        ),
        option(
            "release",
            "r",
            description="install testing version sakurapkg",
            flag=True
        )
    ]

    def handle(self):
      if self.option("testing"):
	      subprocess.Popen("pip install git+https://github.com/sonyakun/sakurapkg@Testing", shell=True)
      elif self.option("release"):
        subprocess.Popen("pip install sakurapkg", shell=True)
