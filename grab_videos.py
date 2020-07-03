# Hold off on prophet image generation, probably not useful since I buy small caps

import sys 
import argparse as ap
import pathlib
import glob
import shutil
from jinja2 import Template
from datetime import date, datetime

def main(args):
    end_date = str(date.today())
    gh_pages_name = 'gh-pages'
    for report_cfg_file in glob.glob("lib/cfg/*.yml"):
        # report_name = report_cfg["name"]
        pass 
        options = dict(Version="1.0.0")
        report_name = 'test'
        output_folder = f"{args.output}/{report_name}"
        pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)

        
        with open(args.template) as file_:
            template = Template(file_.read())
        renderer_template = template.render(**options)
        with open(f"{output_folder}/index.html", "w", errors='ignore') as f:
            f.write(renderer_template)

        # Attempt to move the folder
        # Make in gh pages folder even if exists
        gh_report_folder = f"{args.output}/{gh_pages_name}/{report_name}/{end_date}"
        pathlib.Path(gh_report_folder).mkdir(parents=True, exist_ok=True)
        # Any files in the output folder, if I need nested files in folders
        # use something else
        for report_file in glob.glob(f"{output_folder}/*"):
            try:
                # Move css files
                shutil.move(report_file, gh_report_folder)
            except shutil.Error as e:
                print(e)
        # Could make into another function
    
if __name__ == "__main__":
    assert sys.version_info >= (3, 6)
    startTime = datetime.now()
    parser = ap.ArgumentParser()
    parser.add_argument("-o",
                        "--output",
                        help="Output folder",
                        default="report")
    parser.add_argument("-t", 
                        "--template", 
                        help="Template file", 
                        default="lib/ytube.jinja2") 
    args = parser.parse_args()
    main(args)
    print("Script Complete")
    print(datetime.now() - startTime)