#    Pandoc Flow - Augments Pandoc with advanced pre-processing, automates routine
#    Copyright (C) 2021 Dmitry Berezovsky
#    The MIT License (MIT)
#
#    Permission is hereby granted, free of charge, to any person obtaining
#    a copy of this software and associated documentation files
#    (the "Software"), to deal in the Software without restriction,
#    including without limitation the rights to use, copy, modify, merge,
#    publish, distribute, sublicense, and/or sell copies of the Software,
#    and to permit persons to whom the Software is furnished to do so,
#    subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be
#    included in all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#    CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
from copy import copy
from typing import Optional

import pandoc_flow.const
from strome import const
from strome.error import ProcessorLoadingError
from pandoc_flow.pipeline import PandocFlowRuntime
from strome.pipeline import PipelineElement, ExternalExecutableMixin
from strome.utils import dict_to_yaml_file

__all__ = ("PandocProcessor",)


class PandocProcessor(PipelineElement, ExternalExecutableMixin):
    NAME = "pandoc"

    def __init__(self) -> None:
        super().__init__()
        self.pandoc_version: Optional[str] = None
        self.pandoc_executable = "pandoc"

    def load(self):
        self.logger.debug("Validating pandoc installation")
        if not self.is_successful_exit_code(self.pandoc_executable, "--version"):
            raise ProcessorLoadingError(
                "Pandoc executable doesn't exist.",
                self,
                recommendation="Check if you have pandoc installed and available in PATH",
            )

    def setup(self, flow_runtime: PandocFlowRuntime, params: dict):
        self.logger.info("Configuring pandoc")
        pandoc_version_result = self.run_executable(self.pandoc_executable, "--version", hide_output=True)
        lines = pandoc_version_result.stdout.split("\n")
        if lines[0].startswith("pandoc"):
            self.pandoc_version = lines[0].replace("pandoc", "").strip()
            self.logger.info("\t\tDetected pandoc version: " + self.pandoc_version)  # type: ignore

    def __generate_pandoc_yaml_conf(self, flow_runtime: PandocFlowRuntime):
        # Generate and write pandoc yaml
        flow_runtime.pandoc_config_generated_path = os.path.join(
            flow_runtime.temp_dir, os.path.basename(flow_runtime.config_path)
        )
        generated_pandoc_conf = copy(flow_runtime.config)
        # Ensure we remove all config options not supported by pandoc
        del generated_pandoc_conf[pandoc_flow.const.CONF_PANDOC_FLOW]
        del generated_pandoc_conf[const.CONF_DEFAULTS]
        if const.CONF_OUTPUT in generated_pandoc_conf:
            del generated_pandoc_conf[const.CONF_OUTPUT]
        # Extend input files with generated ones
        if const.CONF_INPUT_FILES in generated_pandoc_conf:
            generated_pandoc_conf[const.CONF_INPUT_FILES] = (
                flow_runtime.context[const.RUNTIME_INPUT_FILES] + generated_pandoc_conf[const.CONF_INPUT_FILES]
            )
        # Extend resource path
        resource_path = ["."]
        if const.CONF_RESOURCE_PATH in generated_pandoc_conf:
            if isinstance(generated_pandoc_conf[const.CONF_RESOURCE_PATH], list):
                resource_path = generated_pandoc_conf[const.CONF_RESOURCE_PATH]
            elif isinstance(generated_pandoc_conf[const.CONF_RESOURCE_PATH], str):
                resource_path = generated_pandoc_conf[const.CONF_RESOURCE_PATH].split(":")
            else:
                raise ValueError("resource-path must be either list or colon delimited string")
            resource_path += flow_runtime.context[const.RUNTIME_RESOURCE_PATH]
        generated_pandoc_conf[const.CONF_RESOURCE_PATH] = resource_path
        # Write down generated pandoc conf
        dict_to_yaml_file(generated_pandoc_conf, flow_runtime.pandoc_config_generated_path)

    def run(self, flow_runtime: PandocFlowRuntime):
        self.__generate_pandoc_yaml_conf(flow_runtime)
        output_file_path = flow_runtime.config.get("output")
        pandoc_args = [
            self.pandoc_executable,
            "-o",
            output_file_path,
            "--defaults",
            flow_runtime.pandoc_config_generated_path,
        ]
        for meta_var in flow_runtime.context[pandoc_flow.const.RUNTIME_PANDOC_META]:
            pandoc_args += ["-M", meta_var]
        for var in flow_runtime.context[pandoc_flow.const.RUNTIME_PANDOC_VARS]:
            pandoc_args += ["-V", var]
        self.logger.debug("Will be running pandoc with the following params: ")
        self.logger.debug(str(pandoc_args))
        self.run_executable(*pandoc_args)
