#!/usr/bin/env python 

import os

import utils


def travis(_: str):
    travis_fn = os.path.join(d, '.travis.yml')
    if os.path.exists(travis_fn):
        print('rm -rf %s' % travis)


def git(directory_name: str):
    print('git pull')
    print('git commit -am `pwd` ')
    print('git push')


def repositories(directory: str):
    class Repository(object):
        def __init__(self, url, name, id) -> None:
            super().__init__()
            self.url = url
            self.name = name
            self.id = id

    def check_repositories(m_dict: dict):
        main_collection = []
        plugin_collection = []

        def collect_repos(tag, sub_tag, the_list):
            repos = m_dict['project'][tag]
            for r in repos[sub_tag]:
                url = r['url']
                name = r['name']
                id = r['id']
                the_list.append(Repository(url, name, id))

        collect_repos('repositories', 'repository', main_collection)
        collect_repos('pluginRepositories', 'pluginRepository', plugin_collection)

        assert len(main_collection) == 2, 'there should be 2 main repositories'
        assert len(plugin_collection) == 2, 'there should be 2 plugin repositories'

        def validate_repositories(c):
            assert len(
                [a for a in c if
                 'cloudnativejava' in a.url]) == 2, 'there should be two CNJ repositories in %s ' % directory

        validate_repositories(plugin_collection)
        validate_repositories(main_collection)

    utils.process_pom(os.path.join(directory, 'pom.xml'), check_repositories)

def spring_cloud_version(directory: str):

    def check_properties(the_dict: dict):
        utils.check_property(the_dict, 'spring-cloud.version', 'Hoxton.SR3')
        utils.check_property(the_dict, 'java.version', '11')
        utils.check_property(the_dict, 'spring-cloud-spring-service-connector.version', '2.0.1.RELEASE')
        utils.check_property(the_dict, 'kotlin.version', '1.3.61')

    utils.process_pom(os.path.join(directory, 'pom.xml'), check_properties)



def spring_boot_version(directory: str):
    def check_version(the_dict: dict):
        match = '2.2.5'
        if match not in the_dict['project']['parent']['version']:
            print('the pom.xml does not match the required version')

    utils.process_pom(os.path.join(directory, 'pom.xml'), check_version)


if __name__ == '__main__':
    twi = os.path.expanduser('~/code/this-week-in')
    handlers = [spring_boot_version, spring_cloud_version, repositories, travis, git ]
    dirs = [os.path.join(twi, x) for x in os.listdir(twi)]
    for d in dirs:
        if os.path.isdir(d):
            print('cd %s' % d)
            for f in handlers:
                f(d)
