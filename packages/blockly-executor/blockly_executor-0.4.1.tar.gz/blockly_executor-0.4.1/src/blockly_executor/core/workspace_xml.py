import xml.etree.ElementTree as XmlTree

from blockly_executor.plugins.standard_blocks.blocks.procedures_defnoreturn import ProceduresDefnoreturn
from blockly_executor.plugins.standard_blocks.blocks.procedures_defreturn import ProceduresDefreturn
from blockly_executor.plugins.standard_blocks.blocks.root import Root
from .workspace import Workspace


class WorkspaceXml(Workspace):
    ns = {'b': 'https://developers.google.com/blockly/xml'}
    version = 'xml'

    def __init__(self, executor, data, name, logger):
        super().__init__(executor, data, name, logger)
        self.data = self.workspace_to_tree(data)
        self.blocks = self.data

    @staticmethod
    def workspace_to_tree(workspace_raw):
        XmlTree.register_namespace('', 'https://developers.google.com/blockly/xml')
        return XmlTree.fromstring(workspace_raw)

    def read_procedures_and_functions(self):
        self.functions = {}
        for node in self.data.findall("./b:block[@type='procedures_defreturn']", self.ns):
            name = node.find("./b:field[@name='NAME']", self.ns).text
            self.functions[name] = ProceduresDefreturn.init(self.executor, name, node, logger=self.logger)

        for node in self.data.findall("./b:block[@type='procedures_defnoreturn']", self.ns):
            name = node.find("./b:field[@name='NAME']", self.ns).text
            self.functions[name] = ProceduresDefnoreturn.init(self.executor, name, node, logger=self.logger)

    def read_variables(self):
        result = {}
        for node in self.data.findall("./b:variables/b:variable", self.ns):
            name = node.text
            _id = node.attrib.get('id')
            result[_id] = name
        return result

    @classmethod
    def get_child_block(cls, node):
        child = None
        if node:
            child = node.find('./b:block', cls.ns)
            if child is None:
                child = node.find('./b:shadow', cls.ns)
        return child

    @classmethod
    def find_child_blocks(cls, node):
        blocks = []
        if node:
            for child in node:
                if child.tag.endswith('block'):
                    blocks.append(child)
        return blocks

    @classmethod
    def find_field_by_name(cls, node, name):
        return node.find(f"./b:field[@name='{name}']", cls.ns).text

    @classmethod
    def find_statement_by_name(cls, node, name=None):
        if name:
            return node.find(f"./b:statement[@name='{name}']", cls.ns)
        else:
            return node.find(f"./b:statement", cls.ns)

    @classmethod
    def get_next_statement(cls, node):
        return node.find(f"./b:next", cls.ns)

    @classmethod
    def find_mutation_by_name(cls, node, name, default=None):
        mutation = node.find(f"./b:mutation", cls.ns)
        if mutation is None:
            return default
        return mutation.get(name, default)

    @classmethod
    def find_mutation_args(cls, node):
        result = []
        args = node.findall(f'./b:mutation/b:arg', cls.ns)
        if args is not None:
            for arg in args:
                result.append(arg.get('name'))
        return result

    @classmethod
    def find_inputs(cls, node):
        inputs = node.findall("./b:value", cls.ns)
        result = {}
        if inputs is not None:
            for input in inputs:
                input_name = input.get('name')
                result[input_name] = input
        return result

    @classmethod
    def find_input_by_name(cls, node, name):
        return node.find(f"./b:value[@name='{name}']", cls.ns)

    def find_fields(self, block, node, path, context, block_context):
        fields = node.findall("./b:field", self.ns)
        if fields is None:
            return

        for i in range(len(fields)):
            _param_name = fields[i].get('name')
            block_context[_param_name] = fields[i].text

    async def execute_inputs(self, block, node, path, context, block_context):
        inputs = node.findall("./b:value", self.ns)
        if inputs is None:
            return

        for i in range(len(inputs)):
            _param_name = inputs[i].get('name')
            if _param_name not in block_context:
                block_context[_param_name] = await block.execute_all_next(
                    inputs[i], f'{path}.{_param_name}', context, block_context)
