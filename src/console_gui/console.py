import os.path

from src.models.beam import Beam
from src.models.node import Node
from src.models.material import Material
from src.models.section import Section
from src.models.meta import ObjectDoesNotExist


class ConsoleMode(object):
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
                print("Under construction")
            elif action == 'support':
                print("Under construction")
            elif action == 'run':
                print("Under construction")
            elif action == 'settings':
                ConsoleSettingsMenu().settings_menu()
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
            print("Type _id of the {name} to be removed, 'list' or 'back' to cancel".format(name=self.obj.name))
            action = input('')
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
    def _value_input(msg):
        return input(msg+' :')


class ConsoleNodeMenu(ConsoleObjectMenu):
    def __init__(self):
        self.obj = Node

    def _add_object(self):
        Node.get_or_create(
            x=self._value_input('x'),
            y=self._value_input('y')
        )


class ConsoleSectionMenu(ConsoleObjectMenu):
    def __init__(self):
        self.obj = Section

    def _add_object(self):
        Section.get_or_create(
            name=self._value_input('Name'),
            area=self._value_input('Area'),
            inertia=self._value_input('Inertia')
        )


class ConsoleMaterialMenu(ConsoleObjectMenu):
    def __init__(self):
        self.obj = Material

    def _add_object(self):
        Material.get_or_create(
            name=self._value_input('Name'),
            young=self._value_input("Young's module"),
            poisson=self._value_input("Poisson's constant")
        )


class ConsoleBeamMenu(ConsoleObjectMenu):
    def __init__(self):
        self.obj = Beam
        self.start_node = None
        self.end_node = None
        self.material = None
        self.section = None

    def _add_object(self):
        print('Step 1: Select or create first Node:')
        self.start_node = self._select_or_create_obj(Node, ConsoleNodeMenu)
        print('Step 2: Select or create second Node:')
        self.end_node = self._select_or_create_obj(Node, ConsoleNodeMenu)
        print('Step 3: Select or create Material:')
        self.material = self._select_or_create_obj(Material, ConsoleMaterialMenu)
        print('Step 4: Select or create Section:')
        self.section = self._select_or_create_obj(Section, ConsoleSectionMenu)
        Beam.get_or_create(
            start_node=self.start_node,
            end_node=self.end_node,
            material=self.material,
            section=self.section
        )

    @staticmethod
    def _select_or_create_obj(obj, obj_manager):
        while True:
            ConsolePrintOut().print_model(obj)
            print(
                "Type _id of the {name} to be selected, 'manage' to go to manager, 'back' to cancel"
                .format(name=obj.name)
            )
            action = input('')
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


class ConsoleSettingsMenu(object):
    def settings_menu(self):
        print("Under construction.")

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
