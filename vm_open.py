#!/usr/bin/env python

"""
Python script that will automatically open virtual machines from a computer in VMWare Workstation 12. Here are the more
detailed specifics of what the script should do:

-Opening 5 virtual machines randomly from the total pool of all virtual machines in VMWare Workstation 12, with a short
interval of 1-60 seconds between opening each of these 5 virtual machines
-Waiting 15 minutes then closing all 5 of the opened virtual machines
-restart Verizon hotspot via http://my.jetpack
-Opening 5 new randomly selected virtual machines and repeating the process from the beginning
-Continuing to do these steps until every virtual machine in VMWare Workstation 12 has been accessed, each virtual
machine having only been opened and closed one time

"""

from __future__ import print_function

import atexit

from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim

import ssl
import random
import time

import hashlib
import requests
import re

VMWARE_HOST = '127.0.1.1'
VMWARE_USER = 'DESKTOP-J53J8RM\VM-Thor'
VMWARE_PWD = 'Adcrush123!'
VMWARE_PORT = 443

BUSY_LOOP_DELAY = 3

VM_GROUP_SIZE = 5

MIN_DELAY = 1
MAX_DELAY = 60

RUN_TIME = (60*15)

HOTSPOT_DELAY = (60*3)
HOTPSPOT_PASSWORD = '0def8621'


def print_vm_info(virtual_machine):
    """
    Print information for a particular virtual machine or recurse into a
    folder with depth protection
    """
    summary = virtual_machine.summary
    print("Name       : ", summary.config.name)
    print("Template   : ", summary.config.template)
    print("Path       : ", summary.config.vmPathName)
    print("Guest      : ", summary.config.guestFullName)
    print("Instance UUID : ", summary.config.instanceUuid)
    print("Bios UUID     : ", summary.config.uuid)
    annotation = summary.config.annotation
    if annotation:
        print("Annotation : ", annotation)
    print("State      : ", summary.runtime.powerState)
    if summary.guest is not None:
        ip_address = summary.guest.ipAddress
        tools_version = summary.guest.toolsStatus
        if tools_version is not None:
            print("VMware-tools: ", tools_version)
        else:
            print("Vmware-tools: None")
        if ip_address:
            print("IP         : ", ip_address)
        else:
            print("IP         : None")
    if summary.runtime.question is not None:
        print("Question  : ", summary.runtime.question.text)
    print("")


def login_hotspot(jar):

    # request home page to check in logged in
    url = 'http://my.jetpack/'
    response = requests.get(url, cookies=jar)
    response.raise_for_status()

    match = re.search('(<a href="/login/">Sign In</a>)', response.text)
    if match is not None:
        # print("Need to login to hotspot")

        url = 'http://my.jetpack/login/'
        response = requests.get(url, cookies=jar)
        response.raise_for_status()

        match = re.search('id="gSecureToken" value="([^"]*)"', response.text)
        if match is None:
            print(response.text)
            print(response.headers)
            raise ValueError("Unable to find gSecureToken")

        gSecureToken = match.group(1)

        payload = {
            'shaPassword': hashlib.sha1(HOTPSPOT_PASSWORD+gSecureToken).hexdigest(),
            'inputPassword': gSecureToken[:8],
            'gSecureToken': gSecureToken,
            'redirectLocation': '/',
        }

        url = 'http://my.jetpack/login/'
        response = requests.post(url, data=payload, cookies=jar)
        response.raise_for_status()

        match = re.search('(<a href="/logout/">Sign Out</a>)', response.text)
        if match is None:
            print(response.text)
            print(response.headers)
            raise ValueError("Unable to login to device")

    else:
        #  should be already logged in; check though
        match = re.search('(<a href="/logout/">Sign Out</a>)', response.text)
        if match is not None:
            # print("Already logged in")
            pass
        else:
            print(response.text)
            print(response.headers)
            raise ValueError("Internal error - should have been logged in")
    return


def restart_hotspot():
    print("Connecting to device")

    jar = requests.cookies.RequestsCookieJar()
    login_hotspot(jar)

    print("Getting IP address")
    url = 'http://my.jetpack/internet/'
    response = requests.get(url, cookies=jar)
    response.raise_for_status()
    match = re.search('<div class="col input" id="internetStatusIPAddress">([0-9.]*)</div>', response.text)
    if match is None:
        print(response.text)
        print(response.headers)
        raise ValueError("Unable to login to device")
    old_ip = match.group(1)
    print("Current IP address is %s" % old_ip)

    # login, now restart
    print("Restarting")
    url = 'http://my.jetpack/restarting/'
    response = requests.get(url, cookies=jar)
    response.raise_for_status()

    match = re.search('This MiFi device will now restart', response.text)
    if match is None:
        print(response.text)
        print(response.headers)
        raise ValueError("Unable to restart device")

    # extract gSecureToken
    match = re.search('data : { gSecureToken : "([^"]*)" }', response.text)
    if match is None:
        print(response.text)
        print(response.headers)
        raise ValueError("Unable to find gSecureToken")

    gSecureToken = match.group(1)

    payload = {
        'gSecureToken': gSecureToken
    }

    url = 'http://my.jetpack/cgi/webui.cgi?id=restarting&as=1&reboot=true'
    response = requests.post(url, data=payload, cookies=jar)
    response.raise_for_status()

    time.sleep(HOTSPOT_DELAY)

    # check restarted ok
    url = 'http://my.jetpack/'
    response = requests.get(url, cookies=jar)
    response.raise_for_status()
    match = re.search('My Jetpack Home', response.text)
    if match is None:
        print(response.text)
        print(response.headers)
        raise ValueError("Device did not restart ok")

    login_hotspot(jar)
    print("Getting new IP address")
    url = 'http://my.jetpack/internet/'
    response = requests.get(url, cookies=jar)
    response.raise_for_status()
    match = re.search('<div class="col input" id="internetStatusIPAddress">([0-9.]*)</div>', response.text)
    if match is None:
        print(response.text)
        print(response.headers)
        raise ValueError("Unable to login to device")
    new_ip = match.group(1)

    if old_ip == new_ip:
        raise ValueError("IP address did not change after restart: %s" % new_ip)

    print("Current IP address is %s" % new_ip)


