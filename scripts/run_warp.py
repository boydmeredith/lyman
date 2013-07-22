#! /usr/bin/env python
import sys
import shutil
from lyman import frontend as fe
from lyman.tools.commandline import parser
from lyman.workflows import anatwarp


def main(arglist):

    # Process cmdline args
    args = parser.parse_args(arglist)
    plugin, plugin_args = fe.determine_engine(args)

    # Load up the lyman info
    subject_list = fe.determine_subjects(args.subjects)
    project = fe.gather_project_info()

    # Create the workflow object
    normalize = anatwarp.create_anatwarp_workflow(
                    project["data_dir"], subject_list)
    normalize.base_dir = project["working_dir"]
    normalize.config["execution"]["crashdump_dir"] = "/tmp"

    # Execute the workflow
    normalize.run(plugin=plugin, plugin_args=plugin_args)

    # Clean up
    if project["rm_working_dir"]:
        shutil.rmtree(normalize.base_dir)

if __name__ == "__main__":
   main(sys.argv[1:])
