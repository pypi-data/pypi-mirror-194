from blockly_executor.plugins.standard_blocks.blocks.procedures_defnoreturn import ProceduresDefnoreturn
from blockly_executor.plugins.standard_blocks.blocks.procedures_defreturn import ProceduresDefreturn
from .workspace import Workspace


class WorkspaceJson(Workspace):
    version = 'json'

    def __init__(self, executor, data, name, logger):
        super().__init__(executor, data, name, logger)
        try:
            self.blocks = data['blocks']['blocks']
        except (KeyError, TypeError):
            self.blocks = []

        try:
            self.variables = data['variables']
        except (KeyError, TypeError):
            self.blocks = []

    def read_procedures_and_functions(self):
        self.functions = {}
        _handler = {
            'procedures_defreturn': ProceduresDefreturn,
            'procedures_defnoreturn': ProceduresDefnoreturn
        }
        for node in self.blocks:
            if node['type'] in _handler:
                name = node['fields']['NAME']
                self.functions[name] = _handler[node['type']].init(self.executor, name, node, logger=self.logger)

    def read_variables(self):
        result = {}
        for var in self.variables:
            result[var['id']] = var['name']
        return result

    @classmethod
    def get_child_block(cls, node):
        child = None
        if node:
            if isinstance(node, dict):
                child = node.get('block')
                if child is None:
                    return node.get('shadow')
            elif isinstance(node, list):  # root
                for elem in node:
                    if elem['type'] not in ['procedures_defreturn', 'procedures_defnoreturn']:
                        return elem

        return child

    @classmethod
    def find_child_blocks(cls, node):
        blocks = []
        if node:
            if isinstance(node, dict):
                child = node.get('block')
                if child is None:
                    child = node.get('shadow')
                if child is not None:
                    blocks.append(child)
            elif isinstance(node, list):  # root
                blocks = node
        return blocks

    @classmethod
    def find_field_by_name(cls, node, name):
        try:
            return node['fields'][name]
        except (KeyError, TypeError):
            return None

    @classmethod
    def find_statement_by_name(cls, node, name):
        return cls.find_input_by_name(node, name)

    @classmethod
    def get_next_statement(cls, node):
        try:
            return node['next']
        except (KeyError, TypeError):
            return None

    @classmethod
    def find_mutation_by_name(cls, node, name, default=None):
        mutation = node.get('extraState')
        if mutation is not None:
            return mutation.get(name, default)
        return default

    @classmethod
    def find_mutation_args(cls, node):
        mutation = node.get('extraState')
        if mutation is not None:
            return mutation.get('params')
        return None

    @classmethod
    def find_inputs(cls, node):
        return node.get('inputs', {})

    @classmethod
    def find_input_by_name(cls, node, name):
        try:
            return node['inputs'][name]
        except (KeyError, TypeError):
            return None

    def find_fields(self, block, node, path, context, block_context):
        fields = node.get('fields')
        if fields is not None:
            for _param_name in fields:
                _value = fields[_param_name]
                if isinstance(_value, dict):
                    block_context[_param_name] = self.variables[_value['id']]
                else:
                    block_context[_param_name] = _value

    async def execute_inputs(self, block, node, path, context, block_context):
        inputs = node.get('inputs')
        if inputs is not None:
            for name in inputs:
                if block.statement_inputs and name in block.statement_inputs:
                    continue
                if name not in block_context:
                    block_context[name] = await block.execute_all_next(
                        inputs[name], f'{path}.{name}', context, block_context)
