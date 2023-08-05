from box import Box
from pathlib import Path
from collections.abc import Mapping
from typing import Optional
from itertools import chain

from setuptools import setup as _setup, find_namespace_packages
from tomlkit import parse
try:
    from rich.traceback import install
except ImportError:
    pass
else:
    install()


def extra_file_name(file_name, pkg_name):
    pkg_parts = pkg_name.split('.')

    if file_name == '.':
        return pkg_name
    elif file_name.startswith('.'):
        parts = file_name.removeprefix('.').split('.')
        return '.'.join(chain(pkg_parts, parts))
    else:
        return file_name


def get_setup_args():
    with open('./pyproject.toml') as file:
        metadata = parse(file.read())
        project = Box(
            metadata['project'],
            default_box=True,
            default_box_attr=None,
            default_box_none_transform=False,
        )

    first_author = project.authors[0]

    if project.readme is not None:
        readme_path = Path(project.readme)
        with readme_path.open() as readme_file:
            readme = readme_file.read()

        content_types = {
            '.md': 'text/markdown',
            '.rst': 'text/x-rst',
        }

        content_type = content_types[readme_path.suffix.lower()]
    else:
        readme = None
        content_type = None

    if project.name.startswith('@'):
        name = project.name.removeprefix('@').replace('/', '.')
    else:
        name = project.name

    model_package = f'{name}.model'
    model_path = Path(model_package.replace('.', '/'))

    extra_files = metadata
    for path in ('tool', 'omniblack', 'setup', 'extra_files'):
        extra_files = extra_files.get(path)
        if extra_files is None:
            break

    if extra_files:
        package_data = {
            extra_file_name(pkg, name): globs
            for pkg, globs in extra_files.items()
        }
    else:
        package_data = {}

    if model_path.exists():
        package_data = package_data | {
            model_package: ('*.yaml', ),
        }

    if project.urls:
        homepage = project.urls.pop('homepage', None)
        urls = project.urls or None
    else:
        homepage = None
        urls = None

    if project.dependencies:
        deps = project.dependencies
    else:
        deps = None

    if project.scripts:
        entry_points = dict(
            console_scripts=[
                f'{name}={module_path}'
                for name, module_path in project.scripts.items()
            ]
        )
    else:
        entry_points = None

    setup_keywords = dict(
        author=first_author.name,
        author_email=first_author.email,
        classifiers=project.classifiers,
        entry_points=entry_points,
        install_requires=deps,
        keywords=project.keywords,
        license=project.license.name,
        license_files=[project.license.file],
        long_description=readme,
        long_description_content_type=content_type,
        name=name,
        package_data=package_data,
        packages=find_namespace_packages(include=(name, f'{name}.*')),
        project_urls=urls,
        python_requires=project.requires_python,
        url=homepage,
        version=project.version,
        zip_safe=True,
    )

    setup_keywords = {
        key: value
        for key, value in setup_keywords.items()
        if value is not None
    }

    return setup_keywords


def setup(setup_keywords: Optional[Mapping] = None):
    if setup_keywords is None:
        setup_keywords = get_setup_args()

    _setup(**setup_keywords)
