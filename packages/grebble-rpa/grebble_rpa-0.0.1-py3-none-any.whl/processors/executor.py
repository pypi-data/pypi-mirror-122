import os
import shutil
import tempfile
from dataclasses import dataclass
from robot.run import run

from dataclasses_json import dataclass_json
from grebble_flow.processors.base import BaseFlowProcessor
from grebble_flow.processors import models
from grebble_flow.processors.session import Session


@dataclass
@dataclass_json
class RPAProcessorSettings:
    """
    Args:
       code (string): RPA code
    """

    code: str

    def __init__(self, code):
        self.code = code


class RPAProcessor(BaseFlowProcessor):
    title = "RPA executor"
    description = "RPA executor"
    name = "rpa-code-executor"
    group = "Rpa"
    relations = [models.RelationDesc("success")]
    settings = RPAProcessorSettings

    def on_trigger(
        self, session: Session, settings: RPAProcessorSettings, *args, **kwargs
    ):
        dir_path = tempfile.mkdtemp()
        try:
            new_file, filename = tempfile.mkstemp(dir=dir_path)
            os.write(new_file, bytes(settings.code, 'utf-8'))
            os.close(new_file)
            run(filename, outputdir=dir_path)
        finally:
            shutil.rmtree(dir_path, ignore_errors=True)

        yield session.get_message(), "success"
        # exec(code, {"session": session})

