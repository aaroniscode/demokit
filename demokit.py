import argparse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from subprocess import call
import os
import sys
import yaml

# TODO: function to load /bind/demokit.yml and catch exception if not valid YAML

def ascii_art():
    print("     _                      _    _ _   ")
    print("  __| | ___ _ __ ___   ___ | | _(_) |_ ")
    print(" / _` |/ _ \ '_ ` _ \ / _ \| |/ / | __|")
    print("| (_| |  __/ | | | | | (_) |   <| | |_ ")
    print(" \__,_|\___|_| |_| |_|\___/|_|\_\_|\__|\n")

def aws_config(args):
    run_ansible('aws/configure')

def aws_destroy(args):
    run_ansible('aws/destroy')

def aws_run(args):
    run_ansible('aws/run')

def aws_start(args):
    run_ansible('aws/start')

def aws_status(args):
    run_ansible('aws/status')

def aws_stop(args):
    run_ansible('aws/stop')

def aws_terminate(args):
    run_ansible('aws/terminate')

def check_ee():
    vars = yaml.load(file('/bind/demokit.yml', 'r'))

    ee_req_vars = ['docker_ee_url', 'ucp_password']

    if not all(key in vars and vars[key] is not None for key in ee_req_vars):
        setup_ee()

def check_eetest():
    vars = yaml.load(file('/bind/demokit.yml', 'r'))

    eetest_req_vars = ['docker_hub_username', 'docker_hub_email', 'docker_hub_password', 
        'eetest_engine_version', 'eetest_ucp_version', 'eetest_dtr_version']

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
    
    template = env.get_template('ec2.ini.j2')

    with open('/demokit/inventory/ec2.ini', 'wb') as fh:
        fh.write(template.render(vars))

    template = env.get_template('all.yml.j2')

    with open('/demokit/inventory/group_vars/all.yml', 'wb') as fh:
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
    run_ansible('ee/install')

def ee_start(args):
    run_ansible('ee/start')

def ee_status(args):
    run_ansible('ee/status')

def ee_stop(args):
    run_ansible('ee/stop')

def ee_terminate(args):
    run_ansible('ee/terminate')

def ee_windows(args):
    check_ee()
    check_windows()
    run_ansible('ee/windows')

def eetest(args):
    print('Feature under development...')

def eetest_install(args):
    check_ee()
    check_eetest()
    run_ansible('eetest/install')

def eetest_start(args):
    run_ansible('eetest/start')

def eetest_status(args):
    run_ansible('eetest/status')

def eetest_stop(args):
    run_ansible('eetest/stop')

def eetest_terminate(args):
    run_ansible('eetest/terminate')

def eetest_windows(args):
    check_ee()
    check_eetest()
    check_windows()
    run_ansible('eetest/windows')

def k8s_install(args):
    run_ansible('k8s/install')

def k8s_start(args):
    run_ansible('k8s/start')

def k8s_status(args):
    run_ansible('k8s/status')

def k8s_stop(args):
    run_ansible('k8s/stop')

