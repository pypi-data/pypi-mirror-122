import subprocess
import sys
from pip_chill import chill
from pkg_resources import Requirement
import yaml

from spell.api.models import RunRequest
from spell.shared.projects import get_project_by_name


FRAMEWORK_PACKAGES = {
    "tensorflow",
    "keras",
    "pytorch",
    "torchvision",
    "pytorch-lightning",
    "requests",
    "pandas",
    "numpy",
    "matplotlib",
    "scikit-learn",
    "xgboost",
    "spell",
}


def get_base_prefix_compat():
    """Get base/real prefix, or sys.prefix if there is none."""
    return getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix


def in_virtualenv():
    return get_base_prefix_compat() != sys.prefix


class NoEnvFound(RuntimeError):
    message = "Could not find an active conda environment or virtualenv"


class NoVirtualEnvFound(NoEnvFound):
    message = "Could not find an active virtualenv"


class InvalidDependencyConfig(Exception):
    def __init__(self, message):
        self.message = message


class PythonDependencies:
    def __init__(self, pip_env=None, requirements_file=None, pip=None, conda_file=None):
        self.pip_env = pip_env
        self.requirements_file = requirements_file
        self.pip = pip
        self.conda_file = conda_file

    def to_payload(self):
        return {
            "pip_env": self.pip_env.as_package_list() if self.pip_env else [],
            "requirements_file": str(self.requirements_file) if self.requirements_file else None,
            "pip": self.pip.as_package_list() if self.pip else [],
            "conda_file": str(self.conda_file) if self.conda_file else None,
        }


class PipDependencies:
    def __init__(self, deps, overridden_framework_packages=None):
        self.deps = deps
        self.overridden_framework_packages = overridden_framework_packages or []

    @classmethod
    def from_env(cls):
        if not in_virtualenv():
            raise NoVirtualEnvFound
        deps = chill(no_chill=True)[0]
        reqs = []
        for dep in deps:
            full_spec = f"{dep.name}=={dep.version}"
            try:
                req = Requirement.parse(full_spec)
                if req.name not in FRAMEWORK_PACKAGES:
                    req.full_spec = full_spec
                    reqs.append(req)
            except Exception:
                # This should never happen, but just in case
                raise InvalidDependencyConfig(f"Could not parse requirement {full_spec} in environment")
        return cls(deps=reqs)

    @classmethod
    def from_strings(cls, requirements_strings):
        reqs = []
        for requirement in requirements_strings:
            try:
                req = Requirement.parse(requirement)
                req.full_spec = requirement
                reqs.append(req)
            except Exception:
                raise InvalidDependencyConfig(f"Could not parse requirement {requirement}")

        overridden_packages = [r for r in reqs if r.name in FRAMEWORK_PACKAGES]
        # Unlike other methods, this allows a user to override framework images
        return cls(deps=list(reqs), overridden_framework_packages=overridden_packages)

    def as_package_list(self):
        return self.to_pip_names(self.deps)

    @staticmethod
    def to_pip_names(package_list):
        return sorted([dep.full_spec for dep in package_list])

    @staticmethod
    def to_pip_str(package_list):
        return "\n".join(PipDependencies.to_pip_names(package_list))

    def __str__(self):
        return self.to_pip_str(self.deps)


class RequirementsFileDependencies:
    def __init__(self, requirements_file):
        self.requirements_file = requirements_file

    @classmethod
    def from_file(cls, requirements_file_path):
        try:
            with open(requirements_file_path, "r") as requirements_file:
                return cls(requirements_file.read())
        except Exception:
            raise InvalidDependencyConfig(
                f"Could not open pip requirements file at {requirements_file_path}"
            )

    def __str__(self):
        return self.requirements_file


class CondaDependencies:
    def __init__(self, environment):
        self.environment = environment

    @classmethod
    def from_env(cls):
        env_out = subprocess.run(
            ["conda", "env", "export", "--from-history"], stdout=subprocess.PIPE
        )
        if env_out.returncode != 0:
            raise InvalidDependencyConfig(
                "Could not export current conda environment. "
                f"Running 'conda env export --from-history' returned exit code {env_out.returncode} "
            )
        try:
            environment = yaml.safe_load(env_out.stdout)
        except Exception as e:
            raise InvalidDependencyConfig(f"Could not parse current conda environment. Got {e}")

        environment.pop("name")
        environment.pop("prefix", None)
        return cls(environment=environment)

    @classmethod
    def from_file(cls, conda_file_path):
        try:
            with open(conda_file_path) as conda_file:
                try:
                    environment = yaml.safe_load(conda_file)
                    return cls(environment=environment)
                except Exception:
                    raise InvalidDependencyConfig(
                        f"Conda Environment file at {conda_file_path} could not be parsed"
                    )
        except Exception:
            raise InvalidDependencyConfig(
                f"Could not open Conda Environment file at {conda_file_path}",
            )

    def dump(self):
        return yaml.dump(self.environment)

    def __str__(self):
        return self.dump()


def get_pip_conda_dependencies(kwargs):
    """
    Parses code package specification kwargs and returns lists of pip and conda dependencies.
    These parameters (and hence, this code) is shared between the run and model server create
    APIs.
    """
    # grab conda env file contents
    python_deps = merge_dependencies(
        None,
        kwargs.pop("conda_file", None),
        kwargs.pop("requirements_file", None),
        kwargs.pop("pip_packages", []),
    ).to_payload()
    return python_deps["pip"], python_deps["conda_file"]


def merge_dependencies(python_env_deps, conda_file, requirements_file, pip_packages):
    python_deps = python_env_deps
    if conda_file is not None:
        if python_env_deps:
            # TODO(justin): Conda has a merge-environments script which can handle this logic
            raise InvalidDependencyConfig(
                "Merging dependencies from a conda environment and a conda file is not currently supported"
            )
        return PythonDependencies(conda_file=CondaDependencies.from_file(conda_file))

    if isinstance(python_deps, CondaDependencies):
        if pip_packages or requirements_file:
            raise InvalidDependencyConfig(
                "pip packages and requirements files cannot currently be specified when using the --deps-from-env flag "
                "from within a conda environment. You can include the pip installs in the conda environment file "
                "instead."
            )
        return PythonDependencies(conda_file=python_deps)

    python_deps = PythonDependencies(pip_env=python_deps)
    if requirements_file:
        python_deps.requirements_file = RequirementsFileDependencies.from_file(requirements_file)
    if pip_packages:
        python_deps.pip = PipDependencies.from_strings(pip_packages)
    return python_deps


def get_run_request(client, kwargs):
    """Converts an python API request's kwargs to a RunRequest"""
    pip, conda = get_pip_conda_dependencies(kwargs)
    # set workflow id
    if "workflow_id" not in kwargs and client.active_workflow:
        kwargs["workflow_id"] = client.active_workflow.id
    if "project" in kwargs:
        project = kwargs.pop("project")
        existing_projects = client.api.list_projects()

        # NOTE(aleksey): throws if a project with this name does not already exist
        project = get_project_by_name(existing_projects, project)
        kwargs["project_id"] = project.id
    return RunRequest(
        run_type="user",
        pip_packages=pip,
        conda_file=conda,
        **kwargs,
    )
