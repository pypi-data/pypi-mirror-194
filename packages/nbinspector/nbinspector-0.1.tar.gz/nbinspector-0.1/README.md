# nbinspector
Notebook Inspector Tools

# Overview
Simple tool to enable inspection of both dictionaries and generic objects in Jupyter notebooks.

The inspector will create a clickable interface in your notebook where you can browse your object in real time.

# Usage
```
from nbinspector import inspect

# ... define an object named "object"

inspect(object)
```

If you use `inspect()`, the function assumes an interface based on the detected object type. If you'd like to force a behavior, you can use one of the specific inspectors like so:
```
from nbinspector import inspect_dict, inspect_obj

inspect_dict(your_dictionary)
inspect_obj(your_object)
```

