# EOS SDK PBR Monitor Agent

The purpose of this SDK Agent is to monitor the reachability of an IP address and if it fails to respond, remove it from the Nexthop Group configuration of a PBR Policy. Once failed, it will continue to monitor the IP.  If it begins to respond again, it will re-add the IP to the Nexthop Group.

## Switch Setup
### Install
1. Copy `PbrMon-x.x.x-x.swix` to `/mnt/flash/` on the switch or to the `flash:` directory.
2. Copy and install he `.swix` file to the extensions directory from within EOS.  Below command output shows the copy and install process for the extension.
```
Fill in show daemon output later
```
3. In order for the extension to be installed on-boot, enter the following command:
```
copy extensions: boot-extensions
```

### IP Monitor Agent Configuration
1. In EOS config mode perform the following commands for basic functionality (see step #4 for further customization):
```
config
   daemon PbrMon
      exec /usr/bin/PbrMon
      no shutdown
```
2. By default, the agent has the following default values in terms of polling:
- Polling interval = 5 seconds
- Trigger threshold = 2 consecutive failed attempts
- VRF = default (VRF used on the switch by default)
- Source Interface = Egress Interface of Ping

To modify the default behavior, use the following commands to override the defaults:
```
config
   daemon PbrMon
      option poll value {time_in_seconds}
      option threshold value {number_of_failures}
      option vrf value {vrf_name}
      option source value {source_intf}
```
**`time_in_seconds` **(optional)** how much time the agent should wait until it tries to poll the IP addresses*

***`number_of_failures` **(optional)** how many failures should occur consecutively before an action is triggered*

*****`vrf_name` **(optional)** the name of the VRF that the pings should originate from (VRF name is case-sensitive)*

******`source_intf` **(optional)** interface to source ping from. ie `et44, et49_1, ma1, vlan100` See conversion list below for interface mappings*

##### Interface Mappings
- et44 --> Ethernet44
- et49_1 --> Ethernet49/1
- ma1 --> Management1
- vlan100 --> Vlan100

3. In order for this agent to monitor IP addresses, the following commands will need to be taken:
```
config
   daemon PbrMon
      option {device_name} value {ip_of_device}
```
**`device_name` needs to be a unique identifier for each remote host*

**`ip_of_device` needs to be a valid IPv4 address for the remote device for monitoring*

***To see what unique peer identifiers have been created, enter `show daemon PbrMon`*

4. Finally, the name of the Nexthop Group that will be modified in the event of a trigger needs to be added with the following commands:
```
config
   daemon PbrMon
      option nhg value {nhg_name}
```
**`nhg_name` The name of the nexthop-group in the config that will be modified*

Example of a full `daemon PbrMon` config would look like with all parameters specified
```
daemon PbrMon
   option proxy-01 value 192.168.50.16
   option proxy-02 value 192.168.50.17
   option nhg value PROXIES
   option poll value 15
   option threshold value 5
   option vrf value INTERNET
   option source value vlan100
   no shutdown
```

#### Sample output of `show daemon PbrMon`
```
Fill in show output later
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