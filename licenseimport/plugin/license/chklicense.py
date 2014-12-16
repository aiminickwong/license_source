import logging
import gettext
_ = lambda m: gettext.dgettext(message=m, domain='otopi')


import traceback
import gettext
_ = lambda m: gettext.dgettext(message=m, domain='ovirt-engine-setup')


from otopi import util
from otopi import plugin


from . import dialog
from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup.engine import constants as oenginecons
from ovirt_engine_setup.engine_common import constants as oengcommcons
from ovirt_engine_setup.engine_common import database

import inspect
from datetime import datetime

import time
import subprocess
print "sdddddddddddddddddddddd"
import des as des
import md5 as md5
import get_hardwareid as get_hardwareid
desKey="guofu123"


@util.export
class Plugin(plugin.PluginBase):
    """Human dialog protocol provider.

    Environment:
        DialogEnv.DIALECT -- if human activate.
        DialogEnv.BOUNDARY -- set bundary to use.

    """


    def __init__(self, context):
        super(Plugin, self).__init__(context=context)
        self._enabled = True






 
    #pop up a license input dialog
    @plugin.event(
        stage=plugin.Stages.STAGE_SETUP,
        priority=plugin.Stages.PRIORITY_FIRST,
        name="license._validate_license"
    )

    def _validate_license(self):
        #add by mujun
        vmAmount=""
        deadLine=""
        hint=''
        while True:
            
            license=dialog.validate_license(
                dialog=self.dialog,
                name='OVESETUP_ENGINE_ENABLE',
                note=(_('Please Enter your license:'),),
                hint=hint,
                prompt=True,
            )
            print "LICENSE %s" %license
            self.license=license
            try:
                licenseDe = des.strdesde(license,desKey)
                licenseName = licenseDe[0:4]
                deadLine = licenseDe[8:16]
                date_now=datetime.now().strftime("%Y%m%d")
                if date_now > deadLine:
                    self.logger.error(
                       _('License is Expired')
                    )
                    continue
                mac = get_hardwareid.get_hardwareid(license)
                #if (licenseName == md5.strmd5(mac)[0:4]):
	        if ( mac == True ):
                    self.vmAmount = licenseDe[4:8]
                    self.deadLine = licenseDe[8:16]
                # print "license key format success"
                    break
                else:
                    self.logger.error(
                       _('INVALID LICENSE')
                    )
                    self.vmAmount=''
                    self.deadLine=''
                    break
            except Exception as e:
                self.logger.error(
                   _('License key format error : %s' %e)
                )
                break


    @plugin.event(
        stage=plugin.Stages.STAGE_TERMINATE,
        priority=plugin.Stages.PRIORITY_LAST + 30,
        condition=lambda self: self._enabled,
    )
    def _terminate(self):
        self.dialog.terminate()
        self._close()


    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        condition=lambda self: self._enabled,
        priority=plugin.Stages.PRIORITY_LAST+20
    )
    def _save_license(self):
        if not hasattr(self,'license'):
            self._validate_license()
        
        try:
            stamp = int(time.time())
            dbenvkeys=oenginecons.Const.ENGINE_DB_ENV_KEYS
            print self.environment[dbenvkeys['password']]

            sqlQuery = "INSERT INTO license(licensekey, name, vm_amount, deadline, time_stamp) VALUES('%s', '%s', '%s', '%s', %s)" % (self.license,self.environment[oenginecons.PKIEnv.ORG], self.vmAmount, self.deadLine,stamp)
            #sqlQuery = "UPDATE license(licensekey, name, vm_amount, deadline, time_stamp) VALUES('%s', '%s', %s, %s, %s)" % (license, name, vmAmount, deadLine,stamp)
            #execRemoteSqlCommand("postgres","localhost", "5432","engine", sqlQuery, True, "license import error")
            database.OvirtUtils(
            plugin=self,
            dbenvkeys=oenginecons.Const.ENGINE_DB_ENV_KEYS,
            ).tryDatabaseConnect()
            print sqlQuery
            print oenginecons.Const.ENGINE_DB_ENV_KEYS 
            statement = database.Statement(
            dbenvkeys=oenginecons.Const.ENGINE_DB_ENV_KEYS,
            environment=self.environment,
            )
            print self.environment[dbenvkeys['password']]
 
            result = statement.execute(
            statement=sqlQuery,
            args=dict(
                user=self.environment[oenginecons.EngineDBEnv.USER],
            ),
            ownConnection=True,
            transaction=False,
            )            
 
        except RuntimeError as e:
            self.logger.error(
               _('Cannot connect to database: {error}').format(
                            error=e,
                        )
                )

        except Exception as e:
            self.logger.error(
               _('Save License Fail :%s' %e)
                )




