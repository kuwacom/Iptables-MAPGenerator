def generateIptablesRules(inputInterface="eth0", currentIpOctet=1, ipRange=1, portRange=10, startPort=10010, endPort=13000, baseIp=[172, 16, 0]):
    rules = []
    currentPort = startPort

    while currentPort <= endPort:
        if currentIpOctet > 254:
            # 再帰でipをずらす
            return '\n'.join(rules) + '\n' + generateIptablesRules(startPort=currentPort, endPort=endPort, baseIp=[baseIp[0], baseIp[1], baseIp[2] + 1])
            # raise ValueError("IP octet exceeded 254")

        rules.append(f'###')
        rules.append(f'## ssh')
        rules.append(f'-A PREROUTING -i {inputInterface} -p tcp -m tcp --dport {currentPort} -j DNAT --to-destination {".".join(map(str, baseIp))}.{currentIpOctet}:22')
        
        tcpStart = currentPort + 1
        tcpEnd = tcpStart + (portRange - 2)
        if tcpEnd > endPort: # portの範囲外の場合、指定されている最終portへする
            tcpEnd = endPort

        rules.append(f'## tcp')
        rules.append(f'-A PREROUTING -i {inputInterface} -p tcp -m tcp --dport {tcpStart}:{tcpEnd} -j DNAT --to-destination {".".join(map(str, baseIp))}.{currentIpOctet}:{tcpStart}-{tcpEnd}')

        udpStart = currentPort
        udpEnd = udpStart + (portRange - 1)
        if udpEnd > endPort: # portの範囲外の場合、指定されている最終portへする
            udpEnd = endPort

        rules.append(f'## udp')
        rules.append(f'-A PREROUTING -i {inputInterface} -p udp -m udp --dport {udpStart}:{udpEnd} -j DNAT --to-destination {".".join(map(str, baseIp))}.{currentIpOctet}:{udpStart}-{udpEnd}')

        currentPort = udpEnd + 1
        currentIpOctet += ipRange

        # 式は違うが udpEnd と tcpPort はおなじ

    return "\n".join(rules)

# 172.23.0.0/16 へ 10000 - 13000 の範囲で 172.23.0.1 から1飛ばしで10portずつプロットする場合
# currentIpOctet スタートするIP
# ipRange 何個飛ばしでIP指定するか
# portRange IPあたり何個のポートを指定するか
iptablesRules = generateIptablesRules(currentIpOctet=1, ipRange=1, portRange=10, startPort=10000, endPort=13000, baseIp=[172, 23, 0])
print(iptablesRules)
