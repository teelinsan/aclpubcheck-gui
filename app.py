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
    gr.Markdown("# 📝 ACL Pubcheck tool")
    gr.Markdown("This tool check for errors and validate your **.pdf** paper for ACL venues using the official [aclpubcheck tool](https://github.com/acl-org/aclpubcheck).")
    dropdown = gr.Dropdown(
            ["long", "short", "demo", "other"], label="Paper type", value="long"
        )
    file_output = gr.File(file_types=[".pdf"])
    button = gr.Button("Check your PDF!", variant="primary")
    out = gr.HTML()
    button.click(upload_file, [file_output, dropdown], out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default="0.0.0.0", type=str)
    parser.add_argument('--port', default=7860, type=int)
    args = parser.parse_args()

    demo.launch(server_name=args.host, server_port=args.port)
