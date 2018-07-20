![GitHub release](https://img.shields.io/github/release/gitamiller/demokit.svg?style=plastic)

# demokit

demokit quickly and easily creates fully configured demo environments in the cloud (AWS today). It will create a VPC, launch instances, configure security groups, install software, configure settings and populate with demo data. You can also easily shut down instances and restart them to minimize costs.

demokit is built on Ansible and the current demo focus is Docker Enterprise Edition.

## Requirements

demokit is a container-based tool and doesn't require installation. You will need:

1. Docker
2. AWS credentials (IAM user with access key and permissions for EC2, VPC and Route53)
3. Hosted Zone in Route53

## Setup

```bash
docker run demokit/demokit
```

demokit will ask for:

1. AWS access key ID
2. AWS secret access key
3. AWS region
4. Domain name (for your Hosted Zone)

## Usage

Before running any demos, you will need to configure your AWS environment:

```bash
demokit aws config
```

The command above will create a AWS keypair, VPC and Let's Encrypt certificates.

To launch a Docker EE demo environment:

```bash
demokit ee install
```

To remove the demo instances:

```bash
demokit ee terminate
```

## Customize

In your demokit settings directory, ~/demokit/settings, you can edit the YAML config files to customize the demo to your needs.