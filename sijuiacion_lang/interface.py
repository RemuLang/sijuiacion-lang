import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=SyntaxWarning)    
    from sijuiacion_lang.codegen import Codegen
    from sijuiacion_lang.parser_wrap import parse

def load_sij(source: str):
    return Codegen().start(parse(source))
    
def run_sij(path: str):
    with open(path) as f:
        code = load_sij(f.read())
    print(eval(code))

def main():
    from argser import call
    call(run_sij)
