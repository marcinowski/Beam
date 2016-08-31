import os.path
import re

from src.models.beam import Beam
from src.models.node import Node
from src.models.material import Material
from src.models.section import Section
from src.models.load import Force, Momentum, UniformLoad
from src.models.supports import Support, Joint
from src.models.settings import Settings
from src.models.meta import ObjectDoesNotExist

# TODO: FEM!, Settings
# FIXME: Boolean input field: bool('false') doesn't evaluate to False!! Dumbass


class ConsoleMode(object):
    def __init__(self):
        Settings()

    def run(self):
        print("Type 'help' for the list of available options.")
        while True:
            print("***Main Menu***")
            action = input('>>')
            if action == 'quit':
                return
            elif action == 'help':
                self._view_help()
            elif action == 'node':
                ConsoleNodeMenu().object_menu()
            elif action == 'section':
                ConsoleSectionMenu().object_menu()
            elif action == 'material':
                ConsoleMaterialMenu().object_menu()
            elif action == 'beam':
                ConsoleBeamMenu().object_menu()
            elif action == 'load':
                LoadMainMenu().sub_menu()
            elif action == 'support':
                ConsoleSupportMainMenu().sub_menu()
            elif action == 'run':
                print("Under construction")
            elif action == 'settings':
                ConsoleSettingsMenu().sub_menu()
            else:
                print("Unknown command. Type 'help' for the list of available options.")

    @staticmethod
    def _view_help():
        with open(os.path.dirname(__file__) + '\\help_msg.txt', 'r') as f:
            print(f.read())


class ConsoleObjectMenu(object):
    """This is a skeleton for other model menus"""
    def __init__(self):
        """
        Method init is overwritten in every child-class, a little bit hacky I guess.
        """
        self.obj = None

    def object_menu(self):
        print("Do you want to 'add', 'list' {name}s, 'delete' them, or 'back' to main?".format(name=self.obj.name))
        while True:
            print("***{name} Menu***".format(name=self.obj.name.capitalize()))
            action = input('>>')
            if action == 'add':
                print("Provide the following values:")
                self._add_object()
                print('{name} created!'.format(name=self.obj.name))
            elif action == 'list':
                ConsolePrintOut().print_model(self.obj)
            elif action == 'delete':
                self._delete_menu()
            elif action == 'help':
                with open(os.path.dirname(__file__) + '\\help_sub_msg.txt', 'r') as f:
                    print(f.read().format(object=self.obj.name))
            elif action == 'back':
                return
            else:
                print("Unknown command. Type 'help' for the list of available options.")

    def _delete_menu(self):
        if self.obj.objects:
            ConsolePrintOut().print_model(self.obj)
        else:
            print('No {name}s to delete. Back to {name} Menu.'.format(name=self.obj.name))
            return
        while True:
            print('***{name} Delete Menu***'.format(name=self.obj.name))
            print("Type _id of the {name} to be removed, 'list' or 'back' to cancel".format(name=self.obj.name))
            action = input('>>')
            if action == 'back':
                return
            elif action == 'list':
                ConsolePrintOut().print_model(self.obj)
            else:
                try:
                    obj_to_remove = self.obj.get_obj_by_params(_id=int(action))
                except ObjectDoesNotExist:
                    print("Wrong id! Try again or 'back' to cancel")
                except ValueError:
                    print("Wrong id! Try again or 'back' to cancel")
                else:
                    self.obj.remove(obj_to_remove)
                    print("{name} was successfully removed!".format(name=self.obj.name))

    def _add_object(self):
        """
        Should be overwritten with specific model.
        :return:
        """
        pass

    @staticmethod
    def _value_input(pattern, msg, _type, warn):
        # fixme: maybe make a class out of inputs? many options-positive, lt_one etc.
        while True:
            action = input(msg+' :')
            if re.search(pattern, action):
                return _type(action)
            else:
                print(warn)

    def _int_value_input(self, msg):
        return self._value_input(
            pattern=r'^-?[0-9]+$',
            msg=msg,
            _type=int,
            warn="Input should be a whole number!"
        )

    def _string_value_input(self, msg):
        return self._value_input(
            pattern=r'^[a-zA-Z][a-zA-Z1-9_]+$',
            msg=msg,
            _type=str,
            warn="Input should start with a letter, and should not contain spaces or special signs!"
        )

    def _float_value_input(self, msg):
        return self._value_input(
            pattern=r'^-?[0-9]+(\.[0-9]{0,2})?$',
            msg=msg,
            _type=float,
            warn="Number must be whole or decimal up to 2 decimal places!"
        )

    def _float_value_lt_one_input(self, msg):
        return self._value_input(
            pattern=r'^0.[0-9]{1,2}$',
            msg=msg,
            _type=float,
            warn="Number must be decimal up to 2 decimal places between 0 and 1!"
        )

    def _bool_value_input(self, msg):
        return self._value_input(
            pattern=r'^((?i)[t](rue)?)|((?i)[f](alse)?)$',
            msg=msg,
            _type=bool,
            warn="You should type '(t)rue' or '(f)alse'"
        )


