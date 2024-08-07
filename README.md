# qgis-plugin-base

This repository contains source code for base QGIS plugin. Bear in mind that this is not a full base plugin with all needed utility functions etc. This can be used as a foundation for new QGIS plugin project :)

This repository contains used tools and inspiration from following amazing QGIS projects. Go check them out :fire:

- [cookiecutter-qgis-plugin](https://github.com/GispoCoding/cookiecutter-qgis-plugin/tree/main)
  - cookiecutter template for creating great base for QGIS plugin development
- [qgis-plugin-tools](https://github.com/GispoCoding/qgis_plugin_tools)
  - utility methods for QGIS plugin development
- [pytest-qgis](https://github.com/GispoCoding/pytest-qgis)
  - pytest plugin for QGIS development
- [qgis-plugin-dev-tools](https://github.com/nlsfi/qgis-plugin-dev-tools)
  - development tools to ease up QGIS plugin development

## Table of contents

- [qgis-plugin-base](#qgis-plugin-base)
  - [Table of contents](#table-of-contents)
  - [Environment setup](#environment-setup)
    - [Install QGIS](#install-qgis)
    - [Create virtual environment with QGIS Python dependencies](#create-virtual-environment-with-qgis-python-dependencies)
  - [Developing](#developing)
    - [Debugging](#debugging)
    - [Running tests](#running-tests)
    - [Run pre-commit checks](#run-pre-commit-checks)
    - [Translations](#translations)
  - [Packaging plugin](#packaging-plugin)

## Environment setup

Following setup instructions assumes that you are using Windows and `vscode` as IDE.

### Install QGIS

Install latest QGIS LTR (3.34) via [OSGeo4W installer](https://trac.osgeo.org/osgeo4w/). Default installation also configures Python 3.12, Python QT-bindings, GDAL etc. that are necessary for plugin development.

### Create virtual environment with QGIS Python dependencies

Easiest way to install Python virtual environment with all necessary QGIS Python dependencies is to use `OSGeo4W Shell`. The reason for this is that shell already uses Python that comes with QGIS installation. Therefore, it has all necessary Python dependencies that should be included with virtual environment.

Open `OSGeo4W Shell` and navigate to this project folder and run command below

```bash
%PYTHONHOME%/python.exe -m venv --system-site-packages .venv
```

This will create `.venv` folder with required QGIS Python dependencies for plugin development

Create `qgis.pth` file under `.venv` folder with path to Python installation by `OSGeo4W`. Change path matching to your `OSGeo4W` installation path i.e.

```bash
C:/OSGeo4W/apps/qgis-ltr/python
```

Create `sitecustomize.py` filer under `.venv/Lib/site-packages`. Change paths matching to your `OSGeo4W` installation path.

```python
import os

os.add_dll_directory("C:/OSGeo4W/bin")
os.add_dll_directory("C:/OSGeo4W/apps/qgis-ltr/bin")
os.add_dll_directory("C:/OSGeo4W/apps/Qt5/bin")
```

Activate `.venv` by running following command

```bash
.venv\Scripts\activate.bat
```

Make sure that `vscode` interpreter is pointing to created virtual environment. You can check this by `CTRL + SHIFT + P` => "Python: Select Interpreter" -> Select created virtual environment

Compile dependencies from `requirements-dev.in` and `requirements.in` files

```bash
pip install pip-tools
pip-compile requirements-dev.in
pip-compile requirements.in
```

Install Python dependencies

```bash
pip install -r requirements-dev.txt -r requirements.txt
```

Install `pre-commit`

```bash
pre-commit install
pre-commit run --all-files
```

`pre-commit` is run always before committing code to source branch. This assumes that written code conforms against `ruff` and `mypy` linting rules

## Developing

Create `.env` file with content

```env
QGIS_EXECUTABLE_PATH=C:\OSGeo4W\bin\qgis-ltr-bin.exe
DEBUGGER_LIBRARY=debugpy
DEVELOPMENT_PROFILE_NAME=plugin-dev
DEBUGGING_ENABLED=1
PROFILE=local
```

- `QGIS_EXECUTABLE_PATH` - path for the QGIS binary executable i.e. `C:\OSGeo4W\bin\qgis-ltr-bin.exe`
- `PROFILE` - profile of running environment
- (optional) `DEBUGGER_LIBRARY` - what debugging server should `qgis-plugin-dev-tools` start. Possible values are: `debugpy` or `pydevd`
- (optional) `DEVELOPMENT_PROFILE_NAME` - what profile should `qgis-plugin-dev-tools` configure when starting QGIS
- (optional) `DEBUGGING_ENABLED` - defines logging level as `DEBUG` and logs to file if set to `1`

```shell
qgis-plugin-dev-tools start | qpdt start
```

This starts QGIS with plugin loaded, debugging server started and environment variables set

**NOTE** Use plugin reloader plugin for updating plugin code after code changes

### Debugging

Start debugger in `vscode` using `launch.json` configuration. `qgis-plugin-dev-tools` automatically starts debugging server in port 5678. Use `DEBUGGER_LIBRARY` environment variable to adjust whether to use `debugpy` or `pydevd` debugger. Set desired breakpoints to code files and debugger should attach to these when running code.

### Running tests

Tests should be placed under `tests` folder with `test_` prefix in file names

```bash
pytest
```

### Run pre-commit checks

```bash
pre-commit run --all-files
```

### Translations

`translations.pro` defines from which QT UI and Python files translations should be retreived. Run script `scripts\update-translations.sh` to update `.ts` files with newest translations

Translations can be used in Python code as follows

```python
translate("<TRANSLATION_CONTEXT>", "<TRANSLATION_KEY>")
```

In UI files it looks something like this, where `translationKey` is the key that is translatable in `.ts` files.

```xml
<widget class="QLabel" name="label">
  <property name="text">
    <string>translationKey</string>
  </property>
</widget>
```

Language files are located in `plugin/resources/i18n` folder where each locale gets its own file. Translations itself can be modified straighly to `.ts` files. But also [QT Linquist](`https://github.com/lelegard/qtlinguist-installers/releases`) desktop program can be used to do that.

In order to QT-framework to read newest compiled translations script `scripts\update-translations.sh` has to be run.

## Packaging plugin

```bash
qgis-plugin-dev-tools build | qpdt build
```

This creates a zip file i.e. `plugin-x.x.x.zip` into `dist` folder. This zip-file can be installed via QGIS `Manage and Install Plugins...`.
