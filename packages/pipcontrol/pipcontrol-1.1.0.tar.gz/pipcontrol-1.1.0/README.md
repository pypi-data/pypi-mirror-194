# pipcontrol

This package is developed for automation of pip install

## How to use

```python
import os

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
pipcontrol = PipControl(ABS_PATH)

pipcontrol.install(packages=["boto3", "urllib3", "wheel", "twine"])
pipcontrol.update(packages=["boto3", "urllib3", "wheel", "twine"])
# pipcontrol.uninstall(packages=["boto3", "urllib3", "wheel", "twine"])

pipcontrol.requirement_freeze()
# pipcontrol.requirement_install()
# pipcontrol.requirement_uninstall()

pipcontrol.setup_venv()
pipcontrol.run("run.py")

```
