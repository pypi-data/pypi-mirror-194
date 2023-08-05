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




import os
from typing import Union,Iterable
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

def purge_dist():
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
    path = f"{root_path}/dist"
    if _cdir.exists(path):
        _cdir.delete(path)

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

