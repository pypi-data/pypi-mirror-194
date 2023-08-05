from abc import ABCMeta, abstractmethod

from blockly_executor.plugins.standard_blocks.blocks.root import Root


class Workspace:
    __metaclass__ = ABCMeta
    version = None

    def __init__(self, executor, data, name, logger):
        self.executor = executor
        self.name = name
        self.data = data
        self.blocks = None
        self.functions = None
        self.variables = None
        self.logger = logger

    def get_start_block(self, endpoint, context):
        # стартуем с функции
        self.read_procedures_and_functions()
        self.variables = self.read_variables()
        if endpoint:
            try:
                block = self.functions[endpoint]
            except KeyError:
                context.status = 'error'
                context.result = f'not found endpoint {endpoint}'
                return context
        else:
            try:
                block = self.functions['main']
            except KeyError:
                block = Root.init(self.executor, '', self.blocks, logger=self.logger)
        return block

    @abstractmethod
    def read_procedures_and_functions(self):
        raise NotImplementedError()

    @abstractmethod
    def read_variables(self):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get_child_block(cls, node):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def find_child_blocks(cls, node):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def find_field_by_name(cls, node, name):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def find_statement_by_name(cls, node, name):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get_next_statement(cls, node):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def find_mutation_by_name(cls, node, name, default=None):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def find_mutation_args(cls, node):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def find_inputs(cls, node) -> dict:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def find_input_by_name(cls, node, name):
        raise NotImplementedError()

    @abstractmethod
    def find_fields(self, block, node, path, context, block_context):
        raise NotImplementedError()

    @abstractmethod
    async def execute_inputs(self, block, node, path, context, block_context):
        raise NotImplementedError()
