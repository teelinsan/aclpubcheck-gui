import gradio as gr
import re
import os
import subprocess
import argparse


def remove_color_codes(text):
    color_pattern = re.compile(r"\x1b\[\d+m")
    clean_text = re.sub(color_pattern, "", text)
    return clean_text


def to_html(document):
    lines = document.split("\n")
    formatted_lines = []

    for line in lines:
        if line.startswith("Error"):
            formatted_line = f'<span style="color: red;">{line}</span>'
        elif line.startswith("Warning"):
            formatted_line = f'<span style="color: yellow;">{line}</span>'
        elif line.startswith("Parsing Error:"):
            formatted_line = f'<span style="color: yellow;">{line}</span>'
        elif line == "All Clear!":
            formatted_line = f'<span style="color: green;">{line}</span>'
        else:
            formatted_line = line

        formatted_lines.append(formatted_line)

    formatted_document = "<br>".join(formatted_lines)
    return formatted_document


def add_images(file_name):
    html = '<div align="center">'
    for file in os.listdir("."):
        if file.startswith(f"errors-{file_name}") and file.endswith(".png"):
            html += f'<img src="file/{file}">'
    html += "</div>"
    return html


def clear_cached_images(file_name):
    for file in os.listdir("."):
        if file.startswith(f"errors-{file_name}") and file.endswith(".png"):
            os.remove(file)


def get_filename(file):
    file_name = os.path.basename(file).split(".")[0]
    if "_" in file_name:
        # apparently aclpubcheck doesn't like underscores in filenames
        file_name = file_name.split("_")[0]
    return file_name


def upload_file(file, paper_type):
    file_name_cmd = file.name.replace(" ", "\ ")
    file_name = get_filename(file.name)
    clear_cached_images(file_name)
    command = f"aclpubcheck --paper_type {paper_type} {file_name_cmd}"
    out = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, text=True, stderr=subprocess.STDOUT
    )
    return to_html(remove_color_codes(out.stdout)) + add_images(file_name)


with gr.Blocks() as demo:
    header = """
        <div align="center">
        <img src="https://upload.wikimedia.org/wikipedia/en/thumb/7/72/Association_for_Computational_Linguistics_logo.svg/2880px-Association_for_Computational_Linguistics_logo.svg.png" alt="acl-logo" width=100px/>
        <h1>ACL Pubcheck Tool</h1>
        </div>
    """
    gr.HTML(header)
    gr.Markdown(
        "Drop or upload your paper here to have it checked for [*ACL conferences](https://www.aclweb.org/) guidelines."
    )
    dropdown = gr.Dropdown(
        ["long", "short", "demo", "other"], label="Paper type", value="long"
    )
    file_output = gr.File(file_types=[".pdf"])
    button = gr.Button("Check your PDF!", variant="primary")
    out = gr.HTML()
    gr.Markdown(
        "This graphical interface is using the official [aclpubcheck tool](https://github.com/acl-org/aclpubcheck). Check the [Github repo for more information.](https://github.com/teelinsan/aclpubcheck-gui)"
    )
    gr.Markdown(
        "No data is collected. If you prefer you can also duplicate this Space to run it privately. [![Duplicate Space](https://img.shields.io/badge/-Duplicate%20Space-blue?labelColor=white&style=flat&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAP5JREFUOE+lk7FqAkEURY+ltunEgFXS2sZGIbXfEPdLlnxJyDdYB62sbbUKpLbVNhyYFzbrrA74YJlh9r079973psed0cvUD4A+4HoCjsA85X0Dfn/RBLBgBDxnQPfAEJgBY+A9gALA4tcbamSzS4xq4FOQAJgCDwV2CPKV8tZAJcAjMMkUe1vX+U+SMhfAJEHasQIWmXNN3abzDwHUrgcRGmYcgKe0bxrblHEB4E/pndMazNpSZGcsZdBlYJcEL9Afo75molJyM2FxmPgmgPqlWNLGfwZGG6UiyEvLzHYDmoPkDDiNm9JR9uboiONcBXrpY1qmgs21x1QwyZcpvxt9NS09PlsPAAAAAElFTkSuQmCC&logoWidth=14)](https://huggingface.co/spaces/teelinsan/aclpubcheck?duplicate=true)"
    )

    button.click(upload_file, [file_output, dropdown], out)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0", type=str)
    parser.add_argument("--port", default=7860, type=int)
    args = parser.parse_args()

    demo.launch(server_name=args.host, server_port=args.port)
