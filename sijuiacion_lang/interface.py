from importlib._bootstrap_external import _code_to_hash_pyc
from importlib.util import source_hash

import warnings
import bytecode as bytec

with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=SyntaxWarning)
    from sijuiacion_lang.codegen import Codegen
    from sijuiacion_lang.parser_wrap import parse


def _code_template():
    runtime = __import__("runtime").__dict__
    code, info = "code"

    def nest(code, info):
        co_consts = code.co_consts
        for eval_str, index in info[0].items():
            co_consts[index].append(eval(eval_str, runtime))
        for index, nest_info in info[1]:
            nest(co_consts[index], nest_info)

    nest(code, info)
    exec(code)


def link_constants(cg, code, info):
    instrs = bytec.Bytecode.from_code(_code_template.__code__)
    const_map = {"runtime": cg.cg.env.__name__, 'code': (code, info)}

    for each in instrs:
        if isinstance(each, bytec.Instr):
            if each.name == 'LOAD_CONST':
                arg = const_map.get(each.arg)
                if arg:
                    each.arg = arg
    return instrs.to_code()


def load_sij(source: str):
    cg = Codegen()
    code, info = cg.start(parse(source))
    mk = link_constants(cg, code, info)
    return mk


def run(path: str):
    with open(path) as f:
        code = load_sij(f.read())
    exec(code)


def cc(path: str, out: str):
    with open(path, 'rb') as f:
        source = f.read()
        code = load_sij(source.decode('utf8'))
    with open(out, 'wb') as f:
        data = _code_to_hash_pyc(code, source_hash(source))
        f.write(data)


def main():
    import argser
    subs = argser.SubCommands()
    subs.add(run)
    subs.add(cc)
    subs.parse()
