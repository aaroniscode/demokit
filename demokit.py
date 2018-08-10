import argparse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from subprocess import call
import os
import sys
import yaml
from plugins.filters.custom import base64decode_filter

# TODO: function to load /bind/demokit.yml and catch exception if not valid YAML

def ascii_art():
    print("     _                      _    _ _   ")
    print("  __| | ___ _ __ ___   ___ | | _(_) |_ ")
    print(" / _` |/ _ \ '_ ` _ \ / _ \| |/ / | __|")
    print("| (_| |  __/ | | | | | (_) |   <| | |_ ")
    print(" \__,_|\___|_| |_| |_|\___/|_|\_\_|\__|\n")

def check_ee():
    vars = yaml.load(file('/bind/demokit.yml', 'r'))

    ee_req_vars = ['docker_ee_url', 'ucp_password']

    if not all(key in vars and vars[key] is not None for key in ee_req_vars):
        setup_ee()

def check_eetest():
    vars = yaml.load(file('/bind/demokit.yml', 'r'))

    eetest_req_vars = ['docker_hub_username', 'docker_hub_email', 'docker_hub_password',
        'eetest_engine_channel', 'eetest_ucp_version', 'eetest_dtr_version']

    if not all(key in vars and vars[key] is not None for key in eetest_req_vars):
        setup_eetest()

def check_windows():
    vars = yaml.load(file('/bind/demokit.yml', 'r'))

    windows_req_vars = ['windows_password']

    if not all(key in vars and vars[key] is not None for key in windows_req_vars):
        setup_windows()

