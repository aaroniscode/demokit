# demo-kit

This is demo-kit! Documentation is under construction.

There are no tagged versions yet. The master branch will have breaking changes.

## Usage

demo-kit is built on top of Ansible and requires that you run the `ansible-playbook`
command in the root directory. Ansible will search your current working directory
for ansible.cfg and will also use the ec2.py dynamic inventory script.

First, setup your AWS environment by creating a VPC, key pair and security groups.

```bash
$ ansible-playbook aws/create_environment.yml
```

> Note: If you update your security groups in  `demos/settings/aws_security_groups.yml` you can just re-run the create_environment playbook. The playbooks are idempotent and can be run multiple times without error.

Next, launch your EC2 instances and install Docker EE.

```bash
$ ansible-playbook demos/launch_and_install_ee_linux.yml
```

If you would like Windows instances, demo-kit can run the Windows launch and install in parallel for maximum speed. Windows takes a lot longer to boot and install software, so it's best to have demo-kit automate them in parallel to avoid having the Linux instances wait for their Windows counterparts.

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

If you are running demo-kit on macOS High Sierra (10.13) and using Windows instances, there is an issue(http://sealiesoftware.com/blog/archive/2017/6/5/Objective-C_and_fork_in_macOS_1013.html) with Python that will cause it to crash.

To work around the issue:

```bash
$ export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```

You may want to add that to your `.bashrc` or `.zshrc`.

The playbook `aws/run_instances` will launch new instances and start any stopped instances that are defined in the `demos/settings/aws_ec2.yml` config file. If any stopped instances are started, demo-kit won't wait for the EC2 instances to get IP addresses before continuing with the playbook and those instances won't be assigned DNS or picked up by the inventory refresh. You can either run the playbook again or choose the `aws/start_only_stopped_instances.yml` which will pause and wait for public IP addresses to be assigned before continuing.

## Installation

demo-kit requires the following items to be installed and/or configured.

1. [Python 3](#python-3)
2. [Ansible 2.5.0](#ansible-2.5.0)
3. [AWS SDK for Python](#aws-sdk-for-python-(boto3))
4. [AWS Configuration and Credentials](#aws-configuration-and-credentials)
5. [SSH Keys](#ssh-keys)
6. [Python Library for WinRM](#python-library-for-winrm)
7. [Clone the demo-kit Repository](#clone-the-demo-kit-repository)

**Important: Ansible must be installed using `pip`. Don't use `brew`.**

#### Python 3

On MacOS, you can use [Homebrew](https://brew.sh). To install Homebrew:

```bash
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
Then use Homebrew to install Python 3.

```bash
$ brew install python
```

#### Ansible 2.5.0

Ansible version 2.5.0 or greater is required. At this time version 2.5.0 has been tested.
```bash
$ pip3 install ansible==2.5.0
```
> Note: If Ansible is installed by Homebrew it will break the ec2.py dynamic inventory script.
> https://github.com/ansible/ansible/issues/30497
> https://github.com/Homebrew/brew/issues/3167

#### AWS SDK for Python (Boto3)

Homebrew installs pip from Python 3 as [`pip3`](https://docs.brew.sh/Homebrew-and-Python). If you installed python using a different method or are running on Linux you may have to use `pip`.

```bash
$ pip3 install boto3
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

The easiest way to setup these files is to use the AWS CLI. On MacOS you can install the AWS CLI with Homebrew:

```bash
$ brew install awscli
```

Then run the `configure` command.

```bash
$ awscli configure
```

Test your configuration

```bash
$ aws ec2 describe-instances --output table
```

#### SSH Keys

Both private and public SSH keys are required to launch and manage Linux hosts. You can check for existing keys: `ls -al ~/.ssh`.

The default private key is often named `id_rsa`.
The default public key is often named `id_rsa.pub`.

You can follow the guide(https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/) hosted on Github to create keys if you don't already have them or if you want to use separate, dedicated keys.

#### Python Library for WinRM

This library is only required if you want to launch and configure Windows instances.

```bash
$ pip3 install pywinrm
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

> Note: You can re-run the `setup/configure` playbook after making changes to the `setup/answers.yml` file, if for example, you wanted to change your AWS region. If an existing settings file is overwriten, demo-kit will create a date-stamped backup file.

Setup is complete. Visit the [Usage](#usage) section to launch your demo environment!
