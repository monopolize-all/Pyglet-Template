import os
import shutil
import yaml


USE_DEFAULT_PREFERENCES = True

preferences = []  # Reference to current preferences


program_path = os.path.dirname(__file__)
preferences_path = os.path.join(program_path, 'preferences.yaml')
default_preferences_path = os.path.join(program_path, 'default_preferences.yaml')

if USE_DEFAULT_PREFERENCES:
    shutil.copyfile(default_preferences_path, preferences_path)


funcs_to_call_on_preferences_update = []

# Decorator
def call_on_preferences_update(func):
    funcs_to_call_on_preferences_update.append(func)
    return func


def on_preferences_update():
    for func in funcs_to_call_on_preferences_update:
        func()


def save():
    with open(preferences_path, "w") as f_handle:
        yaml.dump(preferences, f_handle)

def load():
    global preferences
    with open(preferences_path, "r") as f_handle:
        preferences_dict = yaml.safe_load(f_handle)

    preferences = PrefObj(preferences_dict)

    on_preferences_update()

class PrefObj:

    INDENT_STEP = '  '

    def __init__(self, pref_dict):
        if type(pref_dict) == list:
            self.children = []

            for elem in pref_dict:
                if type(elem) in (list, dict):
                    self.children.append(PrefObj(elem))
                else:
                    self.children.append(elem)
            

        elif type(pref_dict) == dict:
            self.children = {}
            for key, elem in pref_dict.items():
                
                if type(elem) in (list, dict):
                    self.children[key] = PrefObj(elem)
                else:
                    self.children[key] = elem
            
            for key, val in self.children.items():
                setattr(self, key, val)

        else:
            raise Exception('Unaccounted case error.')

    def __getitem__(self, key):
        return self.children[key]

    def __setitem__(self, key, val):
        self.children[key] = val

    def __str__(self, indent=''):
        out = ''
        if type(self.children) == list:
            for elem in self.children:
                if type(elem) == PrefObj:
                    out += indent + elem.__str__(indent+self.INDENT_STEP) + ':\n'
                else:
                    out += indent + str(elem) + '\n'

        elif type(self.children) == dict:
            for key, elem in self.children.items():
                if type(elem) == PrefObj:
                    out += indent + key + ':\n'
                    out += elem.__str__(indent+self.INDENT_STEP)
                else:
                    out += indent + key + ': ' + str(elem) + '\n'

        else:
            raise Exception('Unaccounted case error.')

        return out


funcs_to_call_on_preferences_update.append(save)

load()
