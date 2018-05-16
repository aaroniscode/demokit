# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Automatically create and renew certificates with Let's Encrypt using DNS-01 challenge
- Install UCP with certificate
- Install DTR with certificate

### Changed
- docker_py is pinned to a version (3.3.0) to avoid breaking changes
- aws/destroy_environment.yml terminates instances in parallel for increased speed

## [v0.3.0] - 2018-04-30
### Added
- Populate DTR repositories (create repos, push tagged images)
- Add a couple demo applications (compose files)
- Setup asks for Docker EE license file and copies to demos/licenses
- Setup asks for UCP admin password

### Changed
- Moved a few settings around for better usability

## v0.2.0 - 2018-04-25
### Added
- First tagged release
- Documentation
- Automated setup
- Populate UCP organization, teams, users and user/team assignments
- Populate UCP collections
- Customize volumes for ec2 instances

[Unreleased]: https://github.com/gitamiller/demo-kit/compare/master...devel
[v0.3.0]: https://github.com/gitamiller/demo-kit/compare/v0.2.0...v0.3.0
