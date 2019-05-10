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
from mkctf.cli.wizard import ChallengeConfigurationWizard
from mkctf.helper.checksum import ChecksumFile
from .config import ChallengeConfiguration
# =============================================================================
#  CLASSES
# =============================================================================
class Challenge:
    '''[summary]
    '''
    def __init__(self, repo, path, conf=None):
        '''Constructs a new instance
        '''
        self._conf = conf
        self._repo = repo
        self._path = path
        self._conf_path = path.joinpath('.mkctf.yml')
        if not conf:
            self._conf = ChallengeConfiguration.load(self._conf_path)
            self._conf.validate()

    @property
    def conf(self):
        return self._conf

    @property
    def repo(self):
        return self._repo

    @property
    def path(self):
        return self._path

    @property
    def description(self):
        '''Retrieve challenge description from filesystem
        '''
        desc_path = self.path.joinpath(self.repo.conf.description)
        if desc_path.is_file():
            return desc_path.read_text()
        return None

    def _save_conf(self):
        '''Save challenge configuration to disk
        '''
        if not self._conf.validate(throw=False):
            app_log.error("save operation aborted: invalid configuration")
            return False
        self._conf.save(self._conf_path)
        return True

    def _create_dir(self, directory):
        '''Creates a directory
        '''
        dir_path = self.path.joinpath(directory)
        if not dir_path.is_dir():
            dir_path.mkdir(parents=True, exist_ok=True)
            return True
        return False

    def _create_file(self, file):
        '''Creates a file
        '''
        name = file['name']
        exe = file.get('exec')
        template = file.get('from')
        filepath = self.path.joinpath(name)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        content = "# mkCTF generated this file automatically without using a template\n"
        if template:
            tmpl_path = self.repo.template_dir.joinpath(template)
            if tmpl_path.is_file():
                tmpl = Template(tmpl_path.read_text())
                try:
                    content = tmpl.render(repo_conf=self.repo.conf, chal_conf=self.conf)
                except:
                    content = tmpl_path.read_text()
                    app_log.exception(f"{filepath} rendering failed, copying template content instead...")
        if not filepath.is_file():
            with filepath.open('w') as fp:
                fp.write(content)
            if exe:
                filepath.chmod(S_IRWXU)
            return True
        return False

    async def _run(self, script, dev, timeout):
        '''Runs a script as an asynchronous subprocess
        '''
        script_path = Path(script)
        script_parents = script_path.parents
        script = f'./{script_path.name}'
        if script_path.is_absolute():
            cwd = script_parents[0]
        else:
            cwd = self.path
            if len(script_parents) > 1:
                cwd /= script_parents[0]
        app_log.info(f"running {script_path.name} within {cwd}.")
        if dev:
            proc = await create_subprocess_exec(script, '--dev', stdout=PIPE, stderr=PIPE, cwd=str(cwd))
        else:
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

    def init(self):
        '''Create challenge files
        '''
        self.path.mkdir(parents=True, exist_ok=True)
        dir_list = self.repo.conf.directories(self.conf.category)
        for directory in dir_list:
            if not self._create_dir(directory):
                app_log.warning(f"directory exists already: {directory}")
        file_list = self.repo.conf.files(self.conf.category)
        for file in file_list:
            if not self._create_file(file):
                app_log.warning(f"file exists already: {file}")
        return self._save_conf()

    def configure(self, override_conf=None):
        final_conf = override_conf
        if not final_conf:
            wizard = ChallengeConfigurationWizard(self.conf)
            if not wizard.show():
                return False
            final_conf = wizard.result
        self._conf = final_conf
        return self._save_conf()

    def enable(self, enabled):
        '''Enable or disable the challenge
        '''
        self._conf['enabled'] = enabled
        self._save_conf()

    def renew_flag(self, size):
        '''Replace current flag by a randomly generated one
        '''
        flag = self.repo.conf.make_rand_flag(size)
        self._conf['flag'] = flag
        self._save_conf()
        return flag

    def update_static_url(self):
        '''Update challenge static url in configuration if required
        '''
        static_url = self.repo.conf.make_static_url(self.conf.slug)
        if self.conf.static_url != static_url:
            self._conf['static_url'] = static_url
            self._save_conf()
        return static_url

    def export(self, export_dir, include_disabled):
        '''Export the challenge

        Creates a gzipped tar archive containing all of the challenge "exportable" files
        '''
        if not include_disabled and not self.conf.enabled:
            app_log.warning(f"export ignored {self.conf.slug} (disabled)")
            return {'ignored': True}

        app_log.info(f"exporting {self.conf.slug}...")
        archive_name = self.conf.static_url.split('/')[-1]
        if not archive_name:
            app_log.error(f"export ignored {self.conf.slug} (invalid/empty static_url)")
            app_log.error(f"running `mkctf-cli update-meta` should be enough to fix this issue.")
            return {'ignored': True}

        archive_path = export_dir.joinpath(archive_name)
        checksum_file = ChecksumFile()
        with tarfile.open(str(archive_path), 'w:gz') as arch:
            for directory in self.repo.conf.directories(self.conf.category, public_only=True):
                dir_path = self.path.joinpath(directory)
                for entry in scandir(dir_path):
                    entry_path = Path(entry.path)
                    if entry_path.is_dir():
                        app_log.warning(f"export ignored {entry_path} within {self.conf.slug} (directory)")
                        continue
                    checksum_file.add(entry_path)
                    app_log.debug(f"adding {entry_path} to archive...")
                    arch.add(str(entry_path), arcname=entry.name)
            with tempfile.NamedTemporaryFile('w') as tmpfile:
                tmpfile.write(checksum_file.content)
                tmpfile.flush()
                app_log.debug(f"adding checksum.sha256 to archive...")
                arch.add(tmpfile.name, arcname='checksum.sha256')

        arch_checksum_file = ChecksumFile()
        arch_checksum_file.add(archive_path)
        export_dir.joinpath(f'{archive_name}.sha256').write_text(arch_checksum_file.content)
        return archive_path

    async def build(self, dev=False, timeout=4):
        '''Build the challenge
        '''
        return await self._run(self.repo.conf.build, dev, timeout)

    async def deploy(self, dev=False, timeout=4):
        '''Deploy the challenge
        '''
        return await self._run(self.repo.conf.deploy, dev, timeout)

    async def healthcheck(self, dev=False, timeout=4):
        '''Check the health of a deployed challenge
        '''
        return await self._run(self.repo.conf.healthcheck, dev, timeout)
