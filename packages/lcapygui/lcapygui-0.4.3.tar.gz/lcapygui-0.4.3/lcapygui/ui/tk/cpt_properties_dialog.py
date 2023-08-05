from ...components.capacitor import Capacitor
from ...components.inductor import Inductor
from ...components.vcvs import VCVS
from ...components.vccs import VCCS
from ...components.ccvs import CCVS
from ...components.cccs import CCCS
from tkinter import Tk, Button
from .labelentries import LabelEntry, LabelEntries


class CptPropertiesDialog:

    def __init__(self, ui, cpt, update=None, title=''):

        self.cpt = cpt
        self.update = update
        self.ui = ui

        self.master = Tk()
        self.master.title(title)

        entries = []
        if cpt.kinds != {}:
            kind_name = cpt.kinds[cpt.kind]
            entries.append(LabelEntry(
                'kind', 'Kind', kind_name, list(cpt.kinds.values()),
                command=self.on_update))

        if cpt.styles != {}:
            style_name = cpt.styles[cpt.style]
            entries.append(LabelEntry(
                'style', 'Style', style_name, list(cpt.styles.values()),
                command=self.on_update))

        entries.append(LabelEntry('name', 'Name', cpt.name,
                                  command=self.on_update))
        entries.append(LabelEntry('value', 'Value', cpt.value,
                                  command=self.on_update))

        if isinstance(cpt, Capacitor):
            entries.append(LabelEntry(
                'initial_value', 'v0', cpt.initial_value,
                command=self.on_update))
        elif isinstance(cpt, Inductor):
            entries.append(LabelEntry(
                'initial_value', 'i0', cpt.initial_value,
                command=self.on_update))
        elif isinstance(cpt, (VCVS, VCCS, CCVS, CCCS)):
            names = [c.name for c in ui.model.components if c.name[0] != 'W']
            entries.append(LabelEntry('control', 'Control',
                                      cpt.control, names,
                                      command=self.on_update))

        for k, v in cpt.fields.items():
            entries.append(LabelEntry(k, v, getattr(cpt, k),
                                      command=self.on_update))

        self.labelentries = LabelEntries(self.master, ui, entries)

        button = Button(self.master, text="OK", command=self.on_ok)
        button.grid(row=self.labelentries.row)

    def on_update(self, arg=None):

        if self.cpt.kinds != {}:
            self.cpt.kind = self.cpt.inv_kinds[self.labelentries.get('kind')]

        if self.cpt.styles != {}:
            self.cpt.style = self.cpt.inv_styles[self.labelentries.get(
                'style')]

        name = self.labelentries.get('name')
        if name.startswith(self.cpt.name[0]):
            self.cpt.name = self.labelentries.get('name')
        else:
            self.ui.show_error_dialog('Cannot change component type')

        self.cpt.value = self.labelentries.get('value')

        try:
            self.cpt.initial_value = self.labelentries.get('initial_value')
        except KeyError:
            pass

        try:
            self.cpt.control = self.labelentries.get('control')
        except KeyError:
            pass

        for k, v in self.cpt.fields.items():
            setattr(self.cpt, k, self.labelentries.get(k))

        if self.update:
            self.update(self.cpt)

    def on_ok(self):

        self.on_update()

        self.master.destroy()
