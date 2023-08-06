import os

class File:
    def __init__(self, path):
        with open(path, "r") as file:

            self.name = os.path.basename(file.name).replace("_", "-")
            self.path = path
            self.abs_lines = list()
            self.settings = dict()
            self.ranges_of_comps = dict()
            self.number_of_comps = 0
            self.more_than_one_comp = False

            self.add_setting = Add_setting(self)

            supported_formats = {"gaussian": (0, "Entering Link 1"),
                                 "orca": (3, "* O   R   C   A *")
                                 }

            def check_line(dict, line):
                ans = [k for k in list((i, j[0]) if j[1] in line else False for i, j in dict.items()) if k]
                if ans:
                    return ans[0]

            for index, line in enumerate(file):
                out = check_line(supported_formats, line)
                if out:
                    #print(out)
                    self.type = out[0]
                    self.ranges_of_comps.update({self.number_of_comps: (index - out[1], None)})
                    #print(index, out[1], self.number_of_comps)
                    if self.number_of_comps > 0:
                        self.more_than_one_comp = True
                        self.ranges_of_comps.update({self.number_of_comps -1 : (self.ranges_of_comps.get(self.number_of_comps-1)[0], index - out[1] - 1)})
                    self.number_of_comps += 1

            print("INFO:  Number of recognised computations in "+self.type.capitalize()+" file: "+str(self.number_of_comps))


        self.reader = ImportReader(self)


    def list_settings(self):
        if len(self.settings) == 0:
            print("INFO:  There are currently no settings appended.")
            print(" "*7 + "Use the method >> add_setting(label, *strings) << to add them.")
        else:
            print("INFO:  Currently active settings:")
            for lab, sett in self.settings.items():
                print(" "*9+"> "+lab)
                for string in sett.strings:
                    print(" "*13+str(string))


class AbsLine:
    def __init__(self, wavelength, strength, *transitions):
        self.wavelength = wavelength
        self.f = strength
        self.transitions = list(transitions)


class ImportReader:
    def __init__(self, file):
        self.parent_file = file
        self.type = self.parent_file.type

        self.initialize_reader()
        #self.parameters = list()
        self.module.run(self)

    def initialize_reader(self):
        if not hasattr(self, "type"):
            raise ValueError("ImportReader cannot be initialized, attribute >> type << is missing")

        try:
            self.module = __import__("colour_of_molecule.input." + self.type, fromlist=[None])
            #print("Importing from colour_of_molecule.input." + self.type + " ...")
        except:
            raise Exception("Something went wrong while initializing file reader. Is the input type implemented?")

    # def update(self):
    #     self.module.run(self)

    def __get__(self, instance, owner):
        self.module.run(self)

class Setting:
    def __init__(self, label, *args):
        self.label = label
        self.strings = list(args)


class Add_setting:
    def __init__(self,file):
        self.__file = file

    def __call__(self, label, *args):
        #self.__file.settings.update({label : Setting(label, *args)})
        overwrite = "N"
        if label in self.__file.settings:
            print("WARNING:  Setting with the same label already exists!")
            print("Do you want to overwrite it?")
            overwrite = input("[y/N]")
        if overwrite == "y" or label not in self.__file.settings:
            self.__file.settings.update({label: Setting(label, *args)})
            self.__file.list_settings()
            #self.__file.reader.update()
        elif overwrite == "N":
            print("Command has been canceled.")
        else:
            print("WARNING:  Answer was not recognised. Command has been canceled.")

    def template(self, label):
        print("Importing template setting for label: "+label)



