import os
import re
from src.models.meta import ObjectDoesNotExist


class ConsolePrints(object):
    def print_error(self, msg):
        self._print_modified(msg, '\033[31;1m')  # red

    def print_info(self, msg):
        self._print_modified(msg, '\033[32;1m')  # green

    def print_warn(self, msg):
        self._print_modified(msg, '\33[33;1m')  # yellow

    def print_help(self, msg):
        self._print_modified(msg, '\033[36;1m')  # cyan

    @staticmethod
    def _print_modified(msg, color):
        print(color + msg + '\033[0m')


class ConsoleInputs(ConsolePrints):
    def int_value_input(self, msg):
        return self._value_input(
            pattern=r'^-?[0-9]+$',
            msg=msg,
            _type=int,
            warn="Input should be a whole number!"
        )

    def string_value_input(self, msg):
        return self._value_input(
            pattern=r'^[a-zA-Z][a-zA-Z1-9_]+$',
            msg=msg,
            _type=str,
            warn="Input should start with a letter, and should not contain spaces or special signs!"
        )

    def float_value_input(self, msg):
        return self._value_input(
            pattern=r'^-?[0-9]+(\.[0-9]{0,2})?$',
            msg=msg,
            _type=float,
            warn="Number must be whole or decimal up to 2 decimal places!"
        )

    def float_value_lt_one_input(self, msg):
        return self._value_input(
            pattern=r'^0.[0-9]{1,2}$',
            msg=msg,
            _type=float,
            warn="Number must be decimal up to 2 decimal places between 0 and 1!"
        )

    def bool_value_input(self, msg):
        while True:
            action = input(msg + ' :')
            if re.search(r'^((?i)[t](rue)?)$', action):
                return True
            elif re.search(r'^((?i)[f](alse)?)$', action):
                return False
            else:
                self.print_warn("You should type '(t)rue' or '(f)alse'")

    def _value_input(self, pattern, msg, _type, warn):
        while True:
            action = input(msg+' :')
            if re.search(pattern, action):
                return _type(action)
            else:
                self.print_warn(warn)


class TemplateMenu(ConsoleInputs, ConsolePrints):
    def _view_help(self, help_path):
        with open(os.path.dirname(__file__) + help_path, 'r') as f:
            print(f.read())


class ConsoleObjectMenu(TemplateMenu):
    """This is a template for other model menus"""
    obj = None

    def object_menu(self):
        self.print_help("Do you want to 'add', 'list' {name}s, 'delete' them, or 'back' to main?".format(name=self.obj.name))
        while True:
            self.print_info("***{name} Menu***".format(name=self.obj.name.capitalize()))
            action = input('>>')
            if action == 'add':
                self.print_help("Provide the following values:")
                self._add_object()
                self.print_info('{name} created!'.format(name=self.obj.name))
            elif action == 'list':
                ConsolePrintOut().print_model(self.obj)
            elif action == 'delete':
                self._delete_menu()
            elif action == 'help':
                self._view_help('\\help_sub_msg.txt')
            elif action == 'back':
                return
            else:
                self.print_warn("Unknown command. Type 'help' for the list of available options.")

    def _delete_menu(self):
        if self.obj.objects:
            ConsolePrintOut().print_model(self.obj)
        else:
            self.print_warn('No {name}s to delete. Back to {name} Menu.'.format(name=self.obj.name))
            return
        while True:
            self.print_info('***{name} Delete Menu***'.format(name=self.obj.name))
            self.print_help("Type _id of the {name} to be removed, 'list' or 'back' to cancel".format(name=self.obj.name))
            action = input('>>')
            if action == 'back':
                return
            elif action == 'list':
                ConsolePrintOut().print_model(self.obj)
            else:
                try:
                    obj_to_remove = self.obj.get_obj_by_params(_id=int(action))
                except ObjectDoesNotExist:
                    self.print_warn("Wrong id! Try again or 'back' to cancel")
                except ValueError:
                    self.print_warn("Wrong id! Try again or 'back' to cancel")
                else:
                    self.obj.remove(obj_to_remove)
                    self.print_info("{name} was successfully removed!".format(name=self.obj.name))

    def _add_object(self):
        """
        Should be overwritten with specific model.
        :return:
        """
        pass

    def _view_help(self, help_path):
        with open(os.path.dirname(__file__) + help_path, 'r') as f:
            print(f.read().format(object=self.obj.name))


class ConsolePrintOut(ConsolePrints):
    def print_model(self, model):
        try:
            instance = model.objects[0]
        except IndexError:
            return self.print_warn('No {name}s created yet.'.format(name=model.name))
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
