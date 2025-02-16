<h1 align="center">PapersChat</h1>

<h2 align="center">Chatting With Papers Made Easy</h2>

<h3 align="center">If you find PapersChat useful, please consider to support us through donation:</h3>
<div align="center">
    <a href="https://github.com/sponsors/AstraBert"><img src="https://img.shields.io/badge/sponsor-30363D?style=for-the-badge&logo=GitHub-Sponsors&logoColor=#EA4AAA" alt="GitHub Sponsors Badge"></a>
</div>

**PapersChat** is an agentic AI application that allows you to chat with your papers and gather also information from papers on ArXiv and on PubMed. It is powered by [LlamaIndex](https://www.llamaindex.ai/), [Qdrant](https://qdrant.tech) and [Mistral AI](https://mistral.ai/en).

### Install and launch it

The installation of the application is a unique process, you simply have to clone the GitHub repository:

```bash
git clone https://github.com/AstraBert/PapersChat.git
cd PapersChat/
```

To launch the app, you can follow two paths:

**1. Docker (recommended)**

> _Required: [Docker](https://docs.docker.com/desktop/) and [docker compose](https://docs.docker.com/compose/)_

- Add the `mistral_api_key`, `phoenix_api_key` and `llamacloud_api_key`  variables in the [`.env.example`](./docker/.env.example) file and modify the name of the file to `.env`. Get these keys:
    + [On Mistral AI](https://console.mistral.ai/api-keys/)
    + [On LlamaCloud](https://cloud.llamaindex.ai/)
    + [On Phoenix/Arize](https://llamatrace.com/projects)

```bash
# modify your access token, e.g. hf_token="hf_abcdefg1234567"
mv .env.example .env
```

- Launch the docker application:

```bash
# If you are on Linux/macOS
bash start_services.sh
# If you are on Windows
.\start_services.ps1
```

You will see the application running on http://localhost:7860 and you will be able to use it. Depending on your connection and on your hardware, the set up might take some time (up to 30 mins to set up) - but this is only for the first time your run it!

**2. Source code**

> _Required: [Docker](https://docs.docker.com/desktop/), [docker compose](https://docs.docker.com/compose/) and [conda](https://anaconda.org/anaconda/conda)_

- Add the `mistral_api_key`, `phoenix_api_key` and `llamacloud_api_key`  variables in the [`.env.example`](./docker/.env.example) file and modify the name of the file to `.env`. Get these keys:
    + [On Mistral AI](https://console.mistral.ai/api-keys/)
    + [On LlamaCloud](https://cloud.llamaindex.ai/)
    + [On Phoenix/Arize](https://llamatrace.com/projects)

```bash
mv .env.example .env
# modify the variables, e.g.:
# llamacloud_api_key="llx-000-abc"
# mistral_api_key="01234abc"
# phoenix_api_key="56789def"
```

- Set up PapersChat using the dedicated script:

```bash
# For MacOs/Linux users
bash local_setup.sh
# For Windows users
.\local_setup.ps1
```

- Or you can do it manually, if you prefer:

```bash
docker compose up db -d

conda env create -f environment.yml

conda activate papers-chat
python3 scripts/app.py
conda deactivate
```

## Contributing

Contributions are always welcome! Follow the contributions guidelines reported [here](CONTRIBUTING.md).

## License and rights of usage

The software is provided under MIT [license](./LICENSE).

### Full documentation will come soon!👷‍♀️

