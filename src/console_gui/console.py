from src.console_gui.console_tools import TemplateMenu, ConsolePrintOut, ConsoleObjectMenu
from src.models.beam import Beam
from src.models.node import Node
from src.models.material import Material
from src.models.section import Section
from src.models.load import Force, Momentum, UniformLoad
from src.models.supports import Support, Joint
from src.models.settings import Settings
from src.models.meta import ObjectDoesNotExist

# TODO: FEM!, README.md


class ConsoleMode(TemplateMenu):
    def __init__(self):
        Settings.get_or_create()

    def run(self):
        self.print_info("Welcome to Beam!")
        self.print_help("Type 'help' for the list of available options.")
        while True:
            self.print_info("***Main Menu***")
            action = input('>>')
            if action == 'quit':
                return
            elif action == 'help':
                self._view_help('\\help_msg.txt')
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
                self.print_error("Under construction")
            elif action == 'settings':
                ConsoleSettingsMenu().sub_menu()
            else:
                self.print_warn("Unknown command. Type 'help' for the list of available options.")


class ConsoleNodeMenu(ConsoleObjectMenu):
    def __init__(self):
        self.obj = Node

    def _add_object(self):
        Node.get_or_create(
            x=self.float_value_input('x'),
            y=self.float_value_input('y')
        )


class ConsoleSectionMenu(ConsoleObjectMenu):
    def __init__(self):
        self.obj = Section

    def _add_object(self):
        Section.get_or_create(
            name=self.string_value_input('Name'),
            area=self.float_value_input('Area'),
            inertia=self.float_value_input('Inertia')
        )


class ConsoleMaterialMenu(ConsoleObjectMenu):
    def __init__(self):
        self.obj = Material

    def _add_object(self):
        Material.get_or_create(
            name=self.string_value_input('Name'),
            young=self.float_value_input("Young's module"),
            poisson=self.float_value_lt_one_input("Poisson's constant")
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

    def _select_or_create_obj(self, obj, obj_manager, message):
        while True:
            self.print_help(message)
            ConsolePrintOut().print_model(obj)
            self.print_help(
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
                    self.print_warn("Wrong id! Try again or 'back' to cancel")
                except ValueError:
                    self.print_warn("Wrong id! Try again or 'back' to cancel")
                else:
                    self.print_info("{name} was selected!".format(name=str(obj_selected)))
                    return obj_selected


class LoadTemplateMenu(ConsoleObjectMenu):
    def _select_obj(self, obj):
        ConsolePrintOut().print_model(obj)
        while True:
            self.print_help("Type _id of the {name} to be selected, 'list' to list the {name}s".format(name=obj.name))
            action = input('>>')
            if action == 'list':
                ConsolePrintOut().print_model(obj)
            else:
                try:
                    obj_selected = obj.get_obj_by_params(_id=int(action))
                except ObjectDoesNotExist:
                    self.print_warn("Wrong id! Try again or 'back' to cancel")
                except ValueError:
                    self.print_warn("Wrong id! Try again or 'back' to cancel")
                else:
                    self.print_info("{name} was selected!".format(name=str(obj_selected)))
                    return obj_selected


class ForceMenu(LoadTemplateMenu):
    def __init__(self):
        self.obj = Force

    def _add_object(self):
        Force.get_or_create(
            node=self._select_obj(Node),
            mgn_x=self.float_value_input('Magnitude x'),
            mgn_y=self.float_value_input('Magnitude y')
        )


class MomentumMenu(LoadTemplateMenu):
    def __init__(self):
        self.obj = Momentum

    def _add_object(self):
        Momentum.get_or_create(
            node=self._select_obj(Node),
            value=self.float_value_input('Momentum value'),
        )


class UniformLoadMenu(LoadTemplateMenu):
    def __init__(self):
        self.obj = UniformLoad

    def _add_object(self):
        UniformLoad.get_or_create(
            beam=self._select_obj(Beam),
            mgn_x=self.float_value_input('Magnitude x'),
            mgn_y=self.float_value_input('Magnitude y')
        )


class SupportMenu(LoadTemplateMenu):
    def __init__(self):
        self.obj = Support

    def _add_object(self):
        self.print_help("Type 'true' or 'false' to BLOCK the following directions.")
        Support.get_or_create(
            node=self._select_obj(Node),
            x=self.bool_value_input('Direction x'),
            y=self.bool_value_input('Direction y'),
            rot=self.bool_value_input('Rotation')
        )


class JointMenu(LoadTemplateMenu):
    def __init__(self):
        self.obj = Joint

    def _add_object(self):
        self.print_help("### Type 'true' or 'false' to RELEASE the following directions. ###")
        Joint.get_or_create(
            node=self._select_obj(Node),
            x=self.bool_value_input('Direction x'),
            y=self.bool_value_input('Direction y'),
            rot=self.bool_value_input('Rotation')
        )


class LoadMainMenu(TemplateMenu):
    def sub_menu(self):
        while True:
            self.print_info('***Load Menu***')
            self.print_help("Manage entities 'force', 'momentum', 'uniform' or 'back' to main.")
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
                self.print_warn("Unknown command. Type 'help' for the list of available options.")


class ConsoleSupportMainMenu(TemplateMenu):
    def sub_menu(self):
        while True:
            self.print_info('***Support Main Menu***')
            self.print_help("Manage entities 'support', 'joint', or 'back' to main.")
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
                self.print_warn("Unknown command. Type 'help' for the list of available options.")


class ConsoleSettingsMenu(TemplateMenu):
    def sub_menu(self):
        while True:
            self.print_info('***Settings Menu***')
            self.print_help("'Show' or 'edit' settings.")
            action = input('>>')
            if action == 'show':
                ConsolePrintOut().print_model(Settings)
            elif action == 'edit':
                self.edit_settings()
            elif action == 'back':
                return
            elif action == 'help':
                pass
            else:
                self.print_warn("Unknown command. Type 'help' for the list of available options.")

    def edit_settings(self):
        self.print_help("Provide a multiplier of the following settings:")
        Settings.objects[0].modify_parameters(
            length=self._modify_setting('length', '1m'),
            force=self._modify_setting('force', '1N'),
            pressure=self._modify_setting('pressure', '1Pa'),
            time=self._modify_setting('time', '1s'),
        )

    def _modify_setting(self, param, unit):
        self.print_help("The {param}'s unit of reference is {unit}".format(param=param, unit=unit))
        return self.int_value_input(param)


if __name__ == '__main__':
    ConsoleMode().run()
