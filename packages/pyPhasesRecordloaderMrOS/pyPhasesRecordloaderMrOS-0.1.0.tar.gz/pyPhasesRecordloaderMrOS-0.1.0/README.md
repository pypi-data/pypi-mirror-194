# Extension for pyPhasesRecordloader

Extension to load data records from the MrOS Sleep Study (MrOS) database.

The extensions requires a downloaded version of the mros dataset. The location can be set through the config value `mros-path`.

## Usage

In a phase you can acess the data through the `RecordLoader`:

Add the plugins and config values to your `project.yaml`:

```yaml
name: MrOSProject
plugins:
  - pyPhasesML
  - pyPhasesRecordloaderMrOS
  - pyPhasesRecordloader

phases:
  - name: MyPhase

config:
  mros-path: C:/datasets/mros

```

In a phase (`phases/MyPhase.py`) you can acess the records through the `RecordLoader`:

```python
from pyPhasesRecordloader import RecordLoader
from pyPhases import Phase

class MyPhase(Phase):
    def run(self):
      recordIds = recordLoader.getRecordList()
      for recordId in recordIds:
        record = recordLoader.getRecord(recordId)
```

Run Your project with `python -m phases run MyPhase`