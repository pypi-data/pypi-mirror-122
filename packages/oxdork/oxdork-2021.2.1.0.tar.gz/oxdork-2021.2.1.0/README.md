![Screenshot_20210827-111909-removebg-preview](https://user-images.githubusercontent.com/74001397/131107876-db415339-0c1d-4876-8665-fe9b76c4518c.png)

![Python Version](https://img.shields.io/badge/python-3.x-blue?style=flat&logo=python)
![OS](https://img.shields.io/badge/OS-GNU%2FLinux-red?style=flat&logo=linux)
![GitHub](https://img.shields.io/github/license/rlyonheart/oxdork?ystyle=flat)
![CodeFactor](https://www.codefactor.io/repository/github/rlyonheart/oxdork/badge)
![Snyk Vulnerabilities for GitHub Repo](https://img.shields.io/snyk/vulnerabilities/github/rlyonheart/oxdork)
![Lines of code](https://img.shields.io/tokei/lines/github/rlyonheart/oxdork)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/rlyonheart/oxdork?include_prereleases)
![GitHub repo size](https://img.shields.io/github/repo-size/rlyonheart/oxdork)

 # Google dorking
 Google hacking, also named Google dorking, is a hacker technique that uses Google Search and other Google applications to find security holes in the configuration and computer code that websites are using. Google dorking could also be used for OSINT(Open Source Intelligence).
 

 **o𝐱𝐝𝐨𝐫𝐤** *uses Google dorking techniques and Google dorks to find security holes and misconfigurations in web servers*.


# Basic dorks

| Dork         | Usage     | Example |
| ------------- |:---------:|:-------:|
| <code>allintext:</code> | *finds all specified terms in the title of a page* |  **allintext:passwords** |
| <code>inurl:</code> | *finds a specified string in the url of a page*      |   **inurl:index.php?id=1** |
| <code>site:</code> |  *locks a search on a specified site or domain*  |  **site:example.com**  |
| <code>intitle:</code> |  *finds a specified strings in the title of a page* |  **intitle:"your text here"** |
| <code>link:</code> | *searches for all links to a specified site or domain* | **link:example.com** |
| <code>cache:</code> | *returns Google's cached copy of a specified url page* | **cache:www.example.com** |
| <code>info:</code> | *returns summary information about a specified url* | **info:https://example.com** |



# Installation & Usage
**Clone from Github**:
> <code>$ git clone https://github.com/rlyonheart/oxdork.git</code>

> <code>$ cd oxdork/oxdork</code>

> <code>$ python oxdork</code>

**example**:
> <code>$ python oxdork -v intext:cybersecurity</code>

**Or Install from pypi**:
> <code>$ pip install oxdork</code>

> <code>$ oxdork</code>

**example**:
> <code>$ oxdork -v intext:cybersecurity</code>



# Optional Arguments

| Flag           | Or            |MetaVar|                 Usage|
| ------------- |:-------------:|:----------------------:|:---------:|
| <code>-c</code>           | <code>--count</code>    | **NUMBER** |  *number of dork results to return (default is 50)* |
| <code>-o</code>      | <code>--outfile</code>      |   **FILENAME** |  *output filename*  |
| <code>-v</code>      | <code>--verbose</code>      |    |  *run program in verbose mode*  |



# Notes:
* *Use VPN for better experience.*

* *If search query contains spaces, it should be put inside quote* **" "** *symbols.*

* *Sending more than 5 requests in less than 5 minutes will return a 429 error code. That is why using VPN is recommemded.*


# Queries:
A collection of 5,568 common dork queries [here](https://github.com/rlyonheart/oxdork/tree/master/dork_queries)

  
*by* [Richard Mwewa](https://about.me/rlyonheart)