class ConsoleNodeMenu(ConsoleObjectMenu):
    def __init__(self):
        self.obj = Node

    def _add_object(self):
        Node.get_or_create(
            x=self._float_value_input('x'),
            y=self._float_value_input('y')
        )


class ConsoleSectionMenu(ConsoleObjectMenu):
    def __init__(self):
        self.obj = Section

    def _add_object(self):
        Section.get_or_create(
            name=self._string_value_input('Name'),
            area=self._float_value_input('Area'),
            inertia=self._float_value_input('Inertia')
        )


class ConsoleMaterialMenu(ConsoleObjectMenu):
    def __init__(self):
        self.obj = Material

    def _add_object(self):
        Material.get_or_create(
            name=self._string_value_input('Name'),
            young=self._float_value_input("Young's module"),
            poisson=self._float_value_lt_one_input("Poisson's constant")
        )


class ConsoleBeamMenu(ConsoleObjectMenu):
    def __init__(self):
        self.obj = Beam
        self.start_node = None
        self.end_node = None
        self.material = None
        self.section = None

    def _add_object(self):
        msg = 'Step 1: Select or create first Node:'
        self.start_node = self._select_or_create_obj(Node, ConsoleNodeMenu, msg)
        msg = 'Step 2: Select or create second Node:'
        self.end_node = self._select_or_create_obj(Node, ConsoleNodeMenu, msg)
        msg = 'Step 3: Select or create Material:'
        self.material = self._select_or_create_obj(Material, ConsoleMaterialMenu, msg)
        msg = 'Step 4: Select or create Section:'
        self.section = self._select_or_create_obj(Section, ConsoleSectionMenu, msg)
        Beam.get_or_create(
            start_node=self.start_node,
            end_node=self.end_node,
            material=self.material,
            section=self.section
        )

    @staticmethod
    def _select_or_create_obj(obj, obj_manager, message):
        while True:
            print(message)
            ConsolePrintOut().print_model(obj)
            print(
                "Type _id of the {name} to be selected, 'manage' to go to manager."
                .format(name=obj.name)
            )
            action = input('>>')
            if action == 'manage':
                obj_manager().object_menu()
            else:
                try:
                    obj_selected = obj.get_obj_by_params(_id=int(action))
                except ObjectDoesNotExist:
                    print("Wrong id! Try again or 'back' to cancel")
                except ValueError:
                    print("Wrong id! Try again or 'back' to cancel")
                else:
                    print("{name} was selected!".format(name=str(obj_selected)))
                    return obj_selected


class LoadTemplateMenu(ConsoleObjectMenu):
    @staticmethod
    def _select_obj(obj):
        ConsolePrintOut().print_model(obj)
        while True:
            print("Type _id of the {name} to be selected, 'list' to list the {name}s".format(name=obj.name))
            action = input('>>')
            if action == 'list':
                ConsolePrintOut().print_model(obj)
            else:
                try:
                    obj_selected = obj.get_obj_by_params(_id=int(action))
                except ObjectDoesNotExist:
                    print("Wrong id! Try again or 'back' to cancel")
                except ValueError:
                    print("Wrong id! Try again or 'back' to cancel")
                else:
                    print("{name} was selected!".format(name=str(obj_selected)))
                    return obj_selected


class ForceMenu(LoadTemplateMenu):
    def __init__(self):
        self.obj = Force

    def _add_object(self):
        Force.get_or_create(
            node=self._select_obj(Node),
            mgn_x=self._float_value_input('Magnitude x'),
            mgn_y=self._float_value_input('Magnitude y')
        )


class MomentumMenu(LoadTemplateMenu):
    def __init__(self):
        self.obj = Momentum

    def _add_object(self):
        Momentum.get_or_create(
            node=self._select_obj(Node),
            value=self._float_value_input('Momentum value'),
        )


