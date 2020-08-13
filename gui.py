import sizetree
import tkinter as tk
import tkinter.filedialog
import json
import os


class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.root_path = ""
        self.title("size tree")

        self.options_frame = tk.LabelFrame(self, text="Options")
        self.options_frame.grid(row=1, column=0)

        self.checkboxes = {
            "animated_bars": tk.Checkbutton(self.options_frame, text="Animate the bars"),  # Javascript side \/
            "slow_mode": tk.Checkbutton(self.options_frame, text="Slow mode"),
            "view_on_finish": tk.Checkbutton(self.options_frame, text="Load page when finished"),  # Python side \/
            "print_indexed_dirs": tk.Checkbutton(self.options_frame, text="Print searched directorys"),
        }  # Support for more options as needed (though idk what theyed be)

        self.checkbox_vars = {}
        for key, checkbox in self.checkboxes.items():
            newvar = tk.IntVar()
            checkbox.config(variable=newvar)
            self.checkbox_vars[key] = newvar

        self.checkboxes["view_on_finish"].select()
        self.checkboxes["print_indexed_dirs"].select()
        self.checkboxes["animated_bars"].select()

        [cb.grid(row=row, column=0) for row, cb in enumerate(self.checkboxes.values())]

        self.path_choice_label = tk.Label(self, text="Root directory: ")
        self.path_choice_label.grid(row=0, column=0, sticky="e")

        self.path_choice_button = tk.Button(self, text="    ", command=self.file_prompt)
        self.path_choice_button.grid(row=0, column=1)

        self.path_choise_display = tk.Entry(self, state="readonly")  # Unsure if readonly is a good idea.
        self.path_choise_display.grid(row=0, column=2)

        self.execute_button = tk.Button(self, text="Generate", command=self.run)
        self.execute_button.grid(row=1, column=1, columnspan=2)

        self.set_root_path("C:\\")

    def file_prompt(self):
        self.set_root_path(tk.filedialog.askdirectory())

    def set_root_path(self, s: str):
        s = s.replace('/', '\\')
        self.root_path = s

        self.path_choise_display.config(state="normal")
        self.path_choise_display.delete(0, "end")
        self.path_choise_display.insert(0, s)
        self.path_choise_display.config(state="readonly")

    def run(self):
        # [widget.config(state="disabled") for widget in self.children.values()]
        self.withdraw()

        options = {}
        for key, val in self.checkbox_vars.items():
            options[key] = bool(val.get())

        print(options)

        tree = sizetree.FilenameHolder(self.root_path, True, options["print_indexed_dirs"])

        with open("sizes.json", "w") as f:
            f.write("var sizes = ")
            json.dump(tree.classes[-1].get_info_dict(), f, indent=1)
            f.write("\nvar options = ")
            json.dump(options, f, indent=4)

        if options["view_on_finish"]:
            os.startfile("graph.html")

        self.destroy()


if __name__ == '__main__':
    gui = Gui()
    print("Use the gui")
    gui.mainloop()
    print("Success")
