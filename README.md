# drycc manager
[![Build Status](https://woodpecker.drycc.cc/api/badges/drycc/manager/status.svg)](https://woodpecker.drycc.cc/drycc/manager)
[![codecov](https://codecov.io/github/drycc/manager/branch/main/graph/badge.svg?token=YNjGaRzZz8)](https://codecov.io/github/drycc/manager)

The Workflow Manager is responsible for interfacing with Drycc Workflow data. It integrates the passport component and can manage one or more drycc clusters.

## Development

The Drycc project welcomes contributions from all developers. The high-level process for development matches many other open source projects. See below for an outline.

* Fork this repository
* Make your changes
* [Submit a pull request][prs] (PR) to this repository with your changes, and unit tests whenever possible.
  * If your PR fixes any [issues][issues], make sure you write Fixes #1234 in your PR description (where #1234 is the number of the issue you're closing)
* Drycc project maintainers will review your code.
* After two maintainers approve it, they will merge your PR.

## Testing
The Drycc project requires that as much code as possible is unit tested, but the core contributors also recognize that some code must be tested at a higher level (functional or integration tests, for example).