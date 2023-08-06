import os.path
import argparse

def generate_out_file(extent: str, name: str="output"):
    fname, ext = os.path.splitext(name)
    if ext != extent:
        fname += ext
        ext = extent

    text = "{}{}".format(fname, ext)
    if os.path.exists(text):
        base = "{}({}){}"
        counter = 1
        text = base.format(fname, counter, ext)
        while os.path.exists(text):
            counter += 1
            text = base.format(fname, counter, ext)
    return text

def generate_out_dir_name(name: str):
    text = name
    if os.path.exists(name):
        base = "{}({})"
        counter = 1 
        text = base.format(name, counter)
        while os.path.exists(text):
            counter +=1
            text = base.format(name, counter)
    return text

def get_args(desc: str) -> tuple[str, str]:
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--input",required=True,type=str, help="Archivo de entrada, formato COCO")
    parser.add_argument("--output", type=str, help="""Archivo de salida de
     clases en texto plano""")
    
    args = parser.parse_args()
    return (args.input, args.output)

