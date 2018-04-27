# Administration

## Version string management
We use [versioneer](https://github.com/warner/python-versioneer) to manage `mlt` version strings.
Unless there is a good reason to run this scenario again, it's provided here for reference only.

This is how we enabled `versioneer` support for `mlt`.

```bash
$ git checkout https://github.com/IntelAI/mlt.git
$ cd mlt
$ make venv
Creating python2 and 3 virtualenv in .venv and .venv3 dirs
...
  py2-venv: commands succeeded
  py3-venv: commands succeeded
  congratulations :)
$ . .venv/bin/activate
(.venv) $ pip install versioneer
Collecting versioneer==0.18
...
Installing collected packages: versioneer
Successfully installed versioneer-0.18
```

Now edit [setup.cfg](../setup.cfg) and add the following section:
```
[versioneer]
VCS = git
style = pep440
versionfile_source = mlt/_version.py
versionfile_build = mlt/_version.py
tag_prefix = v
```

and install `versioneer`
```bash
$ versioneer install
versioneer.py (0.18) installed into local tree
Now running 'versioneer.py setup' to install the generated files..
 creating mlt/_version.py
 appending to mlt/__init__.py
 appending 'versioneer.py' to MANIFEST.in
 appending versionfile_source ('mlt/_version.py') to MANIFEST.in

Your setup.py appears to be missing some important items
(but I might be wrong). Please make sure it has something
roughly like the following:

 import versioneer
 setup( version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),  ...)
```

Finally update [setup.py](../setup.py) and add the following lines as was instructed by `versioneer`:
```python
import versioneer

setup(name='mlt',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      ...
```

## Creating Python distributions for PyPI
Currently [Makefile](../Makefile) has a couple of subcommands to create a Python distribution and also publish the binary to [PyPI](https://pypi.org/).

```bash
$ make dist
Creating python2 and 3 virtualenv in .venv and .venv3 dirs
...
Building wheels for collected packages: mlt
  Running setup.py bdist_wheel for mlt ... done
  Stored in directory: /Users/ashahba/source_code/IntelAI/mlt-versions/dist
Successfully built mlt
```
Now you should have `mlt` wheel under `dist` folder:
```bash
$ ls dist/
PyYAML-3.12-cp27-cp27m-macosx_10_13_x86_64.whl		docopt-0.6.2-py2.py3-none-any.whl			pip-10.0.1-py2.py3-none-any.whl				six-1.11.0-py2.py3-none-any.whl				watchdog-0.8.3-cp27-cp27m-macosx_10_13_x86_64.whl
argh-0.26.2-py2.py3-none-any.whl			mlt-0.1.0a1+18.g60503e0-py2.py3-none-any.whl		progressbar2-3.37.1-py2.py3-none-any.whl		tabulate-0.8.2-cp27-none-any.whl
conditional-1.2-py2.py3-none-any.whl			pathtools-0.1.2-cp27-none-any.whl			python_utils-2.3.0-py2.py3-none-any.whl			termcolor-1.1.0-cp27-none-any.whl
```

Users can use the wheel file for virtual or system wide installations by running for example:
```bash
pip install dist/mlt-0.1.0a1+18.g60503e0-py2.py3-none-any.whl
```

## Publish current mlt version to PyPI
In order to push Python distribution of `mlt` to `PyPI`, `.pypirc` file need to be configured in Admin user's home directory which [distutils](https://docs.python.org/2/distutils/packageindex.html) checks.

Read/Write permissions to the file `.pypirc` should be reserved to only current user and it's format should be as follows:

```
[distutils]
index-servers =
    pypitest
    pypi

[pypitest]
repository: <repository-url>
username: <username>
password: <password>

[pypi]
repository: <repository-url>
username: <username>
password: <password>
```

Usually people publish the distributions to `PyPI` for latest tags.
Once the distribution binary is built successfully for a given tag, you should be able to run:

```bash
make release dist/mlt-0.1.0a1+18.g60503e0-py2.py3-none-any.whl
```

and that publishes the distribution to `PyPI`.

Minutes later end users would be able to just run:
```
pip install mlt
```
to install current version of `mlt` on their systems, or they can upgrade existing `mlt` to latest version:
```bash
pip install -U mlt
```
