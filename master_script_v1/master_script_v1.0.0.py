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
def website_search(nmap_report):
    #searches nmap reports for port 80 or http
    search_args = 'egrep "80/open|http" < ' + nmap_report
    #web_result is equal to the exit code of the egrep, if 0, then there is a website; if 1, then there is not.
    web_result = call(search_args, stdout=DEVNULL, shell=True)
    return web_result


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
http_host = list()
for client in hosts_dict:
    #searches nmap reports for websites
    nreport = work_dir + client['ip'] + '/' + 'nmap_results.txt'
    web_result = website_search(nreport)
    #if there is a website then it scrapes the website
    if web_result == 0:
        #adds host to http_host list
        http_host.append(client['ip'])
        #defines the directory that files will be read/written from
        host_dir = work_dir + client['ip'] + '/'
        http_location = host_dir + 'index.html'
        #downloads website, checks for urls and emails, then scrapes it for emails and urls, both are stored in seperate list
        webscrape.download_website(client['ip'], http_location)
        echeck = webscrape.email_check(http_location)
        if echeck == True:
            emails = webscrape.email_scrape(http_location)
            #saves the emails list to file in the report directory
            save_to_file(host_dir, 'emails.txt', emails)
        ucheck = webscrape.url_check(http_location)
        if ucheck == True:
            urls = webscrape.url_scrape(http_location)
            #saves the urls list to file in the report directory
            save_to_file(host_dir, 'urls.txt', urls)
print('[+] Websites stolen!')
###Ending statement###
print('[+] Script Complete! Reports area now avalible. Prepare to breach...')
