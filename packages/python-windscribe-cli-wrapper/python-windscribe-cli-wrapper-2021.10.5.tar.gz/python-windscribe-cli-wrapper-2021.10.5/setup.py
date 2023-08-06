from datetime import datetime, timezone
import setuptools


def construct_package_version():
    current_date = datetime.now(tz=timezone.utc)

    return f'{current_date.year}.{current_date.month}.{current_date.day}'


def package_details():
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Development Status :: 2 - Pre-Alpha',
    ]

    requirements = [
        'attrs>=19.0.0',
        'loguru>=0.5.0',
        'pexpect>=4.0.0',
    ]

    return {
        'author': 'anton.alvariumsoft',
        'author_email': 'anton.alvariumsoft@gmail.com',
        'description': 'Python Windscribe VPN CLI wrapper (Fixed https://github.com/Dayzpd/Python-Windscribe)',
        'keywords': 'windscribe vpn',
        'classifiers': classifiers,
        'license': 'MIT',
        'name': 'python-windscribe-cli-wrapper',
        'packages': ['windscribe'],
        'url': 'https://gitlab.com/anton.alvariumsoft/python-windscribe-cli-wapper',
        'version': construct_package_version(),
        'install_requires': requirements,
    }


setuptools.setup(**package_details())
