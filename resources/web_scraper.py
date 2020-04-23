#!/usr/bin/env python3

#Written by Blackfire

import subprocess
import argparse
import re
from os import devnull

#Scraper that allows scraping for emails or urls on a target webpage
#Written by Blackfire

def get_arguments():
    #Allows cli option input
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file-name", dest="file_name", help="Destination file for wget")
    parser.add_argument("-t", "--target", dest="target", help="Target website for scrape")
    parser.add_argument("-e", "--email", dest="email", action="store_true", help="Scrape target for emails")
    parser.add_argument("-u", "--url", dest="url", action="store_true", help="Scrape target for urls")
    options = parser.parse_args()
    #Forces -t and -f to be required
    if not options.target:
        parser.error("[-] Please specify a target to scan, use --help for more info.")
    if not options.file_name:
        parser.error("[-] Please specify a destination file, use --help for more info.")
    #Requires either -e or -u to scrape for emails or urls
    if not options.email and not options.url:
        parser.error("[-] Please specify either -e and/or -u, use --help for more info.")
    return options

def download_website(target, file_name):
    #Uses linux wget to download website to the target location and returns html page.
    subprocess.call(["wget", "-qO", file_name, target])
    website = subprocess.check_output(["cat", file_name]).decode("utf-8")
    return website

def cleanup(file_name):
    #Removes file_name so that scan results are only printed by print_result
    subprocess.call(["rm", file_name])

def email_scrape(html_file):
    #Searches for all unique emails of target webpage and returns them as a list
    website = subprocess.check_output(["cat", html_file]).decode("utf-8")
    emails = list(set(re.findall(r"\w+\.?\w+\@\w+\.\w{2,3}", website)))
    emails = list(filter(None, emails))
    emails.sort()
    return emails

def url_scrape(html_file):
    #Searches for all unique urls of target webpage and returns them as a list
    unorganized_urls = subprocess.check_output("cat " + html_file + " | grep \"href=\" | cut -d" + "\'" + "\"" + "\'" + " -f2 | uniq -u | egrep \"^http?|^\/\"", shell=True).decode("utf-8")
    urls = list(set(unorganized_urls.split("\n")))
    urls = list(filter(None, urls))
    urls.sort()
    return urls

def print_results(scrape_results, list_name):
    #Prints results of a list
    print(" " * 12 + list_name + "\n" + "-" * 30)
    print(*scrape_results, sep="\n")
    print("")

def url_check(html_file):
    #Checks html_file to see if it has any urls and return a 0 if there is and 1 if there is not.
    ulist = subprocess.call("cat " + html_file + " | grep \"href=\" | cut -d" + "\'" + "\"" + "\'" + " -f2 | uniq -u | egrep \"^http?|^\/\"", shell=True, stdout=open(devnull, 'w'))
    if ulist == 0:
        check = True
    else:
        check = False
    return check

def email_check(html_file):
    #Checks html_file to see if it has any urls and return a 0 if there is and 1 if there is not.
    website = subprocess.check_output(["cat", html_file]).decode("utf-8")
    elist = re.findall(r"\w+\.?\w+\@\w+\.\w{2,3}", website)
    check = bool(elist)
    return check


###Beginning of Operation###
if __name__ == '__main__':
    options = get_arguments()
    website = download_website(options.target, options.file_name)
    #Captures emails if -e was used
    if options.email == True:
        emails = email_scrape(options.file_name)
        print_results(emails, "emails")
    #Captures urls if -u was used
    if options.url == True:
        urls = url_scrape(options.file_name)
        print_results(urls, "urls")
    cleanup(options.file_name)