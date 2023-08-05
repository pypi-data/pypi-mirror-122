import inspect
import os
import pkgutil
import sys

from robot.libdocpkg import LibraryDocumentation

from service.keywords.models import Keyword, Param


def check_keyword_functions(obj):
    result = []
    for name, item in inspect.getmembers(obj):
        try:
            if hasattr(item, "robot_name"):
                params = []
                for param in item.__code__.co_varnames:
                    if param != "self":
                        params.append(Param(param))
                result.append(Keyword(name=name, params=params))
        except:
            continue

    return result


def find_all_keywords(package):
    result = []
    for name, obj in inspect.getmembers(package, predicate=inspect.isclass):
        result += check_keyword_functions(obj)

    return result


def find_in_module(module):
    if module not in sys.modules:
        __import__(module)
    module_path = sys.modules[module].__file__
    if module_path.endswith("__init__.py"):
        module_path = os.path.dirname(module_path)
    result = find_all_keywords(sys.modules[module])

    for package in pkgutil.walk_packages([module_path]):
        if package.ispkg:
            result += find_in_module(module + "." + package.name)

    return list({object_.name: object_ for object_ in result}.values())


def find_library_context_in_package(
    modules=[
        "Browser.keywords",
        "RPA.Browser.Playwright",
        "RPA.Browser.Selenium",
        "RPA.SAP",
        "RPA.Excel",
        "RPA.Desktop",
        "RPA.Dialogs",
        "RPA.Excel",
        "RPA.Outlook",
    ]
):
    result = []
    for module in modules:
        item = {"library": module, "keywords": find_in_module(module)}
        if module == "RPA.Browser.Selenium":
            item["keywords"] += [
                Keyword(
                    name="Wait Until Element Is Visible",
                    params=[
                        Param(name="locator"),
                        Param(name="timeout"),
                        Param(name="error"),
                    ],
                ),
                Keyword(name="Click Element", params=[Param(name="locator"),]),
                Keyword(
                    name="Input Text",
                    params=[
                        Param(name="locator"),
                        Param(name="text"),
                        Param(name="clear"),
                    ],
                ),
            ]
        result += [item]

    return result


def get_all_keywords():
    modules = [
        "BuiltIn",
        "OperatingSystem",
        "Collections",
        "DateTime",
        "Dialogs",
        "Process",
        "Reserved",
        "Screenshot",
        "String",
        "XML",
        "RPA.Archive",
        "RPA.Browser",
        "RPA.Browser.Playwright",
        "RPA.Browser.Selenium",
        "RPA.Cloud",
        "RPA.Cloud.AWS",
        "RPA.Cloud.Azure",
        "RPA.Crypto",
        "RPA.Database",
        "RPA.Desktop",
        "RPA.Desktop.Clipboard",
        "RPA.Desktop.OperatingSystem",
        "RPA.Desktop.Windows",
        "RPA.Dialogs",
        "RPA.Email.Exchange",
        "RPA.Email.ImapSmtp",
        "RPA.Excel.Application",
        "RPA.Excel.Files",
        "RPA.FTP",
        "RPA.FileSystem",
        "RPA.HTTP",
        "RPA.Images",
        "RPA.JSON",
        "RPA.JavaAccessBridge",
        "RPA.Netsuite",
        "RPA.Notifier",
        "RPA.Outlook.Application",
        "RPA.PDF",
        "RPA.RobotLogListener",
        "RPA.SAP",
        "RPA.Salesforce",
        "RPA.Slack",
        "RPA.Tables",
        "RPA.Tasks",
        "RPA.Twitter",
        "RPA.Word.Application",
    ]
    result = []
    for module in modules:
        arguments = [module, "list"]
        name = (module,)
        docformat = "REST"
        version = ""
        lib_or_res, output = arguments[:2]
        libdoc = LibraryDocumentation(lib_or_res, name, version, docformat)
        item = {
            "library": module,
            "keywords": [
                Keyword(
                    name=x.name,
                    short_doc=x.shortdoc,
                    doc=x.doc,
                    params=[Param(name=y) for y in x.args.argument_names],
                )
                for x in libdoc.keywords
            ],
        }
        result.append(item)

    return result
