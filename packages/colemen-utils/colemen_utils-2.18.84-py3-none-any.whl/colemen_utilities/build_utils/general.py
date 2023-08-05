'''
    Description

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 02-24-2023 06:04:49
    `name`: general
    * @TODO []: documentation for general
'''





import base64
import importlib
import os
from string import Template
import subprocess
import sys
from typing import Union,Iterable

from importlib.machinery import SourceFileLoader
# import colemen_utils as c
import colemen_utilities.string_utils as _csu
import colemen_utilities.directory_utils as _cdir
import colemen_utilities.file_utils as _f
import colemen_utilities.list_utils as _arr




# PATHS = [
#     f"./apricity",
# ]

def list_py_modules(
    root_path:str,
    exclude:Union[str,list]=None,
    additions:Union[str,list]=None,
    print_outputs:bool=False,
    )->Iterable[str]:
    '''
        Compile a list of module import paths for the setuptools setup method.

        ----------

        Arguments
        -------------------------
        `root_name` {str}
            The name of the directory to search in, this must be located in the same directory
            as the setup.py file.

        [`additions`=None] {str,list}
            A list of import paths to add include.
            This where you can imports that are in the root folder of the package (same folder as the setup.py)
            These are added verbatim, so don't fuck up.

        [`exclude`=None] {str,list}
            A list of strings, if any of these are found in a file path, that file will not be included
            __pycache__ directories are always ignored.

        [`print_outputs`=False] {bool}
            If True the imports are printed to console.


        Return {list}
        ----------------------
        A list of import path strings.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 02-24-2023 06:54:02
        `memberOf`: general
        `version`: 1.0
        `method_name`: list_py_modules
        * @xxx [02-24-2023 07:03:03]: documentation for list_py_modules
    '''
    output = []
    root_name = os.path.basename(root_path)
    root_path = os.path.dirname(root_path)

    paths = [f"{root_path}/{root_name}"]
    exclude_base = ['__pycache__',' - Copy']
    if isinstance(exclude,(str)):
        exclude = _arr.force_list(exclude,allow_nulls=False)
    exclude_base = exclude_base + [exclude]
    additions = _arr.force_list(additions,allow_nulls=False)

    for path in paths:

        path = _csu.file_path(path)
        if _cdir.exists(path) is False:
            if path.startswith("./"):
                test_path = path.replace("./",root_path)
                if _cdir.exists(test_path):
                    path = test_path
            else:
                continue

        dir_name = os.path.basename(path)
        files = _f.get_files_obj(path,extensions=['.py'],exclude=['__pycache__'])
        for file in files:

            module_path = f"{root_name}"
            # module_path = f"{root_name}\\{dir_name}"
            # print(f"module_path: {module_path}")
            module_dot_name = f"{root_name}"
            # print(f"module_dot_name: {module_dot_name}")
            file_path = f"{module_path}\\{file.dir_path.replace(path,'')}\\{file.name_no_ext}"
            if file.name == "__init__.py":
                file_path =f"{module_path}\\{file.dir_path.replace(path,'')}"

            dot_name = file_path.replace("\\",".")
            dot_name = _csu.strip_excessive_chars(dot_name,["."])
            # dot_name = re.sub(r'[\.]{2,}',".",dot_name)

            if dot_name == f"{module_dot_name}.":
                dot_name = module_dot_name

            output.append(dot_name)

        output = sorted(output)


    output = _arr.remove_duplicates(output)
    output = _arr.force_list(additions) + output

    if print_outputs:
        for o in output:
            print(f"'{o}',")
    list_path = _csu.file_path(f"{root_path}/package_build_settings.json")
    settings = _f.read.as_json(list_path)
    if settings is not False:
        settings['py_modules'] = output
        _f.writer.to_json(list_path,settings)

    return output

def purge_dist(root_path:str=None):
    '''
        Deletes the dist folder from the project directory.

        ----------


        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-02-2022 08:40:48
        `memberOf`: build_utils
        `version`: 1.0
        `method_name`: purge_dist
        * @xxx [12-02-2022 08:41:15]: documentation for purge_dist
    '''
    if root_path is None:
        root_path = os.getcwd()

    path = f"{root_path}/dist"
    if _cdir.exists(path):
        _cdir.delete(path)

def create_build_utils_batch(user_name:str=None,password:str=None):
    '''
        Create the build_utils directory and the build_package module.

        Then create the major,minor,patch release batches.

        When you run any of these batch files, they will build the package and optionally
        upload the package to pypi.

        ----------

        Arguments
        -------------------------
        `user_name` {str}
            Pypi user name

        `password` {str}
            pypi password.

        Keyword Arguments
        -------------------------
        `arg_name` {type}
            arg_description

        Return {type}
        ----------------------
        return_description

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 02-25-2023 11:37:42
        `version`: 1.0
        `method_name`: create_build_utils_batch
        * @TODO []: documentation for create_build_utils_batch
    '''
    _confirm_preparations()
    template = _f.readr(f"{os.getcwd()}/colemen_utilities/build_utils/build_package.template")
    s = Template(template)
    if user_name is None:
        user_name = "none"
        password = "none"
    else:
        user_name = base64.b64encode(user_name.encode("ascii")).decode("ascii")
        password  = base64.b64encode(password.encode("ascii")).decode("ascii")


    out = s.substitute(
        user_name=user_name,
        password=password,
    )

    utils_path = f"{os.getcwd()}/build_utils"
    build_package_path = f"{utils_path}/build_package.py"
    _cdir.create(utils_path)
    _f.write(build_package_path,out)

    module = SourceFileLoader("build_package",build_package_path).load_module()
    module.create_release_batches()

def build_this_package(release:str="patch",user_name:str=None,password:str=None):
    release = release.lower()
    releases = ["major","minor","patch"]
    if release not in releases:
        raise ValueError(f"The release value must be :[{', '.join(releases)}]")
    utils_path = f"{os.getcwd()}/build_utils"
    build_package_path = f"{utils_path}/build_package.py"
    create_build_utils_batch(user_name,password)
    module = SourceFileLoader("build_package",build_package_path).load_module()
    module.main(release)


def _confirm_preparations():
    import importlib.util
    import sys
    setup_path = f"{os.getcwd()}/setup.py"
    if _f.exists(setup_path) is False:
        raise TypeError("Failed to locate the setup.py file.")

    # @Mstep [] install wheel and twine if necessary.
    packages = ["wheel","twine"]
    # print(sys.modules)
    for name in packages:
        if importlib.util.find_spec(name) is None:
            install(name)


    #     if name not in sys.modules:
    #         install(name)

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
# def compile_manifest(
#     paths:Union[str,list],
#     exclude:Union[str,list]=None,
#     )->Iterable[str]:
#     paths = _arr.force_list(paths)
#     base_exclude = ["/Lib/","/Scripts/"] + _arr.force_list(exclude,allow_nulls=False)

#     cwd = root_path
#     for path in paths:
#         path = _csu.file_path(path,url=True)
#         files = _f.get_files_obj(path,exclude=base_exclude)
#         for file in files:
#             rel_path = file.file_path.replace(cwd,'')
#             print(f"rel_path:{rel_path}")

