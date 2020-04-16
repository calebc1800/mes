#!/usr/bin/env python3

#This is the 'Master Sword' of enumeration scripts, attempting to combine host discovery, process discovery and report analysis within one script.
#Created by Caleb Chang

import resources.rootchk as rootchk
import resources.mac_changer as mac
import resources.network_scanner as netscan
import resources.web_scraper as webscrape
import argparse
from subprocess import call, Popen, check_output
from datetime import datetime
from os import devnull, path

#Global Script Variables
DEVNULL = open(devnull, 'w')

#functions
def get_agruments():
    #Allows cli option input
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', dest='directory', help='Destination directory for enumeration report ending with a /.')
    parser.add_argument('-t', '--target', dest='target', help='Target IP or IP subnet')
    options = parser.parse_args()
    #Forces -t and -d to be required
    if not options.directory:
        parser.error('[-] Please specify a directory for the report, use --help for more info.')
    if not options.target:
        parser.error('[-] Please specify an IP/IP subnet, use --help for more info.')
    #Checks if options.directory is exist
    dir_exist = path.isdir(options.directory)
    if dir_exist != True:
        parser.error('[-] The directory you entered does not exist. Please enter a valid directory.')
    return options
def mk_dir(location, dirname):
    #uses bash mkdir to create a new directory
    call(['mkdir', location + dirname])
def save_to_file(location, filename, array):
    #Opens a file and adds each array entry on a new line
    with open(location + filename, mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n'.join(array))
        myfile.write('\n')
def nmap_scan(ip_addr, report_name, wait):
    scan_args = ['nmap', '-T4', '-Pn', '-sV', '--version-intensity', '0', '-oG', report_name, ip_addr]
    p = Popen(scan_args)
    #If wait is equal to 0, then continue the script, else wait for nmap_scan to complete before continuing
    if wait == 0:
        return p
    else:
        p.wait()
def webserver_search(nmap_report):
    #searches nmap reports for an open port 80
    search_args = 'egrep "[0-9]{1,5}/open/tcp//http.*//" < ' + nmap_report
    #web_result is equal to the exit code of the egrep, if 0, then there is a website; if 1, then there is not.
    web_result = call(search_args, stdout=DEVNULL, shell=True)
    #now that we know whether there is a webserver, if there is we want to return the ip:mac of the webserver
    if web_result == 0:
        ip_args = 'egrep -o "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" < ' + nmap_report + ' | uniq'
        web_ip = check_output(ip_args, shell=True).decode("utf-8").rstrip('\n')
        mac_args = 'egrep -o "[0-9]{1,5}/open/tcp//http.*//" < ' + nmap_report + ' | cut -d "/" -f1'
        web_port = check_output(mac_args, shell=True).decode("utf-8").rstrip('\n')
        webserver = str(True)
        return webserver, web_ip, web_port
    else:
        #Fill variables with empty data
        webserver = str(False)
        web_ip = 0
        web_port = 0
        return webserver, web_ip, web_port


###Operation Start###
rootchk.check()
options = get_agruments()
#Creates reporting directory with current date
start_time = datetime.now().strftime('%Y-%m-%d-%H:%M')
mk_dir(options.directory, 'master_report-' + start_time)
work_dir = options.directory + 'master_report-' + start_time + '/'
print('[+] Report directory created as ' + work_dir)
##Network scan which saves as a variable and in a file in the reporting directory
hosts_dict = netscan.scan(options.target)
hosts_list = list()
for client in hosts_dict:
    hosts_list.append(client['ip'] + '\t' + client['mac'])
save_to_file(work_dir, 'hosts_report', hosts_list)
#Checks to make sure that there are targets to scan... If not, then will exit script
hosts_exist = bool(hosts_dict)
if hosts_exist != True:
    print('[-] ERROR: No targets were found')
    print('[+] Deleting report directory')
    call(['rm', '-r', work_dir])
    print('[+] Exiting Script...')
    exit(1)
#Created directory for each host found
for client in hosts_dict:
    mk_dir(work_dir, client['ip'])
print('[+] There are ' + str(len(hosts_list)) + ' target(s) online')
##nmap scan
#initialize process list to keep track of subprocesses
ps = list()
for client in hosts_dict:
    #run nmap_scan as a subprocess and continue script.
    nmap_location = work_dir + client['ip'] + '/' + 'nmap_results.txt'
    p = nmap_scan(client['ip'], nmap_location, 0)
    #Adds the process to list
    ps.append(p)
#waits for each subprocess to complete before continuing script
for p in ps:
    p.wait()
print('[+] Detailed scan complete!')
##website scrapper
#initializes list of http_host for future use
http_list = list()
ecount = 0
ucount = 0
for client in hosts_dict:
    #searches nmap reports for webservers and saves them as dictionaries in list
    nreport = work_dir + client['ip'] + '/' + 'nmap_results.txt'
    web_result, web_ip, web_port = webserver_search(nreport)
    if web_result == str(True):
        http_host = {'ip': web_ip, 'port': web_port}
        http_list.append(http_host)
#scrapes websites from http_host
for server in http_list:
    #defines exact ip+port address
    webserver = str(server['ip']) + ':' + str(server['port'])
    #defines the directory that files will be read from/written to
    host_dir = work_dir + str(server['ip']) + '/'
    http_location = host_dir + server['port'] + '_index.html'
    #downloads website, checks for urls and emails, then scrapes it for emails and urls, both are stored in seperate list
    webscrape.download_website(webserver, http_location)
    echeck = webscrape.email_check(http_location)
    if echeck == True:
        emails = webscrape.email_scrape(http_location)
        #adds amount of emails to total email count
        ecount = ecount + len(emails)
        #saves the emails list to file in the report directory
        save_to_file(host_dir, 'emails.txt', emails)
    ucheck = webscrape.url_check(http_location)
    if ucheck == True:
        urls = webscrape.url_scrape(http_location)
        #adds amount of urls to total url count
        ucount = ucount + len(urls)
        #saves the urls list to file in the report directory
        save_to_file(host_dir, 'urls.txt', urls)
print('[+] Script found ' + str(len(http_list)) + ' webservers. \nThese websites contain a total of:')
print(str(ecount) + ' unique emails \n' + str(ucount) + ' unique urls')
###Ending statement###
print('[+] Script Complete! Reports are now avalible. Prepare to breach...')
exit(0)