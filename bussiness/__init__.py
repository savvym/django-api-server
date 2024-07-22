def mount():
    import pathlib
    import os
    import ast
    import traceback
    import logging

    log = logging.getLogger('django')
    py_files = pathlib.Path(os.path.dirname(__file__)).glob('**/*.py')
    for py_file in py_files:
        log.debug("py_file: {0}".format(py_file))
        try:
            has_entry = [
                i for i in ast.walk(ast.parse(open(py_file).read()))
                if i.__dict__.get('name') == 'entry' and isinstance(
                    i, ast.FunctionDef)
            ]
        except:
            log.warning(py_file, "not vaild.")
            log.warning(f'{py_file}不是一个有效的Python文件')
            continue
        if has_entry:
            parted = str(py_file).split('/')[-3:]
            parted[-1] = parted[-1].split('.')[0]
            log.info('.'.join(parted))
            try:
                log.debug('正在加载：' + '.'.join(parted))
                __import__('.'.join(parted))
            except Exception as e:
                log.error(f'{e}')
                log.error(f'{e}')
                log.error(traceback.format_exc())

