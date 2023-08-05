from blockly_executor.core.exceptions import ServiceException, ErrorInBlock
from blockly_executor.core.block_templates.simple_block import SimpleBlock
from blockly_executor import ExtException


class ExecuteWorkspace(SimpleBlock):

    async def _calc_value(self, node, path, context, block_context):
        try:
            params_count = int(self.workspace.find_mutation_by_name(node, 'param_count', 0))
            workspace_name = block_context['NAME']
            endpoint = block_context.get('ENDPOINT')
            if '_previous_workspace' not in block_context:
                block_context['_previous_workspace'] = self.executor.workspace.name
            if '_child' not in block_context:
                block_context['_child'] = {'variable_scopes': [{}]}
                for i in range(params_count):
                    key = block_context.get(f'PARAM_NAME_{i}')
                    value = block_context.get(f'PARAM_VALUE_{i}')
                    block_context['_child']['variable_scopes'][0][key] = value

            nested_context = context.init_nested(block_context, workspace_name)
            result = await self.executor.execute_nested(
                nested_context,
                endpoint=endpoint,
                commands_result=self.executor.commands_result,
            )
            self.executor.workspace.name = block_context['_previous_workspace']
            return result
        except ServiceException as err:
            raise err from err
        except Exception as err:
            raise ErrorInBlock(parent=err)