def k8s_terminate(args):
    run_ansible('k8s/terminate')

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

    aws_parser = subparser.add_parser('aws', help='commands to manage AWS resources')
    debug_parser = subparser.add_parser('debug').set_defaults(func=debug)
    ee_parser = subparser.add_parser('ee', help='commands to demo Docker EE 2.0')
    eetest_parser = subparser.add_parser('eetest', help='commands to demo Docker EE test versions (coming soon)').set_defaults(func=eetest)
    k8s_parser = subparser.add_parser('k8s', help='commands to demo Kubernetes on Docker CE')  
    subparser.add_parser('settings', help='reset demo settings, backup any changed files').set_defaults(func=settings)
    subparser.add_parser('setup', help='update demokit configuration').set_defaults(func=setup)
    ssh_parser = subparser.add_parser('ssh', help='ssh into EC2 instance')
    ssh_parser.add_argument('hostname', help='EC2 instance hostname')
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
    aws_config_parser.set_defaults(func=aws_config)

    aws_destroy_parser = aws_subparser.add_parser(
        'destroy',
        help='terminate EC2 instances and destroy all AWS resources'
    )
    aws_destroy_parser.set_defaults(func=aws_destroy)

    aws_run_parser = aws_subparser.add_parser(
        'run',
        help='launch all EC2 instances in settings/aws_ec2.yml'
    )
    aws_run_parser.set_defaults(func=aws_run)
    
    aws_start_parser = aws_subparser.add_parser(
        'start',
        help='start any stopped EC2 instances'
    )
    aws_start_parser.set_defaults(func=aws_start)

    aws_status_parser = aws_subparser.add_parser(
        'status',
        help='display any running or stopped EC2 instances'
    )
    aws_status_parser.set_defaults(func=aws_status)

    aws_stop_parser = aws_subparser.add_parser(
        'stop',
        help='shut down all running EC2 instances'
    )
    aws_stop_parser.set_defaults(func=aws_stop)

    aws_terminate_parser = aws_subparser.add_parser(
        'terminate',
        help='terminate all EC2 instances'
    )
    aws_terminate_parser.set_defaults(func=aws_terminate)

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
    ee_install_parser.set_defaults(func=ee_install)

    ee_start_parser = ee_subparser.add_parser(
        'start', 
        help='start any stopped Docker EE demo instances'
    )
    ee_start_parser.set_defaults(func=ee_start)

    ee_status_parser = ee_subparser.add_parser(
        'status', 
        help='display running or stopped Docker EE demo instances'
    )
    ee_status_parser.set_defaults(func=ee_status)

    ee_stop_parser = ee_subparser.add_parser(
        'stop', 
        help='shut down running Docker EE demo instances'
    )
    ee_stop_parser.set_defaults(func=ee_stop)

    ee_terminate_parser = ee_subparser.add_parser(
        'terminate', 
        help='terminate only Docker EE demo instances'
    )
    ee_terminate_parser.set_defaults(func=ee_terminate)

    ee_windows_parser = ee_subparser.add_parser(
        'windows', 
        help='install Docker EE Windows nodes'
    )
    ee_windows_parser.set_defaults(func=ee_windows)

    # eetest_subparser = eetest_parser.add_subparsers(
    #     description=None,
    #     help='', 
    #     metavar='<subcommand>',
    #     title='Commands'        
    # )

    # eetest_install_parser = eetest_subparser.add_parser(
    #     'install', 
    #     help='install Docker EE UCP, DTR test versions'
    # )
    # eetest_install_parser.set_defaults(func=eetest_install)

    # eetest_start_parser = eetest_subparser.add_parser(
    #     'start', 
    #     help='start any stopped Docker EE test instances'
    # )
    # eetest_start_parser.set_defaults(func=eetest_start)

    # eetest_status_parser = eetest_subparser.add_parser(
    #     'status', 
    #     help='display running or stopped Docker EE test instances'
    # )
    # eetest_status_parser.set_defaults(func=eetest_status)

    # eetest_stop_parser = eetest_subparser.add_parser(
    #     'stop', 
    #     help='shut down running Docker EE test instances'
    # )
    # eetest_stop_parser.set_defaults(func=eetest_stop)

    # eetest_terminate_parser = eetest_subparser.add_parser(
    #     'terminate', 
    #     help='terminate only Docker EE test instances'
    # )
    # eetest_terminate_parser.set_defaults(func=eetest_terminate)

    # eetest_windows_parser = eetest_subparser.add_parser(
    #     'windows', 
    #     help='install Docker EE test version on Windows nodes'
    # )
    # eetest_windows_parser.set_defaults(func=eetest_windows)

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
    k8s_install_parser.set_defaults(func=k8s_install)

    k8s_start_parser = k8s_subparser.add_parser(
        'start', 
        help='start any stopped k8s instances'
    )
    k8s_start_parser.set_defaults(func=k8s_start)

    k8s_status_parser = k8s_subparser.add_parser(
        'status', 
        help='display running or stopped k8s instances'
    )
    k8s_status_parser.set_defaults(func=k8s_status)

    k8s_stop_parser = k8s_subparser.add_parser(
        'stop', 
        help='shut down running k8s instances'
    )
    k8s_stop_parser.set_defaults(func=k8s_stop)

    k8s_terminate_parser = k8s_subparser.add_parser(
        'terminate', 
        help='terminate only k8s instances'
    )
    k8s_terminate_parser.set_defaults(func=k8s_terminate)

    args = parser.parse_args()
    args.func(args)

def run_ansible(play):
    create_ec2ini_allyml()
    call(['ansible-playbook', play + '.yml'])

def setup(args):    
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
    print('demokit setup is complete! Before installing your demo, configure AWS VPC, security groups and letsencrypt certs\n')
    print('    demokit aws config\n')

def ssh(args):
    create_ssh_config()
    call(['ssh', '-t', sys.argv[2]])

def main():
    ascii_art()

    if not os.path.isdir('/bind'):
        welcome()
        return

    if not os.path.exists('/bind/demokit.yml'):
        setup(None)
        return

    stream = file('/bind/demokit.yml', 'r')
    vars = yaml.load(stream)
    req_vars = ['aws_profile', 'aws_region', 'aws_route53_domain']

    if not all(key in vars and vars[key] is not None for key in req_vars):
        print("\ndemokit isn't setup correctly. Running setup again...\n")
        setup(None)
        return

    parser()

def welcome():
    print('Welcome to demokit!  You need a local directory to save settings.\n')
    print('    mkdir ~/demokit\n')
    print('Create an alias, because life.\n')
    print('    alias demokit="docker run --rm -v ~/demokit:/bind -v ~/.aws:/root/.aws -it demokit/demokit"\n')
    print('Run demokit.\n')
    print('    demokit\n')

if __name__ == '__main__':
   main()