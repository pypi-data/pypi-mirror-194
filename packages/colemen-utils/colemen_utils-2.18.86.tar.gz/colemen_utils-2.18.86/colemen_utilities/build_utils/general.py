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
    template_path = f"{os.getcwd()}/colemen_utilities/build_utils/build_package.template"
    if _f.exists(template_path) is False:
        template_path = f"{os.getcwd()}/Lib/site-packages/colemen_utilities/build_utils/build_package.template"
        
    if _f.exists(template_path) is False:
        raise ValueError("Failed to locate the Colemen Utils Template")

    print(f"template_path:{template_path}")
    template = _f.readr(template_path)
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
    '''
        Build this package's tar file and optionally upload it to pypi.

        ----------

        Arguments
        -------------------------
        `release` {str}
            The release version to increment [major,minor,patch]

        [`user_name`=None] {str}
            Your Pypi user name.

        [`password`=None] {str}
            Your Pypi password.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 02-25-2023 12:39:38
        `memberOf`: general
        `version`: 1.0
        `method_name`: build_this_package
        * @xxx [02-25-2023 12:41:47]: documentation for build_this_package
    '''
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
    '''
        Confirm that the setup.py file exists and that wheel twine are installed;
        ----------

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 02-25-2023 12:38:46
        `memberOf`: general
        `version`: 1.0
        `method_name`: _confirm_preparations
        `raises`: TypeError
        * @xxx [02-25-2023 12:39:16]: documentation for _confirm_preparations
    '''
    import importlib.util
    import sys
    setup_path = f"{os.getcwd()}/setup.py"
    if _f.exists(setup_path) is False:
        raise TypeError("Failed to locate the setup.py file.")

    # @Mstep [] install wheel and twine if necessary.
    packages = ["wheel","twine"]
    # print(sys.modules)
    for name in packages:
        is_package_installed(name,auto_install=True)

def install(package):
    '''
        Install a python pip package.
        ----------

        Arguments
        -------------------------
        `package` {str}
            The name of the package to install


        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 02-25-2023 12:38:02
        `version`: 1.0
        `method_name`: install
        * @xxx [02-25-2023 12:38:39]: documentation for install
    '''
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def is_package_installed(package:Union[str,list],auto_install:bool=False,return_missing:bool=True)->Union[list,bool]:
    '''
        Check if a package installed.

        ----------

        Arguments
        -------------------------
        `package` {list,string}
            A package name or list of package names to check on.
        [`auto_install`=False] {bool}
            If True and a package is not installed, it will install it with pip.
        [`return_missing`=True] {bool}
            If True, this will return a list of missing package names, otherwise a boolean


        Return {list,bool}
        ----------------------
        A list of missing packages if `return_missing` is True, a boolean otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 02-25-2023 12:46:33
        `memberOf`: general
        `version`: 1.0
        `method_name`: is_package_installed
        * @xxx [02-25-2023 12:48:58]: documentation for is_package_installed
    '''
    pkgs = _arr.force_list(package,allow_nulls=False)
    missing = []
    for name in pkgs:
        if importlib.util.find_spec(name) is None:
            if auto_install is True:
                install(name)
            else:
                missing.append(name)
    if len(missing) > 0:
        if return_missing is True:
            return missing
        else:
            return False
    return True



