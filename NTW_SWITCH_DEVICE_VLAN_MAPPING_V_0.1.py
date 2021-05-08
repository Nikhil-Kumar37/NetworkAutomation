"""

        .SYNOPSIS
          Checking VLAN Mapping with Device Port

        .DESCRIPTION
          The script checks whether requested VLAN is mapped to the device port. According to that it sends the output to ServiceNow.

        .INPUTS
          Inputs are coming by CMD Line argument - vlanName, vlanNumber, 

        .OUTPUT
          A Outupt will be sent to the workflow with Json format.
          output = {"retCode" : "1", "result" : "NULL", "retDesc" : "Switch login failed"}
          Yes - Device is already in the network
          No  - Device is not in the netrork

        .EXAMPLE

          > python C:\Network_Scripts\NTW_SWITCH_DEVICE_VLAN_MAPPING_V_0.1.py --vlanNumber=VLANNUMBER --deviceInterfacePort=DEVICEINTERFACEPORT --switchIp=SWITCHIP --deviceType=DEVICETYPE
                          --hostName=HOSTNAME --switchPort=SWITCHPORT --userName=USERNAME --password=PASSWORD --secretPassword=SECRETPASSWORD --globalDelayFactor=2

        .NOTES

          Script Name    : NTW_VLAN_EXIST_IN_SWITCH_V_0.1
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
parser.add_argument('--deviceInterfacePort')
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
interfacePort = args.deviceInterfacePort
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

check_mandatory_vars([vlanNumber, interfacePort, switchIp, deviceType,  hostName, switchPort, userName, password, secretPassword, globalDelayFactor])


##### Connecting Switch #####

try:
        switchConnect = ConnectHandler(**switchInfo)
        switchConnect.enable()
        
except Exception as err:
        output = {"retCode" : "1", "result" : "NULL", "retDesc" : "Switch login failed"}
        write_log(3, err.message)
        exit_script(1,"Switch Login Failed", output)

##### Executing in the switch and storing the output in scriptOutput variable #####        

try:
        scriptOutput = switchConnect.send_command_expect("sh interfaces "+ interfacePort + " status | section  "+ vlanNumber)
        
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

##### Varifying the output according to the result & sending to the workflow #####        

try:
        if (scriptOutput) and (scriptOutput.split()[2] == vlanNumber):
            output = {"retCode" : "0", "result" : "present", "retDesc" : "Success"}
            write_log(1,"Command executed successfully, Vlan & Device mapping is Correct")
            exit_script(3,"Device is already in the requested Network", output)    
        else:
            output = {"retCode" : "0", "result" : "missing", "retDesc" : "Success"}
            write_log(1,"Command executed successfully, Vlan & Device mapping is not Correct")
            exit_script(4,"Device is not in the requested Network", output)
            
except Exception as err:
        output = {"retCode" : "1", "result" : "NULL", "retDesc" : "Verificatin Failed"}
        write_log(3, err.message)
        exit_script(5,"script verification failed", output)
