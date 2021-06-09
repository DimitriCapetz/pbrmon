# EOS SDK PBR Monitor Agent

The purpose of this utility is to test ICMP ping reachability, alert if its down and
run a config change to remove the failed host from a Nexthop-Group. On recovery run 
a change to put the recovered host back in the Nexthop-Group.

## Switch Setup
### Install
1. Copy `PbrMon-x.x.x-x.swix` to `/mnt/flash/` on the switch or to the `flash:` directory.
2. Copy and install he `.swix` file to the extensions directory from within EOS.  Below command output shows the copy and install process for the extension.
```
copy flash:PbrMon-x.x.x-x.swix extension:
extension PbrMon-x.x.x-x.swix
```
3. In order for the extension to be installed on-boot, enter the following command:
```
copy installed-extensions boot-extensions
```

### IP Monitor Agent Configuration
1. In EOS config mode perform the following commands for basic functionality (see step #4 for further customization):
```
daemon PbrMon
   exec /usr/local/bin/PbrMon
   option CHECKINTERVAL value 5
   option NHG_BASE value /mnt/flash/nhg.conf
   option PINGCOUNT value 2
   option PINGTIMEOUT value 2
   option HOLDDOWN value 0
   option HOLDUP value 0
   option VRF value mgmt
   option IPv4 value 10.1.1.1,10.1.2.1,10.1.2.2,10.1.3.1
   option NHG value PROXIES
   option SOURCE value et1
   no shutdown
```

**CHECKINTERVAL** is the time in seconds to check hosts. Default is 5 seconds.

**IPv4** is the address(s) to check. Mandatory parameter. Multiple addresses are comma separated

**NHG** is the name of the Nexthop-Group for the PBR Policy.

**NHG_BASE** is the base config file for the Nexthop-Group when all hosts are up. Mandatory parameter.

**PINGCOUNT** is the number of ICMP Ping Request messages to send. Default is 2.

**HOLDDOWN** is the number of iterations to wait before declaring all hosts up. Default is 0 which means take immediate action.

**HOLDUP** is the number of iterations to wait before declaring all hosts down. Default is 0 which means take immediate action.

**VRF** is the VRF name to use to generate the ICMP pings. If the default is used, then just leave blank and it will use the default VRF.

**SOURCE** is the source interface (as instantiated to the kernel) to generate the pings fromself. This is optional. Default is to use RIB/FIB route to determine which interface to use as sourceself.

**PINGTIMEOUT** is the ICMP ping timeout in seconds. Default value is 2 seconds.


2. Create a file in flash for reference. The NHG_BASE file is just a list of commands that define the steady-state entries of the Nexthop-Group. These commands must be FULL commands just as if you were configuration the switch from the CLI.

For example the above referenced /mnt/flash/nhg.conf file could include the following commands:

```
entry 0 nexthop 10.1.1.1
entry 1 nexthop 10.1.2.1
entry 1 nexthop 10.1.2.2
entry 3 nexthop 10.1.3.1
```
#### Sample output of `show daemon PbrMon`
```
Agent: PbrMon (running with PID 4500)
Uptime: 0:19:16 (Start time: Wed Jun 09 13:53:33 2021)
Configuration:
Option              Value
------------------- ---------------------------------------
CHECKINTERVAL       2
HOLDDOWN            10
HOLDUP              0
IPv4                100.1.3.5,100.1.3.6,100.1.3.7,100.1.3.8
NHG                 PROXIES
NHG_BASE            /mnt/flash/nhg.conf
PINGCOUNT           2
PINGTIMEOUT         2

Status:
Data                  Value
--------------------- ---------------------------------------
100.1.3.5:            UP
100.1.3.6:            UP
100.1.3.7:            DOWN
100.1.3.8:            UP
CHECKINTERVAL:        2
HOLDDOWN:             10
HOLDUP:               0
Health Status:        HOSTS DOWN
IPv4 Ping List:       100.1.3.5,100.1.3.6,100.1.3.7,100.1.3.8
NHG_BASE:             /mnt/flash/nhg.conf
Nexthop-Group:        PROXIES
PINGCOUNT:            2
PINGTIMEOUT:          2
Status:               Administratively Up
```

#### Signs of an Error
In the below log output, a tell-tale sign that there is an error are repeated `PBRMON Agent Initialized` logs:
```
Sep 28 11:33:25 veos-rtr-01 myIP-MON: %AGENT-6-INITIALIZED: Agent 'PbrMon-PbrMon' initialized; pid=14232
Sep 28 11:33:25 veos-rtr-01 myIP-MON: %myIP-6-LOG: PBRMON Agent Initialized
Sep 28 11:33:27 veos-rtr-01 myIP-MON: %AGENT-6-INITIALIZED: Agent 'PbrMon-PbrMon' initialized; pid=14246
Sep 28 11:33:27 veos-rtr-01 myIP-MON: %myIP-6-LOG: PBRMON Agent Initialized
Sep 28 11:33:31 veos-rtr-01 myIP-MON: %AGENT-6-INITIALIZED: Agent 'PbrMon-PbrMon' initialized; pid=14262
Sep 28 11:33:31 veos-rtr-01 myIP-MON: %myIP-6-LOG: PBRMON Agent Initialized
Sep 28 11:33:34 veos-rtr-01 myIP-MON: %AGENT-6-INITIALIZED: Agent 'PbrMon-PbrMon' initialized; pid=14278
Sep 28 11:33:34 veos-rtr-01 myIP-MON: %myIP-6-LOG: PBRMON Agent Initialized
```

If this occurs, check to make sure any optional configuration parameters are correct.