# demo-kit

This is demo-kit! Documentation is under construction.

There are no tagged versions yet. The master branch will have breaking changes.

## Usage

demo-kit is built on top of Ansible and requires that you run the `ansible-playbook`
command in the root directory. Ansible will search your current working directory
for `ansible.cfg` and will also use the `ec2.py` dynamic inventory script.

First, setup your AWS environment by creating a VPC, key pair and security groups.

```bash
$ ansible-playbook aws/create_environment.yml
```

> Note: If you update your security groups in  `demos/settings/aws_security_groups.yml` you can just re-run the create_environment playbook. The playbooks are idempotent and can be run multiple times without error.

Next, launch your EC2 instances and install Docker EE.

```bash
$ ansible-playbook demos/launch_and_install_ee_linux.yml
```

If you would like Windows instances, demo-kit can run the Windows launch and install in parallel for maximum speed. Windows takes a lot longer to boot and install software, so it's best to have demo-kit automate them in parallel to avoid having the Linux instances wait for their Windows counterparts. Open a new terminal window and run:

```bash
$ ansible-playbook demos/launch_and_install_ee_windows.yml
```

To reduce costs, you can easily stop your EC2 instances.

```bash
$ ansible-playbook aws/stop_instances.yml
```

Your demo environment won't break and can be restarted very quickly.

```bash
$ ansible-playbook aws/start_only_stopped.yml
```

If you'd like to terminate your instances and start over:

```bash
$ ansible-playbook aws/terminate_instances.yml
```

And if you want to completely wipe your environment (VPC, key pair and security groups)

```bash
$ ansible-playbook aws/destroy_environment.yml
```

## Known Issues

1. Python on macOS High Sierra (10.13)

If you are running demo-kit on macOS High Sierra (10.13) and using Windows instances, there is an [issue](http://sealiesoftware.com/blog/archive/2017/6/5/Objective-C_and_fork_in_macOS_1013.html) with Python that will cause it to crash.

To work around the issue:

```bash
$ export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```

You may want to add that to your `.bashrc` or `.zshrc`.

2. Restarting stopped EC2 instances

EC2 assigns public IP addresses differently when launching new instances vs starting previously stopped instances. When launching, public IP addresses are assigned immediately. When starting, EC2 assigns IP addresses after the instance state changes. The `aws/run_instances` playbook doesn't wait for EC2 instances to change state due to an issue in Ansible 2.5.0 where it waits not just for the state change, but for the status checks. This can take 2-5 minutes.

The playbook `aws/run_instances` will both launch new instances and start any stopped instances that are defined in the `demos/settings/aws_ec2.yml` config file. If any stopped instances are started, demo-kit won't wait for the EC2 instances to get IP addresses before continuing with the playbook and those instances won't be assigned DNS or picked up by the inventory refresh. You can either run the playbook again or choose the `aws/start_only_stopped_instances.yml` which will pause and wait for public IP addresses to be assigned before continuing.

## Installation

demo-kit requires the following items to be installed and/or configured.

1. [Python 2.7](#python-27)
2. [Ansible 2.5.0](#ansible-250)
3. [AWS SDK for Python](#aws-sdk-for-python)
4. [AWS Configuration and Credentials](#aws-configuration-and-credentials)
5. [SSH Keys](#ssh-keys)
6. [Python Library for WinRM](#python-library-for-winrm)
7. [Clone the demo-kit Repository](#clone-the-demo-kit-repository)

**Important: Ansible must be installed using `pip`. Don't use `brew`.**

#### Python 2.7

On macOS, you can use [Homebrew](https://brew.sh). To install Homebrew:

```bash
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

You can install Python with Homebrew. Python 2.7.14 has been tested.

> Note: There are issues with Python 3 and demo-kit. Initial testing found incompatibilities
with the `async_status` Ansible module.

```bash
$ brew install python@2
```

#### Ansible 2.5.0

Ansible version 2.5.0 is required. Install Ansible using `pip`.

> There are bugs in Ansible 2.5.1. You must install Ansible version 2.5.0.

```bash
$ pip install ansible==2.5.0
```

> Note: If Ansible is installed by Homebrew it will break the ec2.py dynamic inventory script.
> https://github.com/ansible/ansible/issues/30497
> https://github.com/Homebrew/brew/issues/3167

#### AWS SDK for Python

Ansible uses Boto, the AWS SDK for Python. Both `boto` and `boto3` versions of the library are required.

```bash
$ pip install boto boto3
```

#### AWS Configuration and Credentials

The AWS SDK for Python [expects](https://docs.aws.amazon.com/cli/latest/userguide/cli-config-files.html) your config and credentials files to look like:

**~/.aws/credentials**
```ini
[default]
aws_access_key_id=AKIAIOSFODNN7EXAMPLE
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

**~/.aws/config**
```ini
[default]
region=us-west-2
output=json
```

The easiest way to setup these files is to use the AWS CLI. On macOS you can install the AWS CLI with Homebrew:

```bash
$ brew install awscli
```

Then run the `configure` command.

```bash
$ aws configure
```

Test your configuration

```bash
$ aws ec2 describe-instances --output table
```

#### SSH Keys

Both private and public SSH keys are required to launch and manage Linux hosts. You can check for existing keys.

```bash
$ ls -al ~/.ssh
```

The default private key is `id_rsa` and the default public key is `id_rsa.pub`. If you need to generate keys you run `ssh-keygen`.

```bash
$ ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

For more info review the [guide](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/) on Github.

#### Python Library for WinRM

This library is only required if you want to launch and configure Windows instances.

```bash
$ pip install pywinrm
```

#### Clone the demo-kit Repository

```bash
$ git clone https://github.com/gitamiller/demo-kit
```

## Configuration

demo-kit is easy to setup and uses a couple playbooks to automate configuration. Be sure to `cd` to the demo-kit directory.

```bash
$ cd demo-kit
```

Run the questions playbook.

```bash
$ ansible-playbook setup/questions.yml
```

Review your answers and edit any advanced configuration settings in the `setup/answers.yml` file.

Run the configure playbook.

```bash
$ ansible-playbook setup/configure.yml
```

> Note: You can re-run the `setup/configure.yml` playbook after making changes to the `setup/answers.yml` file, if for example, you wanted to change your AWS region. If an existing settings file is overwriten, demo-kit will create a date-stamped backup file.

Setup is complete. Visit the [Usage](#usage) section to launch your demo environment!
