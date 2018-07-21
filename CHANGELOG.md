# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.5.1] - 2018-07-21
### Fixed
- Fixed missing ec2.py dynamic inventory file

## [v0.5.0] - 2018-07-20
### Added
- demokit is now a container! No software to install besides the Docker engine
- demokit uses a single bind mounted directory for local settings -- you can use a cloud service like iCloud Drive or Dropbox to share configuration across computers
- demokit now has easy to use, documented command line actions
- Setup is automatic and simple. Only needs AWS access key, region and domain to start
- Setup tests AWS credentials and access to diagnose any initial setup issues
- Setup creates SSH keys automatically and stores in the local bind mounted directory
- Support for multiple demos running at the same time, with commands to manage each separately
- K8s demo added, running vanilla upstream k8s on Docker CE
- Ubuntu 1804 LTS added as supported OS, used by k8s demo
- Status command added to view running and stopped EC2 instances
- Command line option to limit actions to EC2 instances with a specific tag
- Command line option to SSH into EC2 instances, dynamically creating SSH config file
- Let's Encrypt certificates now support a list of SANs

### Changed
- UCP EC2 instances default to t2.large to avoid warning messages in UCP GUI
- Ansible version upgraded to 2.6.0
- Starting stopped EC2 instances now runs asyncronously, running much faster
- Let's Encrypt certificate chain includes the well trusted IdenTrust|DST Root Certificate

## [v0.4.0] - 2018-05-18
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

[Unreleased]: https://github.com/gitamiller/demokit/compare/master...devel
[v0.5.1]: https://github.com/gitamiller/demokit/compare/v0.5.0...v0.5.1
[v0.5.0]: https://github.com/gitamiller/demokit/compare/v0.4.0...v0.5.0
[v0.4.0]: https://github.com/gitamiller/demokit/compare/v0.3.0...v0.4.0
[v0.3.0]: https://github.com/gitamiller/demokit/compare/v0.2.0...v0.3.0
