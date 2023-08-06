from . import Performance, Transaction
from .partials import HOST
from .enums import ModelType
import sys
import traceback


class Error(Performance):
    model = ''
    timestamp = 0
    host = None
    transaction = None
    class_name = None
    file = None
    line = None
    code = 0
    stack = []
    handled = False
    message = ''
    __prev_number_line = 5
    __next_number_line = 5

    def __init__(self, throwable: Exception, transaction: Transaction):
        Performance.__init__(self)
        self.model = ModelType.ERROR.value
        self.timestamp = self.get_microtime()
        self.host = HOST()
        self.transaction = transaction
        self.message = str(throwable)
        self.stack = []

        ex_type, ex_value, ex_traceback = sys.exc_info()
        trace_back = traceback.extract_tb(ex_traceback)

        self.class_name = throwable.__class__.__name__
        self.file = trace_back[0].filename
        self.code = trace_back[0].line
        self.line = trace_back[0].lineno
        i = 0
        for trace in trace_back:
            item_stack = {
                "class": trace.filename,
                "function": trace.name,
                "args": [],
                "type": "",
                "file": trace.filename,
                "line": trace.lineno,
                "code": self.get_code(trace.filename, trace.lineno)
            }
            self.get_code(trace.filename, trace.lineno)
            self.stack.append(item_stack)

    def set_handled(self, value):
        self.handled = value
        return self

    def stack_trace_to_array(self, stack_trace, top_file=None, top_line=None):
        pass

    def stack_trace_args_to_array(self, trace):
        pass

    def get_code(self, file_path: str, line: int):
        fp = open(file_path)
        code = {}
        cont = 0
        for i, row in enumerate(fp):
            if (line - self.__prev_number_line) <= i <= (line + self.__next_number_line):
                item_code = {
                    "code": row.strip("\n"),
                    "line": i
                }
                code[cont] = item_code
                cont = cont + 1
        return code

    def get_json(self) -> str:
        json_str = Performance.get_json(self)
        json_str['class'] = json_str['class_name']
        del json_str['class_name']
        return json_str
