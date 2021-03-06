[![Tecktron](https://circleci.com/gh/Tecktron/timeservice.svg?style=shield)](https://circleci.com/gh/Tecktron/timeservice) &nbsp; [![codecov](https://codecov.io/gh/Tecktron/timeservice/branch/main/graph/badge.svg?token=HRIVES4L34)](https://codecov.io/gh/Tecktron/timeservice)

# TimeService

TimeService is a simple service that gives time in UTC, or a requested time zone,
represented as an ISO-8601 string. This service also includes the list of available
time zones optionally filtered by the UTC offset or an area.

## Requirements
 - Python 3.8+ or Docker

## Installation
There are 2 ways to use this:
1. Use the Docker image (easiest)
2. Run this as a local Python service

### Docker Service
The latest docker image is available at my docker hub.
[You can find it here](https://hub.docker.com/r/tecktron/timeservice)

#### Docker Example
```
docker pull tecktron/timeservice:latest
docker run -d -p 8182:80 --name timeservice tecktron/timeservice:latest
```
This will bring up the service running locally on port 8182 (I.E., `http://localhost:8182/`).

To stop the service, run `docker stop timeservice`.

### Local server
You can of course just run this locally.

1. Clone this repo.
2. Create a local Python virtual environment and activate it (e.g., `python -m venv ./.venv && source ./.venv/bin/activate`)
3. Install the system packages for [bjoern](https://github.com/jonashaag/bjoern) (on ubuntu/debian this is `sudo apt -y install gcc libev-dev`)
4. Install the requirements using pip (e.g., `pip install -r requirements.txt`)
5. Run the service: `python timeservice.py`.
6. Open your browser to `http://localhost:8182/` to see the time.
7. You can control the host and port with the environment variables `TS_HOST` and `TS_PORT`, which default to `127.0.0.1` and `8182` respectively.

## How to Use

### Get the time
To get the time in UTC (the default time zone) just make a request to the `/` endpoint (I.E., `http://localhost:8182/`)

To get the time in a different time zone just make a request to the name of the time zone. For example, to get the time of New York, request the `/America/New_York` time zone. (I.E., `http://localhost:8182/America/New_York`)

### Get time zones
To get the list of supported time zones, make a request to the `/timezones` endpoint (I.E., `http://localhost:8182/timezones`).

The output type can be controlled using the _HTTP Accept_ header. Supported types are:
- JSON: *application/json*
- HTML: *text/html*
- CSV with header: *text/csv*
- Text (default): *text/plain*


### Filtering time zones
You can filter time zones in two ways:

#### UTC offset
This will return all the time zones for the requested offset.

To filter time zones by their UTC offset, simply add the offset for the time zones you want, for example, to get UTC +0500 you can use `/timezones/+0500` (I.E., `http://localhost:8182/timezones/+0500`). Values of `+05`, `05`, `+500`, `500`, `+5` and `5` are also valid and yield the same results.

#### Area
This will return all the time zones of the requested area.

Some time zones include an area and a location. For example, in the time zone named "America/New_York", "America" is the area and "New York" is the location. If you want to know all the time zones for an area, for example Antarctica, you can make a request to `/timezones/antarctica` (I.E., `http://localhost:8182/timezones/antarctica`).

### Display Help
To display the above help at any time, you can use `/help` endpoint (I.E., `http://localhost:8182/help`).

## Help and support
If you need help or find a bug or would like to ask for a feature (you could build it, see
contributing below). Please first search to see if the issue exists on the github page. If not,
please open a new ticket and explain in as much detail as possible how to recreate the issue or
what feature you'd like to see.

## Contributing and development
This is an opensource project, contributions are welcome. Please follow the guidelines to
contribute to this project.

### Setup
- Use `pip` to install the additional `dev.requirements.txt`.

### Coding standards
Before submitting any code please be sure you have done the following:
- Run coding stands tools, these are isort, black and flake8. They should all pass.
- Run tox and check all tests have passed and that your code coverage is 98% or above.

### Testing
Every bit of code you submit must be fully tested.
All testing is done using pytest, please follow pytest style testing (not unittest).
You can simply use tox to run the tests: `tox -e py39`. This supports environments
`py38` - `py39`.
