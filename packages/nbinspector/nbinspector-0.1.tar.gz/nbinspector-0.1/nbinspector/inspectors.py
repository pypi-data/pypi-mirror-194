import ipywidgets as widgets
from IPython.display import clear_output
from IPython.core.display_functions import display
from functools import partial

boxlayout = widgets.Layout(flex_flow="row wrap")
buttonlayout = widgets.Layout(border="solid", fill="blue")
buttonstyle_blue = widgets.ButtonStyle(button_color="#ADD8E6")
buttonstyle_purple = widgets.ButtonStyle(button_color="#CBC3E3")

def inspect_dict(root_obj):
    def recursive_inspect(b, obj, index_tracker, parent):
        clear_output()

        elements = []

        header_widget = widgets.Output()
        header_widget.append_stdout("Inspecting dictionary...")

        index_tracker_widget = widgets.Output()
        index_tracker_widget.append_stdout(index_tracker)

        if isinstance(obj, dict) and len(obj) > 0:
            for k in obj:
                elements.append(widgets.Button(description="KEY: " + k, layout=buttonlayout, style=buttonstyle_blue))
                f = partial(recursive_inspect, obj=obj[k], index_tracker=f"{index_tracker}[\"{k}\"]", parent=obj)
                elements[-1].on_click(f)
        elif isinstance(obj, list) and len(obj) > 0:
            for i, val in enumerate(obj):
                elements.append(widgets.Button(description="LIST INDEX: " + str(i), layout=buttonlayout, style=buttonstyle_blue))
                f = partial(recursive_inspect, obj=val, index_tracker=f"{index_tracker}[{i}]", parent=obj)
                elements[-1].on_click(f)
        else:
            elements.append(widgets.Output())
            elements[-1].append_stdout("VALUE: " + str(obj))

        root_button = widgets.Button(description="Home", layout=buttonlayout)
        f = partial(recursive_inspect, obj=root_obj, index_tracker="CURRENT PATH: root", parent=root_obj)
        root_button.on_click(f)

        display(widgets.VBox([header_widget, root_button, index_tracker_widget, widgets.HBox(elements, layout=boxlayout)]))
    recursive_inspect(None, root_obj, "CURRENT PATH: root", root_obj)

def inspect_obj(root_obj):
    def get_sorted_attributes(obj):
        public_attr = [a for a in dir(obj) if not a.startswith("_")]
        reserved_attr = [a for a in dir(obj) if a.startswith("__")]
        private_attr = [a for a in dir(obj) if a.startswith("_") and a not in reserved_attr]
        return sorted(public_attr) + sorted(private_attr) + sorted(reserved_attr)

    def recursive_inspect(b, obj, index_tracker, parent):
        clear_output()

        elements = []

        header_widget = widgets.Output()
        header_widget.append_stdout("Inspecting object...")

        index_tracker_widget = widgets.Output()
        index_tracker_widget.append_stdout(index_tracker)

        for k in get_sorted_attributes(obj):
            elements.append(widgets.Button(description=k, layout=buttonlayout, style=buttonstyle_purple))
            try:
                f = partial(recursive_inspect, obj=getattr(obj, k), index_tracker=f"{index_tracker}.{k}", parent=obj)
                elements[-1].on_click(f)
            except:
                elements.pop()
                elements.append(widgets.Output(layout=buttonlayout))
                elements[-1].append_stdout(k)

        value_widget = widgets.Output()
        value_widget.append_stdout("STR: " + str(obj))

        root_button = widgets.Button(description="Home", layout=buttonlayout, )
        f = partial(recursive_inspect, obj=root_obj, index_tracker="CURRENT PATH: root", parent=root_obj)
        root_button.on_click(f)

        display(widgets.VBox([header_widget, root_button, index_tracker_widget, value_widget, widgets.Box(elements, layout=boxlayout)]))
    recursive_inspect(None, root_obj, "CURRENT PATH: root", root_obj)

def inspect(obj):
    if isinstance(obj, dict):
        inspect_dict(obj)
    else:
        inspect_obj(obj)
