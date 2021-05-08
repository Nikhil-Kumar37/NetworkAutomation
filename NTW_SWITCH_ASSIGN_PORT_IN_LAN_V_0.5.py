"""

        .SYNOPSIS
          Assigning port to the requested VLAN

        .DESCRIPTION
          The script add the device port to the requested VLAN by the user.

        .INPUTS
          Inputs are coming by CMD Line argument - vlanNumber, 

        .OUTPUT
          A Outupt will be sent to the workflow with yes or no.
          output = {"retCode" : "1", "result" : "NULL", "retDesc" : "Switch login failed"}
          Yes - Port assigned successfully
          No  - Port assigned unsusccessfully

        .EXAMPLE

          > python C:\Network_Scripts\NTW_SWITCH_ASSIGN_PORT_IN_LAN_V_0.5.py --vlanNumber=VLANNUMBER --deviceInterfacePort=DEVICEINTERFACEPORT --switchIp=SWITCHIP --deviceType=DEVICETYPE
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

##### Assigning port in the VLAN of the switch #####

try:
        configCommands = ["Interface " + interfacePort, "Switchport mode access", "Switchport access vlan " + vlanNumber, "no shut"]
        switchConnect.send_config_set(configCommands)
except:
        output = {"retCode" : "1", "result" : "NULL", "retDesc" : "Script command execution failed"}
        write_log(3, err.message)
        exit_script(1,"Script command execution failed", output)
        
##### Executing in the switch and storing the output in scriptOutput variable #####        

try:
        switchConnect.exit_config_mode()
        resultVerify = switchConnect.send_command_expect("sh interface " + interfacePort + " status | include " + vlanNumber)
        switchConnect.save_config()
        switchConnect.exit_enable_mode()   
        if (resultVerify) and (resultVerify.split()[2] == vlanNumber):
                output = {"retCode" : "0", "result" : "success", "retDesc" : "Port assigned successfully"}
                write_log(1,"Command executed successfully & port assigned successfully")
                exit_script(3,"Port assigned successfully", output)    
        else:
                output = {"retCode" : "0", "result" : "failure", "retDesc" : "Port assign got Failed"}
                write_log(1,"Command executed successfully but port assigned unsuccessfully")
                exit_script(3,"Port assign got Failed", output)    
                
except Exception as err:
        output = {"retCode" : "1", "result" : "NULL", "retDesc" : "Assigning port verfication Failed"}
        write_log(3, err.message)
        exit_script(1, "Assigning port verfication Failed", output)

        

