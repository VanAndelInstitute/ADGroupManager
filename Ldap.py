'''
Created on Sep 17, 2019

@author: zack.ramjan
'''
from ldap3 import Server, Connection, ALL
from ldap3.extend.microsoft.addMembersToGroups import ad_add_members_to_groups as addUsersInGroups
from ldap3.extend.microsoft.removeMembersFromGroups import ad_remove_members_from_groups as removeUsersInGroups
import sys

class Ldap(object):
    '''
    classdocs
    '''


    def __init__(self, binddnIn,bindpwIn,serverIn,baseIn,debug=False):
        self.binddn = binddnIn
        self.bindpw = bindpwIn
        self.server = serverIn
        self.base = baseIn
        self.debug=debug
        self.conn = Connection(Server(self.server, get_info=ALL), self.binddn, self.bindpw, auto_bind=True)
        self.printDebug("connected to " + self.server + " as " + self.conn.extend.standard.who_am_i())
    
    
    def searchGroup(self,group):
        self.conn.search(self.base, '(&(objectclass=group)(cn=' + group + '))')
        if (len(self.conn.response) > 4):
            self.printDebug("multple groups match, exiting " + str(len(self.conn.response)))
            sys.exit()
        if "dn" in  self.conn.response[0]:    
            self.printDebug("found group " + self.conn.response[0]["dn"])
            return (self.conn.response[0]["dn"])
        else:
            self.printDebug("could not locate group")
            sys.exit()    

    def searchUsername(self,username):
        self.conn.search(self.base, '(&(objectclass=person)(sAMAccountName=' + username + '))')
        if (len(self.conn.response) > 4):
            self.printDebug("multiple username match, exiting " + str(len(self.conn.response)))
            sys.exit()
        if "dn" in  self.conn.response[0]:    
            self.printDebug("found username " + self.conn.response[0]["dn"])
            return (self.conn.response[0]["dn"])
        else:
            self.printDebug("could not locate username")
            sys.exit()
            
    def getMembers(self,groupdn):
        #self.printDebug(groupdn)
        self.conn.search(groupdn,'(objectclass=group)',attributes=['member'] )
        #for m in  self.conn.response[0]['attributes']['member']:
            #self.printDebug("\t" + m)
        return self.conn.response[0]['attributes']['member']

    def addUserToGroup(self,userdn,groupdn):
        self.printDebug("adding " + userdn + " to " + groupdn)
        addUsersInGroups(self.conn,[userdn,],[groupdn,], raise_error=True)
        
    def removeUsersInGroups(self,userdn,groupdn):
        self.printDebug("removing " + userdn + " from " + groupdn)
        removeUsersInGroups(self.conn,[userdn,],[groupdn,], fix=True, raise_error=True)    
    
    def verifyUserInGroup(self,userdn,groupdn):
        members = self.getMembers(groupdn)
        return userdn in members
    
    
    def printDebug(self,string):
        if(self.debug):
            sys.stderr.write(string + "\n")
            