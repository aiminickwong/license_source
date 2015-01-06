#! /usr/bin/python

'''
Created on 2014-12-4

@author: MUJUN
'''
import gettext
_ = lambda m: gettext.dgettext(message=m, domain='ovirt-engine-setup')


import sys
import time
import subprocess
import des
import md5
import get_hardwareid


from . import configfile


#from ovirt_engine_setup import constants as osetupcons
from . import otopi_constants as constants
from . import ConfigParser as configparser

from . import constants as oenginecons
from . import database
import os
import glob
from . import common
desKey="guofu123"

class ConectionSetup(object):
    def __init__(self):
        self.environment={}
        self._config = configparser.ConfigParser()
        self._config.optionxform = str
        self._missingconf = []

    def _readEnvironment(self, section, override):
        if self._config.has_section(section):
            for name, value in self._config.items(section):
                try:
                    value = common.parseTypedValue(value)
                except Exception as e:
                    raise RuntimeError(
                        _(
                            "Cannot parse configuration file key "
                            "{key} at section {section}: {exception}"
                        ).format(
                            key=name,
                            section=section,
                            exception=e,
                        )
                    )
                if override:
                    self.environment[name] = value
                else:
                    self.environment.setdefault(name, value)


    def resolveFile(self, file):
        """Resolve file based on installer execution directory"""
        if file is None:
            return None
        elif os.path.isabs(file):
            return file
        else:
            return os.path.join(
                self.environment[
                    constants.BaseEnv.EXECUTION_DIRECTORY
                ],
                file
            )


    def OrgResov(self):
        self.environment.setdefault(
            constants.CoreEnv.CONFIG_FILE_NAME,
            self.resolveFile(
                os.environ.get(
                    constants.SystemEnvironment.CONFIG,
                    self.resolveFile(constants.Defaults.CONFIG_FILE),
                )
            )
        )
        
        self.environment.setdefault(
            constants.CoreEnv.CONFIG_FILE_APPEND,
            None
        )

        def _addConfig(f, missingOK):
            configs = []
            if f:
                for c in f.split(':'):
                    myconfigs = []
                    configFile = self.resolveFile(c)
                    configDir = '%s.d' % configFile
                    if os.path.exists(configFile):
                        myconfigs.append(configFile)
                    myconfigs += sorted(
                        glob.glob(
                            os.path.join(configDir, '*.conf')
                        )
                    )
                    configs.extend(myconfigs)
                    if not missingOK and not myconfigs:
                        self._missingconf.append(c)
            return configs
        #self.environment[constants.CoreEnv.CONFIG_FILE_NAME]="/etc/ovirt-engine-setup.conf"
        self._configFiles = self._config.read(
            _addConfig(
                f='/etc/ovirt-engine-setup.conf',
                missingOK=True
            ) +
            _addConfig(
                f=self.environment[constants.CoreEnv.CONFIG_FILE_APPEND],
                missingOK=False
            )
        )
        self._readEnvironment(
            section=constants.Const.CONFIG_SECTION_DEFAULT,
            override=False
        )
        self._readEnvironment(
            section=constants.Const.CONFIG_SECTION_INIT,
            override=True
        )




    def _setup(self):
        dbenvkeys=oenginecons.Const.ENGINE_DB_ENV_KEYS

        config = configfile.ConfigFile([
            oenginecons.FileLocations.OVIRT_ENGINE_SERVICE_CONFIG_DEFAULTS,
            oenginecons.FileLocations.OVIRT_ENGINE_SERVICE_CONFIG
        ])
        if config.get('ENGINE_DB_PASSWORD'):
            try:
                dbenv = {}
                for e, k in (
                    (oenginecons.EngineDBEnv.HOST, 'ENGINE_DB_HOST'),
                    (oenginecons.EngineDBEnv.PORT, 'ENGINE_DB_PORT'),
                    (oenginecons.EngineDBEnv.USER, 'ENGINE_DB_USER'),
                    (oenginecons.EngineDBEnv.PASSWORD, 'ENGINE_DB_PASSWORD'),
                    (oenginecons.EngineDBEnv.DATABASE, 'ENGINE_DB_DATABASE'),
                ):
                    dbenv[e] = config.get(k)
                for e, k in (
                    (oenginecons.EngineDBEnv.SECURED, 'ENGINE_DB_SECURED'),
                    (
                        oenginecons.EngineDBEnv.SECURED_HOST_VALIDATION,
                        'ENGINE_DB_SECURED_VALIDATION'
                    )
                ):
                    dbenv[e] = config.getboolean(k)

                self.environment.update(dbenv)
            except RuntimeError as e:
                print 'Existing credential use failed'
                msg = _(
                    'Cannot connect to Engine database using existing '
                    'credentials: {user}@{host}:{port}'
                ).format(
                    host=dbenv[oenginecons.EngineDBEnv.HOST],
                    port=dbenv[oenginecons.EngineDBEnv.PORT],
                    database=dbenv[oenginecons.EngineDBEnv.DATABASE],
                    user=dbenv[oenginecons.EngineDBEnv.USER],
                )


    def save2db(self,sqlQuery):
        try:
            dbenvkeys=oenginecons.Const.ENGINE_DB_ENV_KEYS

            #sqlQuery = "UPDATE license(licensekey, name, vm_amount, deadline, time_stamp) VALUES('%s', '%s', %s, %s, %s)" % (license, name, vmAmount, deadLine,stamp)
            #execRemoteSqlCommand("postgres","localhost", "5432","engine", sqlQuery, True, "license import error")
            statement = database.Statement(
            dbenvkeys=oenginecons.Const.ENGINE_DB_ENV_KEYS,
            environment=self.environment,
            )
 
            result = statement.execute(
            statement=sqlQuery,
            args=dict(
                user=self.environment[oenginecons.EngineDBEnv.USER],
            ),
            ownConnection=True,
            transaction=False,
            )            
            return result 
        except RuntimeError as e:
               print e
               print ('Cannot connect to database: {error}').format(
                            error=e,
                        )
               return None
        except Exception as e:
               print ('Save License Fail :%s' %e)
               raise Exception("Save License Fail")
                