class UniformLoadMenu(LoadTemplateMenu):
    def __init__(self):
        self.obj = UniformLoad

    def _add_object(self):
        UniformLoad.get_or_create(
            beam=self._select_obj(Beam),
            mgn_x=self._float_value_input('Magnitude x'),
            mgn_y=self._float_value_input('Magnitude y')
        )


class SupportMenu(LoadTemplateMenu):
    def __init__(self):
        self.obj = Support

    def _add_object(self):
        print("### Type 'true' or 'false' to BLOCK the following directions. ###")
        Support.get_or_create(
            node=self._select_obj(Node),
            x=self._bool_value_input('Direction x'),
            y=self._bool_value_input('Direction y'),
            rot=self._bool_value_input('Rotation')
        )


class JointMenu(LoadTemplateMenu):
    def __init__(self):
        self.obj = Joint

    def _add_object(self):
        print("### Type 'true' or 'false' to RELEASE the following directions. ###")
        Joint.get_or_create(
            node=self._select_obj(Node),
            x=self._bool_value_input('Direction x'),
            y=self._bool_value_input('Direction y'),
            rot=self._bool_value_input('Rotation')
        )


class SubMenu(object):
    def sub_menu(self):
        pass

    @staticmethod
    def _view_help(help_path):
        with open(os.path.dirname(__file__) + help_path, 'r') as f:
            print(f.read())


class LoadMainMenu(SubMenu):
    def sub_menu(self):
        while True:
            print('***Load Menu***')
            print("Manage entities 'force', 'momentum', 'uniform' or 'back' to main.")
            action = input('>>')
            if action == 'force':
                ForceMenu().object_menu()
            elif action == 'momentum':
                MomentumMenu().object_menu()
            elif action == 'uniform':
                UniformLoadMenu().object_menu()
            elif action == 'back':
                return
            elif action == 'help':
                self._view_help('\\help_load_msg.txt')
            else:
                print("Unknown command. Type 'help' for the list of available options.")


class ConsoleSupportMainMenu(SubMenu):
    def sub_menu(self):
        while True:
            print('***Support Main Menu***')
            print("Manage entities 'support', 'joint', or 'back' to main.")
            action = input('>>')
            if action == 'support':
                SupportMenu().object_menu()
            elif action == 'joint':
                JointMenu().object_menu()
            elif action == 'back':
                return
            elif action == 'help':
                self._view_help('\\help_supp_msg.txt')
            else:
                print("Unknown command. Type 'help' for the list of available options.")


class ConsoleSettingsMenu(SubMenu):
    def sub_menu(self):
        while True:
            print('***Settings Menu***')
            print("'Show' or 'edit' settings.")
            action = input('>>')
            if action == 'show':
                ConsolePrintOut().print_model(Settings)
            elif action == 'edit':
                pass
            elif action == 'back':
                return
            elif action == 'help':
                pass
            else:
                print("Unknown command. Type 'help' for the list of available options.")

    def list(self):
        pass

    def edit(self):
        pass


class ConsolePrintOut(object):
    def print_model(self, model):
        try:
            instance = model.objects[0]
        except IndexError:
            return print('No {name}s created yet.'.format(name=model.name))
        fields = instance.__dict__
        columns = len(fields)
        column_names = list(fields.keys())
        column_names.sort()
        column_widths = self._set_column_widths(column_names, model)
        rows = len(model.objects)
        for r in range(2*rows+3):
            if r % 2 == 0:
                string = ''
                for c in column_widths:
                    string += '+'
                    string += '-'*c
                print(string + '+')
            elif r == 1:
                string = ''
                for c in range(columns):
                    width = column_widths[c]
                    attr = column_names[c]
                    string += '| ' + attr + ' '*(width-len(attr)-1)
                print(string + '|')
            else:
                string = ''
                for c in range(columns):
                    mod = model.objects[(r-3)//2]
                    width = column_widths[c]
                    attr = str(getattr(mod, column_names[c]))
                    string += '| ' + attr + ' '*(width-len(attr)-1)
                print(string + '|')

    @staticmethod
    def _set_column_widths(field_names, model):
        result = []
        for name in field_names:
            result.append(0)
            for obj in model.objects:
                result[-1] = max(
                    len(str(getattr(obj, name))),
                    len(name),
                    result[-1]
                )
            result[-1] += 2
        return result

if __name__ == '__main__':
    ConsoleMode().run()
