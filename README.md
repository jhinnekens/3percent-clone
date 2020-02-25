# 3Percent

DESCRIPTION

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

This app works with python 3.6 and virtual env ([see](http://www.dropwizard.io/1.0.2/docs/) how to install)

### Installing

#### Clone repository

```bash
git clone https://github.com/EtienneSeck/3percent.git
```

#### Build from sources

##### Set up virtual env

```bash
cd 3percent
python3 -m venv 3pvenv
```

##### Activate virtual env

###### For linux

```bash
source 3pvenv/bin/activate
```

###### For Windows

```cmd
3pvenv\Script\activate.bat
```

##### Upgrade pip and Install requirements.txt

```cmd
pip install -U pip
pip install -r requirements.txt
```

#### Build With Docker

##### Build Docker Image

```bash
docker-compose build
```

## Running Test

### Local build

```bash
cd src
python run.py
```

### Docker build

```bash
docker-compose up -d
```

#### See logs

```bash
docker-compose logs -f
```

## Deployment

## Built With

## Contributing

## Versioning

## Authors

* **Etienne Seckinger** - *Associate Data Intelligence* -
* **Julien Hinnekens** - *Senior Associate Data Intelligence* -

## License

## Acknowledgments