#
def execSQLOperation(sqlQuery):

    userName=csetup.environment[oenginecons.EngineDBEnv.USER]
    dbHost=csetup.environment[oenginecons.EngineDBEnv.HOST]
    dbPort=csetup.environment[oenginecons.EngineDBEnv.PORT]
    dbName=csetup.environment[oenginecons.EngineDBEnv.DATABASE]
    psw=csetup.environment[oenginecons.EngineDBEnv.PASSWORD]
    return csetup.save2db(sqlQuery)
    #execRemoteSqlCommand(userName,dbHost, dbPort,dbName,psw,sqlQuery, True, "license import error")





def _addLicensetoDB(license,name,vmAmount,deadLine,old_license=None):
    stamp = int(time.time())
    #deletesql="DELETE FROM license"
    #execSQLOperation(deletesql)
    if old_license == license:
        print "License is old,no need to update"
        return  
    sqlQuery = "INSERT INTO license(licensekey, name, vm_amount, deadline, time_stamp) VALUES('%s', '%s', '%s', '%s', %s)" % (license, name, vmAmount, deadLine,stamp)
    
    execSQLOperation(sqlQuery)

    deletesql="DELETE FROM license where licensekey='%s'" %old_license
    execSQLOperation(deletesql)
 


    print "UPDATE SUCCESSFULLY"

    #sqlQuery = "UPDATE license(licensekey, name, vm_amount, deadline, time_stamp) VALUES('%s', '%s', %s, %s, %s)" % (license, name, vmAmount, deadLine,stamp)
    #execRemoteSqlCommand("postgres","localhost", "5432","engine", sqlQuery, True, "license import error")
     
    #execRemoteSqlCommand("engine","localhost", "5432","engine", sqlQuery, True, "license import error")

def execRemoteSqlCommand(userName, dbHost, dbPort, dbName,psw, sqlQuery, failOnError=False, errMsg="license import error"):
    cmd = "/usr/bin/psql -h %s -p %s -U %s -d %s -c \"%s\" -w %s" % (dbHost, dbPort, userName, dbName, sqlQuery,psw)
    return execExternalCmd(cmd, failOnError, errMsg)

def execExternalCmd(command, failOnError=False, msg="license import error", maskList=[]):
    """
    Run External os command
    Receives maskList to allow passwords masking
    """
    p = subprocess.Popen(command, shell=True,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, close_fds=True)
    out, err = p.communicate()
    output = out + err
    #if failOnError and p.returncode != 0:
    #    raise Exception(msg)
    print output
    return ("".join(output.splitlines(True)), p.returncode)

csetup=ConectionSetup()
csetup._setup()
csetup.OrgResov() 
def run(name,license):
    vmAmount=""
    deadLine=""
    try:
        if not name:
            raise Exception("Please Enter your Orgnazation Name") 
        if not license:
            raise Exception('please Enter your License')
        sqlQuery = "select name,licensekey from license limit 1"
        #result=execSQLOperation(sqlQuery)
        result=None
        #FQDN='OVESETUP_CONFIG/fqdn'
        if result:
            
            org=result[0]['name'] 
        #if '.' in csetup.environment[FQDN]:
        #    org = csetup.environment[
        #    FQDN
        #].split('.', 1)[1]
            if not org==name :
                raise Exception("Invalid Orgnazation Name")
            old_license=result[0]['licensekey']
        else:
            old_license = None
    except Exception as e:
        print e
        import sys
        sys.exit(0)

    try:
        licenseDe = des.strdesde(license,desKey)
        deadLine = licenseDe[8:16]
        try:
            int(deadLine)
            if not len(deadLine) == 8:
                raise Exception
        except:
            raise Exception("invalid license") 
        from datetime import datetime
        date_now=datetime.now().strftime("%Y%m%d")
        if date_now > deadLine:
            raise Exception("LICENSE IS EXPIRED")
        licenseName = licenseDe[0:4]
        mac = get_hardwareid.get_hardwareid(license)
        #if (licenseName == md5.strmd5(mac)[0:4]):
	if ( mac == True ):
            vmAmount = licenseDe[4:8]
            deadLine = licenseDe[8:16]
            # print "license key format success"
        else:
            raise Exception("invalid license")
    except Exception as e:
        print e
        print "license key format error"
        import sys
        sys.exit(0)
    #_addLicensetoDB(license,'','','')

    _addLicensetoDB(license,name,vmAmount,deadLine,old_license=old_license)
    
