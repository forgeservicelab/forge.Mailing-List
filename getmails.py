#!/usr/bin/env python
"""Retrieve a list of all active email addresses on FORGE LDAP database

Usage:
    getmails.py <username> <password>
    getmails.py <username> -p
    getmails.py -h | --help

Options:
    -h --help           Show this screen.
    -p --pass           Interactive password
"""
import ldap
import getpass
from docopt import docopt


def _getMailList(user, passwd):
    conn = ldap.initialize('ldaps://auth.forgeservicelab.fi')
    conn.bind_s('cn=%s,ou=accounts,dc=forgeservicelab,dc=fi' % user, passwd)
    searchres = conn.search_s('ou=accounts,dc=forgeservicelab,dc=fi',
                              ldap.SCOPE_ONELEVEL,
                              filterstr='(!(|(employeeType=hidden)(employeeType=disabled)(cn=test*)(sn=service)))',
                              attrlist=['mail'])
    conn.unbind_s()

    return [mail for maillist in map(lambda entry: entry[1]['mail'], searchres) for mail in maillist]


if __name__ == '__main__':
    args = docopt(__doc__)

    if args['--pass']:
        args['<password>'] = getpass.getpass()

    print _getMailList(args['<username>'], args['<password>'])
