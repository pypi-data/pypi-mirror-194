# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['impall']
setup_kwargs = {
    'name': 'impall',
    'version': '1.2.0',
    'description': '🛎 Test-import all modules below a given root 🛎',
    'long_description': "🏁  impall: automatically import all Python modules for testing   🏁\n\nIndividually and separately imports each Python module or file in a project and\nreports warnings or failures at the end.\n\n### Running impall as a unit test\n\nJust inherit from the base class and it will\nautomatically find and import each file, like this.\n\n    import impall\n\n    class ImpAllTest(impall.ImpAllTest):\n        pass\n\n(You can copy [this file](https://github.com/rec/impall/blob/master/all_test.py)\ninto your project if you like.)\n\nTests are customized by overriding one of these following properties in the\nderived class.\n\n    CLEAR_SYS_MODULES, EXCLUDE, FAILING, INCLUDE, MODULES, PATHS,\n    RAISE_EXCEPTIONS, and WARNINGS_ACTION.\n\nFor example, to turn warnings into errors, set the property\nWARNINGS_ACTION in the derived class definition, like this.\n\n    class ImpAllTest(impall.ImpAllTest):\n        WARNINGS_ACTION = 'error'\n\n## Running impall as a command-line utility\n\n    $ impall.py --warnings_action=error\n    $ impall.py -w error\n\nThe properties INCLUDE, EXCLUDE, and PROJECT_PATH can be\nlists of strings, or a string separated with colons like\n'foo.mod1:foo.mod2'\n\nINCLUDE and EXCLUDE match modules, and also allow * as a wildcard.\nA single * matches any module segment, and a double ** matches any\nremaining segments. For example,\n\nINCLUDE = 'foo', 'bar.*', 'baz.**'\n\n* matches `foo` but not `foo.foo`\n* matches `bar.foo` but not `bar` or `bar.foo.bar`\n* matches `baz.foo` as well as `baz.foo.bar` but not `baz`\n\n### A note on side-effects\n\nto reduce side-effects, `sys.modules` is restored to its original\ncondition after each import if CLEAR_SYS_MODULES is true, but there might be\nother side-effects from loading some specific module.\n\nUse the EXCLUDE property to exclude modules with undesirable side\neffects. In general, it is probably a bad idea to have significant\nside-effects just from loading a module.\n\n\n### [API Documentation](https://rec.github.io/impall#impall--api-documentation)\n",
    'author': 'Tom Ritchford',
    'author_email': 'tom@swirly.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rec/impall',
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
