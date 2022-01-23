from rich import print as rprint
import os
import subprocess
from subprocess import PIPE
import pathlib
import logging
log_format = '%(asctime)s %(filename)s: %(message)s'
logging.basicConfig(filename='app.log', level=logging.DEBUG, format=log_format, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

_default_dsop_rke2_repo = "https://github.com/cheruvu1/dsop-rke2"

class Stream:
    def __init__(self, repo_name:str="dsop_rke2", working_dir:str="working", base_dir:str=""):
        self.repo_name = repo_name
        self.working_dir = working_dir
        self.base_dir = base_dir

    def cout(self, text: str):
        rprint(text)

    def Do_No_VNet_Customization(self ):
        dir = f"{self.base_dir}/{self.working_dir}/{self.repo_name}"
        self._clone_env_repo(False)

    def do_rename_terraform_file(self):
        dir = f"{self.base_dir}/{self.working_dir}/{self.repo_name}"
        logger.debug(f"Renaming TF_File: '{dir}/example/terraform.tfvars.sample' To '{dir}/example/terraform.tfvars'")
        if os.path.isfile(f"\"{dir}/example/terraform.tfvars\"") == False:
            logger.debug(f"Copying File: {dir}/example/terraform.tfvars.sample -> {dir}/example/terraform.tfvars")
            res = self._run_process(["cp", f"{dir}/example/terraform.tfvars.sample", f"{dir}/example/terraform.tfvars"]) 

    def do_terraform_destroy(self):
        res = self._run_process(['terraform', f"-chdir={self.working_dir}/{self.repo_name}/example" ,'destroy'])

    def do_vnet_customization():
        pass

    def do_cloud_login(self):
        logger.debug("Setting up Azure Cloud")
        res = self._run_process(['az','cloud', 'set', '--name', 'AzureUSGovernment'])
        res = self._run_process(['az','login'])
        res = self._run_process(['az','cloud', 'list', '-o', 'table'])

    def do_run_terraform(self):
        logger.debug("Running Terraform")
        self._run_terraform_init()
        self._run_terraform()


    def _cout_error(self, text: str):
        rprint(f"[italic red]{text}[/italic red]")

    def _cout_success(self, text: str):
        rprint(f"[green]{text}[/green]")


    def _clone_env_repo(self, dsop_customization_required: bool):
        args = ['git', 'clone', _default_dsop_rke2_repo, f"{self.working_dir}/{self.repo_name}"]
        res = self._run_process(args)

    def run_console(self, ):
        res = self._run_process(['ls', '-l', '-a'],True)
        res = self._run_process(['echo', 'Hello', 'World!'],True)


    def _run_terraform_init(self):
        res = self._run_process(['terraform', f"-chdir={self.working_dir}/{self.repo_name}/example" ,'init'])

    def _run_terraform(self):
        work_dir = f"{self.base_dir}/{self.working_dir}/{self.repo_name}/example"
        args = ['terraform', f"-chdir={work_dir}", 'apply', '-auto-approve']
        res = self._run_process(args)
        

    def _run_process(self, args:list, read_output:bool=False, cwd:str=""):
        logger.debug(f"Running process: {locals()}")
        if cwd.strip() == "":
            result = subprocess.run(args, capture_output=False, text=True)
        else:
            result = subprocess.run(args, capture_output=True, text=True, cwd=cwd )
            return result.stdout

if __name__ == '__main__':
    _stream = Stream()
    _stream.run_console()