def start_vm_batch(crt_vm_list):
    task_list = []

    for vm in crt_vm_list:
        if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
            # VM already started
            raise ValueError("VM %s is already started.  Aborting cycle." % vm.name)

        time.sleep(random.randrange(MIN_DELAY, MAX_DELAY))
        print("Starting %s" % vm.name)
        task = vm.PowerOn()
        task_list.append({
            "vm": vm,
            "task": task,
            })

    while task_list:
        time.sleep(BUSY_LOOP_DELAY)
        if task_list[0]["task"].info.state == vim.TaskInfo.State.success:
            print("VM %s started successful" % task_list[0]["vm"].name)
            task_list.pop(0)
        elif task_list[0]["task"].info.state == vim.TaskInfo.State.error:
            # some vSphere errors only come with their class and no other message
            print("error type: %s" % task_list[0]["task"].info.error.__class__.__name__)
            print("found cause: %s" % task_list[0]["task"].info.error.faultCause)
            for fault_msg in task_list[0]["task"].info.error.faultMessage:
                print(fault_msg.key)
                print(fault_msg.message)
            raise ValueError("Error starting VM %s" % task_list[0]["vm"].name)


def stop_vm_batch(crt_vm_list):
    task_list = []

    for vm in crt_vm_list:
        if vm.runtime.powerState != vim.VirtualMachinePowerState.poweredOn:
            # VM already started
            raise ValueError("VM %s is already stop.  Aborting cycle." % vm.name)

        time.sleep(random.randrange(MIN_DELAY, MAX_DELAY))
        print("Stop %s" % vm.name)
        task = vm.PowerOff()
        task_list.append({
            "vm": vm,
            "task": task,
            })

    while task_list:
        time.sleep(BUSY_LOOP_DELAY)
        if task_list[0]["task"].info.state == vim.TaskInfo.State.success:
            print("VM %s stop successful" % task_list[0]["vm"].name)
            task_list.pop(0)
        elif task_list[0]["task"].info.state == vim.TaskInfo.State.error:
            # some vSphere errors only come with their class and no other message
            print("error type: %s" % task_list[0]["task"].info.error.__class__.__name__)
            print("found cause: %s" % task_list[0]["task"].info.error.faultCause)
            for fault_msg in task_list[0]["task"].info.error.faultMessage:
                print(fault_msg.key)
                print(fault_msg.message)
            raise ValueError("Error stop VM %s" % task_list[0]["vm"].name)
        # check for a question
        elif task_list[0]["vm"].runtime.question is not None:
            question_id = task_list[0]["vm"].runtime.question.id
            question = task_list[0]["vm"].runtime.question.text
            choices = task_list[0]["vm"].runtime.question.choice.choiceInfo
            print("Got a question id : %s" % question_id)
            print("Got a question: %s" % question)
            print("with answers: %s" % choices)


def main():

    ssl_context = ssl._create_unverified_context()
    try:
        service_instance = connect.SmartConnect(host=VMWARE_HOST,
                                                user=VMWARE_USER,
                                                pwd=VMWARE_PWD,
                                                port=VMWARE_PORT,
                                                sslContext=ssl_context)

        atexit.register(connect.Disconnect, service_instance)

        content = service_instance.RetrieveContent()

        container = content.rootFolder  # starting point to look into
        viewType = [vim.VirtualMachine]  # object types to look for
        recursive = True  # whether we should look into it recursively
        containerView = content.viewManager.CreateContainerView(
            container, viewType, recursive)

        vm_list = containerView.view
        print("Found VMs:")
        for vm in vm_list:
            summary = vm.summary
            print("Name       : ", summary.config.name)
            print("State      : ", summary.runtime.powerState)
            if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
                # VM already started
                raise ValueError("VM %s is already started.  Aborting cycle." % vm.name)

        random.shuffle(vm_list)
        # vm_list = vm_list[:7]
        while vm_list:
            print("Starting batch")
            crt_vm_list = vm_list[:VM_GROUP_SIZE]

            start_vm_batch(crt_vm_list)
            print("All VM from batch started successful")
            time.sleep(RUN_TIME)

            print("Shutdown batch")
            stop_vm_batch(crt_vm_list)
            print("All VM from batch shutdown successful")

            del vm_list[:VM_GROUP_SIZE]

            # cycle hotspot
            print("Restarting hotspot")
            restart_hotspot()

    except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)
        return -1

    return 0

# Start program
if __name__ == "__main__":
    main()
