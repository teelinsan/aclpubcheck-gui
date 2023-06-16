import gradio as gr
import re
import subprocess
import argparse

def remove_color_codes(text):
    color_pattern = re.compile(r'\x1b\[\d+m')
    clean_text = re.sub(color_pattern, '', text)
    return clean_text


def to_html(document):
    lines = document.split('\n')
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

    formatted_document = '<br>'.join(formatted_lines)
    return formatted_document


def upload_file(file, paper_type):
    command = f"python3 aclpubcheck-main/aclpubcheck/formatchecker.py --paper_type {paper_type} {file.name}"
    out = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True, stderr=subprocess.STDOUT)
    return to_html(remove_color_codes(out.stdout))


with gr.Blocks() as demo:
    header = """
        <div align="center">
        <img src="https://upload.wikimedia.org/wikipedia/en/thumb/7/72/Association_for_Computational_Linguistics_logo.svg/2880px-Association_for_Computational_Linguistics_logo.svg.png" alt="acl-logo" width=100px/>
        <h1>ACL Pubcheck Tool</h1>
        </div>
    """
    gr.HTML(header)
    gr.Markdown("Drop or upload your paper here to have it checked for [ACL conferences](https://www.aclweb.org/) guidelines.")
    dropdown = gr.Dropdown(
            ["long", "short", "demo", "other"], label="Paper type", value="long"
        )
    file_output = gr.File(file_types=[".pdf"])
    button = gr.Button("Check your PDF!", variant="primary")
    out = gr.HTML()
    gr.Markdown(
        "This graphical interface is using the official [aclpubcheck tool](https://github.com/acl-org/aclpubcheck). Check the [repo for more information.](https://github.com/teelinsan/aclpubcheck-gui)")
    button.click(upload_file, [file_output, dropdown], out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default="0.0.0.0", type=str)
    parser.add_argument('--port', default=7860, type=int)
    args = parser.parse_args()

    demo.launch(server_name=args.host, server_port=args.port)
