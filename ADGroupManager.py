'''
Created on Sep 16, 2019

@author: zack.ramjan
'''

import sys
import Ldap
import getpass 
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='commands', dest="command")
    # A list command
    list_parser = subparsers.add_parser('list', help='List members of group')
    list_parser.add_argument('group', action='store', help='group to list members of')
    
    # the add command
    create_parser = subparsers.add_parser('add', help='add user to group')
    create_parser.add_argument('user', action='store', help='user to add, ex: john.smith')
    create_parser.add_argument('group', action='store', help='group to add user to, ex: staffmembers',)
    
    # the delete command
    delete_parser = subparsers.add_parser('remove', help='Remove user from group')
    delete_parser.add_argument('user', action='store', help='user to remove, ex: john.smith')
    delete_parser.add_argument('group', action='store', help='group to remove user from, ex: staffmembers',)
    args = parser.parse_args()
    
    if not args.command: 
        parser.print_help()
        sys.exit() 
    
    binddn = input("username: ")
    if "@vai.org" not in binddn.lower():
        binddn += "@vai.org" 
    bindpw=getpass.getpass(prompt='Password: ', stream=None) 
    server='vai.org'
    base='dc=vai,dc=org'
    myLdap = Ldap.Ldap( binddn,bindpw,server,base,debug=True)
    
    
    if args.command == 'list':
        print ("listing " + args.group)
        groupdn = myLdap.searchGroup(args.group)
        for m in myLdap.getMembers(groupdn):
            print("\t" + m) 
    
    if args.command == 'add':
        print ("adding " + args.user + " to " + args.group)
        groupdn = myLdap.searchGroup(args.group)
        userdn = myLdap.searchUsername(args.user)
        myLdap.addUserToGroup(userdn,groupdn)
        if not myLdap.verifyUserInGroup(userdn, groupdn):
            sys.stderr.write("ERROR: " + userdn + " is not in " + groupdn + "\nExiting\n")
   
    if args.command == 'remove':
        print ("removing " + args.user + " from " + args.group)
        groupdn = myLdap.searchGroup(args.group)
        userdn = myLdap.searchUsername(args.user)
        myLdap.removeUsersInGroups(userdn,groupdn)
        if myLdap.verifyUserInGroup(userdn, groupdn):
            sys.stderr.write("ERROR: " + userdn + " is still in " + groupdn + "\nExiting\n")
   
