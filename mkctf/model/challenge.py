# =============================================================================
#  IMPORTS
# =============================================================================
import tarfile
import tempfile
from stat import S_IRWXU
from pathlib import Path
from asyncio import create_subprocess_exec, wait_for, TimeoutError
from subprocess import PIPE, CalledProcessError
from jinja2 import Template
from mkctf.helper.fs import scandir
from mkctf.helper.log import app_log
from mkctf.cli.wizards import ChallengeConfigurationWizard
from mkctf.helper.checksum import ChecksumFile
from .config import ChallengeConfiguration
# =============================================================================
#  CLASSES
# =============================================================================
class Challenge:
    '''[summary]
    '''
    @classmethod
    def create(cls, repo, override_conf):
        final_conf = override_conf
        if not final_conf:
            wizard = ChallengeConfigurationWizard(override_conf)
            if not wizard.show():
                return
            final_conf = wizard.result
        chall_path = repo.challenges_dir.joinpath(final_conf['slug'])
        chall_path.mkdir(parents=True)
        conf = ChallengeConfiguration(repo.conf, chall_path.joinpath('.mkctf.yml'))
        conf.override(final_conf)
        conf.save()
        challenge = cls(repo, chall_path, conf)
        challenge.__create_files()
        return challenge

    def __init__(self, repo, chall_path, conf=None):
        '''Constructs a new instance
        '''
        self._repo = repo
        self._chall_path = chall_path
        self._config_file = chall_path.joinpath('.mkctf.yml')
        self._conf = conf or ChallengeConfiguration(repo.conf, self._config_file)

    @property
    def repo(self):
        return self._repo

    @property
    def conf(self):
        return self._conf

    @property
    def path(self):
        return self._chall_path

    @property
    def description(self):
        '''Retrieve challenge description from filesystem
        '''
        desc_path = self._chall_path.joinpath(self.repo.conf.description)
        if desc_path.is_file():
            return desc_path.read_text()
        return None

    def __create_dir(self, directory):
        '''Creates a directory
        '''
        dir_path = self._chall_path.joinpath(directory)
        if not dir_path.is_dir():
            dir_path.mkdir(parents=True, exist_ok=True)
            return True
        return False

    def __create_file(self, file):
        '''Creates a file
        '''
        name = file['name']
        exe = file.get('exec')
        template = file.get('from')
        filepath = self._chall_path.joinpath(name)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        content = "# mkCTF generated this file automatically without using a template\n"
        if template:
            tmpl_path = self.repo.template_dir.joinpath(template)
            if tmpl_path.is_file():
                tmpl = Template(tmpl_path.read_text())
                content = tmpl.render(repository=self.repo, challenge=self)
        if not filepath.is_file():
            with filepath.open('w') as fp:
                fp.write(content)
            if exe:
                filepath.chmod(S_IRWXU)
            return True
        return False

    async def __run(self, script, timeout):
        '''Runs a script as an asynchronous subprocess
        '''
        script_path = Path(script)
        script_parents = script_path.parents
        script = f'./{script_path.name}'
        if script_path.is_absolute():
            cwd = script_parents[0]
        else:
            cwd = self._chall_path
            if len(script_parents) > 1:
                cwd /= script_parents[0]
        app_log.info(f"running {script_path.name} within {cwd}.")
        proc = await create_subprocess_exec(script, stdout=PIPE, stderr=PIPE, cwd=str(cwd))
        rcode = -1
        stdout = None
        stderr = None
        exception = None
        try:
            stdout, stderr = await wait_for(proc.communicate(), timeout=timeout)
            rcode = proc.returncode
        except TimeoutError:
            proc.terminate()
            exception = 'timeout'
        except CalledProcessError as exc:
            proc.terminate()
            rcode = exc.returncode
            stdout = exc.stdout
            stderr = exc.stderr
            exception = 'called process error'
        except Exception as exc:
            exception = str(exc)
        if rcode == 0:
            app_log.info("subprocess terminated successfully.")
        else:
            app_log.warning(f"subprocess terminated unsuccessfully (rcode={rcode}).")
        return {
            'rcode': rcode,
            'stdout': stdout,
            'stderr': stderr,
            'exception': exception
        }

    def __create_files(self):
        '''Create challenge files
        '''
        self._chall_path.mkdir(parents=True, exist_ok=True)
        dir_list = self.repo.conf.directories(self.conf.category)
        for directory in dir_list:
            if not self.__create_dir(directory):
                app_log.warning(f"directory exists already: {directory}")
        file_list = self.repo.conf.files(self.conf.category)
        for file in file_list:
            if not self.__create_file(file):
                app_log.warning(f"file exists already: {file}")
        return True

    def export(self, export_dir, include_disabled):
        '''Export the challenge

        Creates an archive containing all of the challenge "exportable" files.
        '''
        if not include_disabled and not self.enabled:
            app_log.warning(f"export ignored {self.slug} (disabled)")
            return {'ignored': True}

        app_log.info(f"exporting {self.slug}...")
        archive_name = self.conf.static_url.split('/')[-1]
        if not archive_name:
            app_log.error(f"export ignored {self.slug} (invalid/empty static_url)")
            app_log.error(f"running `mkctf-cli update-meta` should be enough to fix this issue.")
            return {'ignored': True}

        archive_path = export_dir.joinpath(archive_name)
        checksum_file = ChecksumFile()
        with tarfile.open(str(archive_path), 'w:gz') as arch:
            for directory in self.repo.conf.directories(self.conf.category, public_only=True):
                dir_path = self._chall_path.joinpath(directory)
                for entry in scandir(dir_path):
                    entry_path = Path(entry.path)
                    if entry_path.is_dir():
                        app_log.warning(f"export ignored {entry_path} within {self.slug} (directory)")
                        continue
                    checksum_file.add(entry_path)
                    arch.add(str(entry_path), arcname=entry.name)
            with tempfile.NamedTemporaryFile('w') as tmpfile:
                tmpfile.write(checksum_file.content)
                arch.add(tmpfile, arcname='checksum.sha256')

        arch_checksum_file = ChecksumFile()
        arch_checksum_file.add(archive_path)
        export_dir.joinpath(f'{archive_name}.sha256').write_text(arch_checksum_file.content)
        app_log.info("done.")
        return archive_path

    async def build(self, timeout=4):
        '''Build the challenge
        '''
        return await self.__run(self.repo.conf.build, timeout)

    async def deploy(self, timeout=4):
        '''Deploy the challenge
        '''
        return await self.__run(self.repo.conf.deploy, timeout)

    async def healthcheck(self, timeout=4):
        '''Check the health of a deployed challenge
        '''
        return await self.__run(self.repo.conf.healthcheck, timeout)
