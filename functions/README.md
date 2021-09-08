# Functions
Most of the functions have been layed out into individual folders and are in a subfolder named `package`

The folder structure for a function looks like this:

```
functions
|_ <function_name>
  |_ create.sh
  |_ destroy.sh
  |_ update.sh
  |_ package
    |_ build.sh
    |_ function.py
    |_ __init__.py
    |_ requirements.txt
```

The create and update scripts basically build and upload the `package` directory to fission.

The destroy script cleans up the `functions` and `package` from fission

There is a `helper.py` which is a common library that multiple functions can consume. So in the create and update steps this file is copied into the package directory before the package is built. And this is deleted. This is the best method I could come up with for function reuse. 

In the main `functions` directory there is are also `create.sh`, `destroy.sh`, & `update.sh` these script manage the Fission `Enviornments` as well as call all of the nested scripts of the same name. ie: `create.sh`

### Deploy functions
This is extreamly easy, from the main `functions` directory simplly run:
```bash
bash create.sh
```

This will deploy all functions and enviorments to Fission.

