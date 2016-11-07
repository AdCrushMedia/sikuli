# sikuli


## vm_open.py

Python script that will automatically open virtual machines from a computer in VMWare Workstation 12. Here are the more
detailed specifics of what the script should do:

- Opening 5 virtual machines randomly from the total pool of all virtual machines in VMWare Workstation 12, with a short interval of 1-60 seconds between opening each of these 5 virtual machines
- Waiting 15 minutes then closing all 5 of the opened virtual machines
- Restart Verizon hotspot via http://my.jetpack
- Opening 5 new randomly selected virtual machines and repeating the process from the beginning
- Continuing to do these steps until every virtual machine in VMWare Workstation 12 has been accessed, each virtual machine having only been opened and closed one time
