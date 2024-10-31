# Developer Guide

This tutorial will teach you step by step how to set up a development environment.

## Prerequisites

At a minimum you will need:

* A Linux distribution
* Node 22+ installed locally
* Python 3.12+ installed locally

## Workflow

Modify necessary environment variables:

* Modify the `contrib/dit/export.sh` file
* Modify the `contrib/init/init-clusters.json` file


Initialize Python related dependencies and start API services:

```
python3 -m venv /usr/local/envs/manager
source /usr/local/envs/manager/bin/activate
pip install -r rootfs/requirements.txt
python manage.py migrate
python manage.py init_clusters --path contrib/init/init-clusters.json
python manage.py runserver
```

Initialize nodejs related dependencies and start web:

```
cd rootfs/web; yarn install; yarn run dev
```

Now, enjoy the development!!!