def create_ec2ini_allyml():
    stream = file('/bind/demokit.yml', 'r')
    vars = yaml.load(stream)

    env = Environment(
        loader = FileSystemLoader('/demokit/setup/templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    env.filters['base64decode'] = base64decode_filter

    template = env.get_template('ec2.ini.j2')

    with open('/demokit/inventory/ec2.ini', 'wb') as fh:
        fh.write(template.render(vars))

    template = env.get_template('all.yml.j2')

    with open('/demokit/inventory/group_vars/all.yml', 'wb') as fh:
        fh.write(template.render(vars))

    template = env.get_template('aws.config.j2')
    with open('/root/.aws/config', 'wb') as fh:
        fh.write(template.render(vars))

    template = env.get_template('aws.credentials.j2')
    with open('/root/.aws/credentials', 'wb') as fh:
        fh.write(template.render(vars))

def create_ssh_config():
    vars = {}
    for filename in ['/bind/demokit.yml', '/bind/settings/aws_ec2.yml']:
        with open(filename) as f:
            vars.update(yaml.load(f))

    env = Environment(
        loader = FileSystemLoader('/demokit/setup/templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('ssh.config.j2')

    with open('/root/.ssh/config', 'w') as fh:
        fh.write(template.render(vars))

def debug(args):
    create_ec2ini_allyml()

    if os.path.exists('/bind/settings/aws_ec2.yml'):
        create_ssh_config()

    call(['sh'])

def ee_install(args):
    check_ee()
    run_ansible(args)

def ee_windows(args):
    check_ee()
    check_windows()
    run_ansible(args)

def eetest_install(args):
    check_ee()
    check_eetest()
    run_ansible(args)

def eetest_windows(args):
    check_ee()
    check_eetest()
    check_windows()
    run_ansible(args)

def parser():
    # Default to printing help info on error
    class MyParser(argparse.ArgumentParser):
        def error(self, message):
            sys.stderr.write('error: %s\n' % message)
            self.print_help()
            sys.exit(2)

    parser = MyParser(
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50, width=200),
        prog='demokit'
    )
    subparser = parser.add_subparsers(help='', metavar='<command>')

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('-l', dest='ec2tag', help='limit to instances with the specified tag')

    aws_parser = subparser.add_parser('aws', help='commands to manage AWS resources')
    debug_parser = subparser.add_parser('debug').set_defaults(func=debug)
    ee_parser = subparser.add_parser('ee', help='commands to demo Docker EE 2.0', parents=[parent_parser])
    eetest_parser = subparser.add_parser('eetest', help='commands to demo Docker EE test versions', parents=[parent_parser])
    k8s_parser = subparser.add_parser('k8s', help='commands to demo Kubernetes on Docker CE', parents=[parent_parser])
    subparser.add_parser('settings', help='reset demo settings, backup any changed files').set_defaults(func=settings)
    subparser.add_parser('setup', help='update demokit configuration').set_defaults(func=setup)
    ssh_parser = subparser.add_parser('ssh', help='ssh into EC2 instance')
    ssh_parser.add_argument('hostname', help='EC2 instance short name (without domain)')
    ssh_parser.set_defaults(func=ssh)

    aws_subparser = aws_parser.add_subparsers(
        description=None,
        help='',
        metavar='<subcommand>',
        title='Commands'
    )

    aws_config_parser = aws_subparser.add_parser(
        'config',
        help='configure AWS VPC, security groups and letsencrypt certs'
    )
    aws_config_parser.set_defaults(func=run_ansible, play='aws/configure')

    aws_destroy_parser = aws_subparser.add_parser(
        'destroy',
        help='terminate EC2 instances and destroy all AWS resources'
    )
    aws_destroy_parser.set_defaults(func=run_ansible, play='aws/destroy')

    aws_status_parser = aws_subparser.add_parser(
        'status',
        help='display any running or stopped EC2 instances'
    )
    aws_status_parser.set_defaults(func=run_ansible, play='aws/status')

    ee_subparser = ee_parser.add_subparsers(
        description=None,
        help='',
        metavar='<subcommand>',
        title='Commands'
    )

    ee_install_parser = ee_subparser.add_parser(
        'install',
        help='install Docker EE UCP, DTR and Linux nodes'
    )
    ee_install_parser.set_defaults(func=ee_install, play='ee/install')

    ee_start_parser = ee_subparser.add_parser(
        'start',
        help='start any stopped Docker EE demo instances'
    )
    ee_start_parser.set_defaults(func=run_ansible, play='ee/start')

    ee_status_parser = ee_subparser.add_parser(
        'status',
        help='display running or stopped Docker EE demo instances'
    )
    ee_status_parser.set_defaults(func=run_ansible, play='ee/status')

    ee_stop_parser = ee_subparser.add_parser(
        'stop',
        help='shut down running Docker EE demo instances'
    )
    ee_stop_parser.set_defaults(func=run_ansible, play='ee/stop')

    ee_terminate_parser = ee_subparser.add_parser(
        'terminate',
        help='terminate only Docker EE demo instances'
    )
    ee_terminate_parser.set_defaults(func=run_ansible, play='ee/terminate')

    ee_windows_parser = ee_subparser.add_parser(
        'windows',
        help='install Docker EE Windows nodes'
    )
    ee_windows_parser.set_defaults(func=ee_windows, play='ee/windows')

    eetest_subparser = eetest_parser.add_subparsers(
        description=None,
        help='',
        metavar='<subcommand>',
        title='Commands'
    )

    eetest_install_parser = eetest_subparser.add_parser(
        'install',
        help='install Docker EE UCP, DTR test versions'
    )
    eetest_install_parser.set_defaults(func=eetest_install, play='eetest/install')

    eetest_start_parser = eetest_subparser.add_parser(
        'start',
        help='start any stopped Docker EE test instances'
    )
    eetest_start_parser.set_defaults(func=run_ansible, play='eetest/start')

    eetest_status_parser = eetest_subparser.add_parser(
        'status',
        help='display running or stopped Docker EE test instances'
    )
    eetest_status_parser.set_defaults(func=run_ansible, play='eetest/status')

    eetest_stop_parser = eetest_subparser.add_parser(
        'stop',
        help='shut down running Docker EE test instances'
    )
    eetest_stop_parser.set_defaults(func=run_ansible, play='eetest/stop')

    eetest_terminate_parser = eetest_subparser.add_parser(
        'terminate',
        help='terminate only Docker EE test instances'
    )
    eetest_terminate_parser.set_defaults(func=run_ansible, play='eetest/terminate')

    eetest_windows_parser = eetest_subparser.add_parser(
        'windows',
        help='install Docker EE test version on Windows nodes'
    )
    eetest_windows_parser.set_defaults(func=eetest_windows, play='eetest/windows')

    k8s_subparser = k8s_parser.add_subparsers(
        description=None,
        help='',
        metavar='<subcommand>',
        title='Commands'
    )

    k8s_install_parser = k8s_subparser.add_parser(
        'install',
        help='install Kubernetes on Docker CE'
    )
    k8s_install_parser.set_defaults(func=run_ansible, play='k8s/install')

    k8s_start_parser = k8s_subparser.add_parser(
        'start',
        help='start any stopped k8s instances'
    )
    k8s_start_parser.set_defaults(func=run_ansible, play='k8s/start')

    k8s_status_parser = k8s_subparser.add_parser(
        'status',
        help='display running or stopped k8s instances'
    )
    k8s_status_parser.set_defaults(func=run_ansible, play='k8s/status')

    k8s_stop_parser = k8s_subparser.add_parser(
        'stop',
        help='shut down running k8s instances'
    )
    k8s_stop_parser.set_defaults(func=run_ansible, play='k8s/stop')

    k8s_terminate_parser = k8s_subparser.add_parser(
        'terminate',
        help='terminate only k8s instances'
    )
    k8s_terminate_parser.set_defaults(func=run_ansible, play='k8s/terminate')

    args = parser.parse_args()
    args.func(args)

def run_ansible(args):
    create_ec2ini_allyml()

    if 'ec2tag' in args and args.ec2tag:
        call(['ansible-playbook', args.play + '.yml', '-e', 'ec2tag=' + args.ec2tag])

    else:
        call(['ansible-playbook', args.play + '.yml'])

def setup(args=None):
    # vars_files in setup/setup.yml will error if the file doesn't exist
    open('/bind/demokit.yml', 'a').close()

    call(['ansible-playbook', '-i', 'inventory/base', 'setup/demokit.yml'])

    if not os.path.exists('/bind/settings'):
        settings(None)

def setup_ee():
    call(['ansible-playbook', '-i', 'inventory/base', 'setup/ee.yml'])

def setup_eetest():
    call(['ansible-playbook', '-i', 'inventory/base', 'setup/eetest.yml'])

def setup_windows():
    call(['ansible-playbook', '-i', 'inventory/base', 'setup/windows.yml'])

def settings(args):
    call(['ansible-playbook', '-i', 'inventory/base', 'setup/settings.yml'])
    print('demokit is setup! Before installing a demo, run the command below to configure AWS VPC, security groups and letsencrypt certs\n')
    print('    demokit aws config\n')

def ssh(args):
    create_ssh_config()
    call(['ssh', '-t', sys.argv[2]])

def welcome():
    print('Welcome to demokit!  A directory for settings is required. An alias is recommended.')
    print('Review the commands below and customize. Or just copy/paste:\n')
    print('    mkdir ~/demokit')
    print('    echo "alias demokit=\'docker run --rm -v ~/demokit:/bind -it demokit/demokit\'" >> ~/.bashrc')
    print('    source ~/.bashrc')
    print('    demokit\n')

def main():
    ascii_art()

    if not os.path.isdir('/bind'):
        welcome()
        return

    if not os.path.exists('/bind/demokit.yml'):
        setup()
        return

    stream = file('/bind/demokit.yml', 'r')
    vars = yaml.load(stream)
    req_vars = [
        'aws_access_key_id', 'aws_secret_access_key', 'aws_region', 'aws_route53_domain',
        'aws_owner_tag'
    ]

    if not vars or not all(key in vars and vars[key] is not None for key in req_vars):
        print("\ndemokit isn't setup correctly. Running setup again...\n")
        setup()
        return

    parser()

if __name__ == '__main__':
   main()