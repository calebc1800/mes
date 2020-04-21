# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
- Full custom errors
- nmap scan selection
- Optional interactive cli
- nmap export as all file types and use .xml for filtering
- Change webscraper to a subprocess so that it runs faster
- Include a ping sweep so that all targets are found
- Optional mac changer
- Make host discovery optional

## [1.1.1] - 2020-04-21
### Added
- Progress bar for nmap scan
- Webserver ips and ports are now saved in a file in the main report directory

### Changed
- nmap scan now does not send info to console

## [1.1.0] - 2020-04-16
### Changed
- Web scraper now can identify which port webservers are hosted on and will correctly grab the website from that port
- Web server ips and ports are now stored as dictionary entries
- Changed some print statements to fix grammar and spelling

## [1.0.1] - 2020-04-10
### Changed
- Cleaned up script overall
- Replaced web scrapper output with a more informative output
- Renamed website_search as webserver_search to clarify and correct diction
- Adjusted regex for webserver_search to only include webservers hosted on the default port 80

## [1.0.0] - 2020-04-08
### Added
- Initial commitment, script works but has security issues and needs to be cleaned up
- Arp network scan
- Report directory creation
- Created resources directory and dependencies
- nmap scan
- Integrated webscrapper
