# Shadowconf

**Shadowconf** - an elegant, dynamic, reflective, productive, reproducible and uninvasive Python yaml configuration framework. The shadow of your codebase. Never gets in your way.

Very well suited for ML projects, AI research, scientific experiments, small frameworks and generally command line based applications.

## Main ideas

Configuration should be ✨ _elegant_ ✨.

Configuration should be ✨ _dynamic_ ✨ - it should be built by arbitrary, freestyle injection of subconfigs (instead of strict hierarchical composition). We can achieve this by custom syntax on top of yaml files.

Configuration should be ✨ _reflective_ ✨ - it should try mirroring the structure of your codebase one-to-one. Each class which you want to configure should have a corresponding yaml file nested in folder structure preferably identical to the codebase. It should be possible to auto-generate yaml configs for your codebase to some extent.

Configuration should be ✨ _productive_ ✨ - you want configs to make it easier and faster to switch options.

Configuration should be ✨ _reproducible_ ✨ - you should be able to easily reproduce any run initiated with your configuration.

Configuration should be ✨ _uninvasive_ ✨ - it should never get in your way. It shouldn't limit the possiblities.


## Abstractions

**Main config (Mconf):** Specifies overall config structure.

**Sub config (Sconf):** Is available globally and can be injected into any part of other configs (as long as no loop is detected in final config tree).

**Override config (Oconf):** A config that can arbitrarily override parts of the final config structure. Can be used to implement submodes, version control specific sets of hyperparameter overrides, etc.

**Alias:** A way to define command line productivity shortcuts.

## Yaml syntax

Example subconfig:
```yaml
_target_: "torch.optim.Adam" # path for object instantation
_return_: "partial" # instantiation strategy, alternatively: "instance", "object"
lr: 0.01
```

Subconfig injection (from external yaml file):
```yaml
optimizer:
  _inject_: "@optimizers.adam.yaml"
```

Subconfig injection with field overrides:
```yaml
model:
  _inject_: "@models.mnist.yaml"
  net:
    _inject_: "@models.nets.resnet.yaml"
    input_size: 784
  optimizer:
    _inject_: "@optimizers.adam.yaml"
    lr: 0.005
```

Example of global config overrides:
```yaml
# here we can attach configs overriding any parts of main config
# each override can optionally specify a custom name (like "exp", "debug", etc.)
# which can be used to refer to it through command line
_overrides_:
  - _self_

  # attach optional local config
  # "optional" keyword means that specified config doesn't need to exist
  # you can use such config for e.g. storing custom paths excluded from version control
  - "optional @local/default.yaml"

  # attach experiment config e.g. `python main.py exp=@experiments/mnist.yaml`
  - exp: "@experiments/default.yaml"

  # attach debugging config, e.g. `python main.py debug=@debugs/step.yaml`
  - debug: null
```

Defining command line aliases:
```yaml
# aliases replace part of command if given pattern is detected 
_aliases_:
 - "exp=": "exp=@experiments/"
 - "debug1": "debug=@debugs/step.yaml"
 - "debug2": "debug=@debugs/epoch.yaml"

# `python main.py exp=mnist.yaml` -> `python main.py exp=@experiments/mnist.yaml`
# `python main.py debug1` -> `python main.py debug=@debugs/step.yaml`
# `python main.py debug2` -> `python main.py debug=@debugs/epoch.yaml`
```

## Command line override syntax

Switching main config:
```bash
python main.py cfg=configs/main.yaml
```

Overriding fields:
```bash
python main.py model.lr=1e-4
```

Switching subconfigs:
```bash
python main.py model=@models/resnet.yaml
python main.py model=@models/resnet
```

Attaching final overrides:
```bash
python main.py exp=@experiments/cifar10.yaml
python main.py exp=@experiments/cifar10
```

Expanding lists:
```bash
python main.py tags+=\[dev,mnist,resnet\]
```

Launching multirun:
```bash
python main.py seed=42,43,44
python main.py seed=42,43,44 launcher=@lauchers/submitit.yaml
```

## Code utilities

```python
import shadowconf as shadow
```

Instantation:
```python
shadow.summon(cfg.model)
```

## Workflow

**Step 1:** Write your python codes. 

Example:
```
src
  train.py
  models
    mnist_module.py
    cifar10_module.py
    imagenet_module.py
  data
    mnist_datamodule.py
    cifar10_datamodule.py
    imagenet_datamodule.py
```

**Step 2:** Easily generate yaml subconfigs by pointing to the folder of python scripts.

Example:
```bash
shadowconf cast -t src/models -o configs/models
```

<!-- Specify -a to also generate yaml per each lonely function in the file. -->
<!-- Specify -f to override already existing yaml files -->

Output:
```
configs
  models
    mnistlitmodule.yaml
    cifar10litmodule.yaml
    imagenetlitmodule.yaml
    imagenetlitmodulespecialised.yaml
```

(generates a separate yaml config for each python class found in src/models folder) <br>
(generated yaml names are based on class names) <br>
(uses default class arguments or inserts "???")

**Step 3:** Write main config by injecting subconfigs.

Example:
```yaml
data:
  _inject_: @data/mnistdatamodule.yaml

model:
  _inject_: @models/mnistlitmodule.yaml
  input_size: {data.}

trainer:
  _inject_: @trainers/default.yaml
```

**Step 4:** Write entry file which instantiates all objects from config.

Example:
```python
import shadowconf as shadow


def train(cfg):
    data = shadow.summon(cfg.data)
    model = shadow.summon(cfg.model)
    trainer = shadow.summon(cfg.trainer)
    trainer.fit(data, model)
    

@shadow.init(cfg="../configs/train.yaml")
def main(cfg)
    train(cfg)


if __name__=="__main__":
    main()
```


## Command line utilities

```bash
shadowconf cast -t src -o configs
shadowconf cast -t src/models -o configs/models
shadowconf cast -t lightning.callbacks.ModelCheckpoint -o configs/callbacks/
shadowconf cast -t lightning.callbacks.ModelCheckpoint -o schemas/callbacks/ -f python
```


## Development notes

(framework design based largely on Hydra)

**Problems:**

Detecting loops in the configuration tree. We should somehow visually print the config loop when its detected.

How to not be invasive for third-party solutions that relaunch the script, e.g. during spawn of DDP processes. Maybe we can provide environment variables which third-party solutions will be able to set to cotrol behavior of multirun, output folder generation, and any other features.

How to make multirun less invasive than in hydra? Should we even allow for `arg=1,2,3` syntax? Maybe we should require an additional, differently decorated function for multirun?

Are we sure `@` character won't break any terminal?

When user overrides field with string starting with `@` from cmd, the compliation will fail. We can require using double character `@@` when someone wants to really specify `@`.

**Features:**

Optional root setup.

Optional auto-loading of .env files.

Optional output folder generation.

Convenient subconfig and field overrides from command line.

Very fast command line auto-complete (it's crucial for productivity, might be impossible to make this fast??)

Variable interpolation.

Building pluggable launchers on top with support for remote environments.

Saving/pickling config for guaranteed reproducibility and easy resuming.

Optional saving snapshots of regex specified folders/files.

Optional, native tagging support?

Print final parsed command when launching.

## Discussing configuration libraries


List of available configuration libraries + what I like/dislike about them:

Omegaconf: <br>
\+ variable interpolation  <br>


Hydra: <br>
\+ overrides available from command line <br>
\+ support for type safety <br>

Dynaconf: <br>
_https://github.com/dynaconf/dynaconf_
