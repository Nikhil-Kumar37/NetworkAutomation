"""

        .SYNOPSIS
          Creating requested VLAN

        .DESCRIPTION
          Creates requested VLAN in the switch

        .INPUTS
          Inputs are coming by CMD Line argument - vlanNumber, vlanName, switchIp, deviceType, hostName, switchPort, userName, password, secretPassword, globalDelayFactor

        .OUTPUT
          A Outupt will be sent to the workflow with Json format.
          output = {"retCode" : "1", "result" : "NULL", "retDesc" : "Switch login failed"}
          Yes - VLAN creation successful
          No  - VLAN creation failed

        .EXAMPLE

          > python NTW_SWITCH_CREATE_VLAN_V_0.1 --vlanNumber=VLANNUMBER --vlanName=VLANNAME --switchIp=SWITCHIP --deviceType=DEVICETYPE
                          --hostName=HOSTNAME --switchPort=SWITCHPORT --userName=USERNAME --password=PASSWORD --secretPassword=SECRETPASSWORD --globalDelayFactor=2

        .NOTES

          Script Name    : NTW_SWITCH_CREATE_VLAN_V_0.1
          Script Version : 2.0
          Author         : Nikhil Kumar
          Creation Date  :

"""

##### Importing all required modules and Automation module #####

import netmiko
import argparse
from netmiko import ConnectHandler
import sys, os
from ITOPSA_STANDALONE_LIB_PY import *


##### Parsing the argument to script with mapping to the variable #####

parser=argparse.ArgumentParser()

parser.add_argument('--vlanNumber')
parser.add_argument('--vlanName')
parser.add_argument('--switchIp')
parser.add_argument('--deviceType')
parser.add_argument('--hostName')
parser.add_argument('--switchPort')
parser.add_argument('--userName')
parser.add_argument('--password')
parser.add_argument('--secretPassword')
parser.add_argument('--globalDelayFactor')

args=parser.parse_args()

##### Variables #####

vlanNumber = args.vlanNumber
vlanName = args.vlanName
switchIp = args.switchIp
deviceType = args.deviceType
hostName = args.hostName
switchPort = args.switchPort
userName = args.userName
password = args.password
secretPassword = args.secretPassword
globalDelayFactor = float(args.globalDelayFactor)


##### SwitchInfo variable for connecting switch #####

switchInfo = {
                'ip':           switchIp,
                'device_type':  deviceType,
                'host':         hostName,
                'port':         switchPort,
                'username':     userName,
                'password':     password,
                'secret':       secretPassword,
                'global_delay_factor': globalDelayFactor,
        }

##### Log Path for the module #####

logPath=os.path.realpath(__file__)
path(logPath)

##### Mandatory Variables #####

check_mandatory_vars([vlanNumber, vlanName, switchIp, deviceType,  hostName, switchPort, userName, password, secretPassword, globalDelayFactor])


##### Connecting Switch #####

try:
        switchConnect = ConnectHandler(**switchInfo)
        switchConnect.enable()
        switchConnect.config_mode()
        
except Exception as err:
        output = {"retCode" : "1", "result" : "NULL", "retDesc" : "Switch login failed"}
        write_log(3, err.message)
        exit_script(1,"Switch Login Failed", output)

##### Executing in the switch and storing the output in scriptOutput variable #####        

try:
        configCommands = ["vlan " + str(vlanNumber), "name " + vlanName, "State active"]
        switchConnect.send_config_set(configCommands)

except Exception as err:
        output = {"retCode" : "1", "result" : "NULL", "retDesc" : "Script command execution failed"}
        write_log(3, err.message)
        exit_script(2,"Script command execution failed", output)


##### Saving the configuration in the switch after Execution #####
        
try:
        switchConnect.exit_config_mode()
        switchConnect.save_config()
        switchConnect.exit_enable_mode()
        
except Exception as err:
        output = {"retCode" : "1", "result" : "NULL", "retDesc" : "Failed to save the configuration in Switch"}
        write_log(3, err.message)
        exit_script(3,"Failed to save the configuration in Switch", output)

##### Sending the result to the workflow #####        

output = {"retCode" : "0", "result" : vlanNumber, "retDesc" : "Success"}
write_log(1,"VLAN created successfully")
exit_script(4,"Success", output)
