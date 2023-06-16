# 📝 ACL Pubcheck Graphical User Interface

ACL Pubcheck GUI is a minimal graphical user interface for the [ACL Pubcheck tool](https://github.com/acl-org/aclpubcheck) made with [gradio](https://github.com/gradio-app/gradio).
The tool allows you to check the compliance of your paper with the [ACL conferences](https://www.aclweb.org/) guidelines by simply drag and drop your pdf file on the interface.

## Usage
The tool is available online on [Hugging Face Spaces](https://aclpubcheck.herokuapp.com/). You can access it by clicking on the button or image below.
Since it is running on a free instance, it might take a while to start if it was inactive for more than 48h.
Alternatively, you can run it locally by following the instructions in the section `Local Deploy`.

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/teelinsan/aclpubcheck) [![Open in Spaces](https://huggingface.co/datasets/huggingface/badges/raw/main/open-in-hf-spaces-md-dark.svg)](https://huggingface.co/spaces/teelinsan/aclpubcheck)
[![gradio.png](assets%2Fscreen.png)](https://huggingface.co/spaces/teelinsan/aclpubcheck)

## Local Deploy
In order to deploy the application locally, you need to have [Docker](https://www.docker.com/) installed on your machine.
You can then build the image and run the container with the following commands:

```bash
docker build -t aclpubcheck-gui .
docker run -p 7860:7860 aclpubcheck-gui
```
The application will be available at [http://localhost:7860](http://localhost:7860). You can customize the port number by changing the last line of the Dockerfile and run again the commands above.