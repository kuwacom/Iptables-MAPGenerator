def generate_iptables_rules(start_port=10010, end_port=13000, base_ip=[172, 23, 0]):
    rules = []
    current_ip_octet = 10
    current_port = start_port

    while current_port <= end_port:
        if current_ip_octet > 254:
            # 再帰でipをずらす
            return "\n".join(rules) + "\n" + generate_iptables_rules(start_port=current_port, end_port=end_port, base_ip=[base_ip[0], base_ip[1], base_ip[2] + 1])
            # raise ValueError("IP octet exceeded 254")

        rules.append(f"###\n## ssh")
        rules.append(f"-A PREROUTING -i wg0 -p tcp -m tcp --dport {current_port} -j DNAT --to-destination {".".join(map(str, base_ip))}.{current_ip_octet}:22")
        
        tcp_start = current_port + 1
        tcp_end = tcp_start + 8
        if tcp_end > end_port:
            tcp_end = end_port

        rules.append(f"## tcp")
        rules.append(f"-A PREROUTING -i wg0 -p tcp -m tcp --dport {tcp_start}:{tcp_end} -j DNAT --to-destination {".".join(map(str, base_ip))}.{current_ip_octet}:{tcp_start}-{tcp_end}")

        udp_start = current_port
        udp_end = udp_start + 9
        if udp_end > end_port:
            udp_end = end_port

        rules.append(f"## udp")
        rules.append(f"-A PREROUTING -i wg0 -p udp -m udp --dport {udp_start}:{udp_end} -j DNAT --to-destination {".".join(map(str, base_ip))}.{current_ip_octet}:{udp_start}-{udp_end}")

        current_port = udp_end + 1
        current_ip_octet += 10

    return "\n".join(rules)

# 172.23.0.0/16 へ 10010 - 13000 の範囲でプロットする場合
iptables_rules = generate_iptables_rules(start_port=10010, end_port=11000, base_ip=[172, 23, 0])
print(iptables_rules)
