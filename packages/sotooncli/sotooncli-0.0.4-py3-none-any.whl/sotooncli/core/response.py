from enum import Enum

import click

from sotooncli.config_utils import set_config
from sotooncli.globals.output_format import OutputFormatOption

ACTIONS = "actions"
TYPE = "type"


class ActionType(Enum):
    OUTPUT = "output"
    SAVE = "save"


class ActionBuilder:
    @staticmethod
    def build(ac_data, cmd_result, ctx, state):
        ac_type = ac_data[TYPE]
        if ac_type == ActionType.SAVE.value:
            save_dict = {}
            for res_key, conf_key in ac_data["map"].items():
                if isinstance(cmd_result, dict) and res_key in cmd_result:
                    save_dict[conf_key] = cmd_result[res_key]
            return SaveAction(save_dict)
        elif ac_type == ActionType.OUTPUT.value:
            output_format = OutputFormatOption().get_value(state, ctx)
            return OutputAction(output_format, cmd_result)
        else:
            raise click.ClickException("Invalid action type")


class Action:
    def act(self):
        raise NotImplementedError


class OutputAction(Action):
    def __init__(self, output_format, data):
        formatter = OutputFormatOption.get_formatter(output_format)
        self.formatted_data = formatter.format(data)

    def act(self):
        click.echo(self.formatted_data)


class SaveAction(Action):
    def __init__(self, save_dict):
        self.save_dict = save_dict

    def act(self):
        for k, v in self.save_dict.items():
            set_config(k, v)


class ResponseType(Enum):
    LIST = "list"
    SINGLE = "single"


class Response:
    _RESPONSE_DATA_KEY = {
        ResponseType.LIST.value: "items",
        ResponseType.SINGLE.value: "item",
    }

    def __init__(self, result, state, ctx):
        if not result[TYPE] or result[TYPE] not in self._RESPONSE_DATA_KEY:
            raise click.ClickException("Invalid response type")
        self.data = result[self._RESPONSE_DATA_KEY[result[TYPE]]]
        self.state = state
        self.ctx = ctx
        self.actions = []
        if ACTIONS in result:
            self._init_actions(result[ACTIONS])
        else:
            self._init_actions([{TYPE: ActionType.OUTPUT.value}])

    def _init_actions(self, action_list):
        for ac_data in action_list:
            self.actions.append(
                ActionBuilder.build(ac_data, self.data, self.ctx, self.state)
            )

    def execute(self):
        for action in self.actions:
            action.act()
