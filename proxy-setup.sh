######################################################################
## Setup steps for bict proxy 1, a hardened nginx reverse proxy.    ##
## Author: Manuel Riesen, Sandro Rüfenacht                          ##
######################################################################
echo "Do not run this script! Read the description of each step and apply the commands manually."
exit 1


##
##  1.0: basic software installation
##

# update and upgrade system
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get autoremove
sudo apt-get autoclean

# install nginx
sudo apt-get install nginx

# install net-tools
sudo apt-get install net-tools

##
##  1.1: remove unused packages
##
sudo apt autoremove --purge snapd
sudo apt-get --purge remove xinetd nis yp-tools tftpd atftpd tftpd-hpa telnetd rsh-server rsh-redone-server

##
##  1.2: disable root account
##
sudo passwd -l root

##
##  1.3: secure shared memory
##

# edit fstab
sudo nano /etc/fstab

# add this line
:'
tmpfs     /run/shm    tmpfs	defaults,noexec,nosuid	0	0
'

# apply changes
sudo mount -a

##
##  2.0: setup unattended upgrades
##

# install package
sudo apt-get install unattended-upgrades

# NOTE: unattended-upgrades is automatically configured for only installing security-related updates.

# configure for all updates, uncomment ...-updates";
sudo nano /etc/apt/apt.conf.d/50unattended-upgrades
:'
Unattended-Upgrade::Allowed-Origins {
        "${distro_id}:${distro_codename}";
        "${distro_id}:${distro_codename}-security";
        // Extended Security Maintenance; doesnt necessarily exist for
        // every release and this system may not have it installed, but if
        // available, the policy for updates is such that unattended-upgrades
        // should also install from here by default.
        "${distro_id}ESMApps:${distro_codename}-apps-security";
        "${distro_id}ESM:${distro_codename}-infra-security";
        "${distro_id}:${distro_codename}-updates";
//      "${distro_id}:${distro_codename}-proposed";
//      "${distro_id}:${distro_codename}-backports";
};
'

##
##  3.0: install and configure ufw
##

# install package
sudo apt-get install ufw

# disable IPv6
sudo nano /etc/default/ufw
:'
IPV6=no
'

# set default rules
sudo ufw default deny incoming
sudo ufw default deny outgoing

# set rules for outgoing requests
sudo ufw allow out 53/tcp
sudo ufw allow out 53/udp
sudo ufw allow out 443/tcp
sudo ufw allow out 80/tcp
sudo ufw allow out 21/tcp
sudo ufw allow out 22/tcp
sudo ufw allow out 25/tcp

# set rules for nginx proxy
sudo ufw allow in 80/tcp
sudo ufw allow in 443/tcp

# enable ufw
sudo ufw enable

##
##  4.0: configure AppArmor
##

# install profiles
sudo apt-get install apparmor-profiles

# install utils
sudo apt-get install apparmor-utils


# get status
sudo apparmor_status

# go to config directory
cd /etc/apparmor.d/

# create nginx config
sudo aa-autodep nginx

# set complain profile
sudo aa-complain nginx

# restart nginx
sudo service nginx restart

# show logs
sudo aa-logprof

# allow all needed restrictions and save profile

# edit profile
sudo nano /etc/apparmor.d/usr.sbin.nginx
:'
#include <tunables/global>

/usr/sbin/nginx {
  #include <abstractions/base>
  #include <abstractions/nameservice>
  #include <abstractions/openssl>
  #include <abstractions/nis>

  capability dac_override,
  capability dac_read_search,
  capability net_bind_service,

  /usr/sbin/nginx mr,
  /var/log/nginx/error.log w,
  /etc/group r,
  /etc/nginx/conf.d/ r,
  /etc/nginx/mime.types r,
  /etc/nginx/nginx.conf r,
  /etc/nsswitch.conf r,
  /etc/passwd r,
  /etc/ssl/openssl.cnf r,
  /run/nginx.pid rw,
  /usr/sbin/nginx mr,
  /var/log/nginx/access.log w,
  /var/log/nginx/error.log w,
  owner /etc/nginx/conf.d/ r,
  owner /etc/nginx/mime.types r,
  owner /etc/nginx/modules-enabled/ r,
  owner /etc/nginx/nginx.conf r,
  owner /etc/nginx/sites-available/ r,
  owner /etc/nginx/sites-enabled/ r,
  owner /run/nginx.pid rw,
  owner /usr/share/nginx/modules-available/mod-http-image-filter.conf r,
  owner /usr/share/nginx/modules-available/mod-http-xslt-filter.conf r,
  owner /usr/share/nginx/modules-available/mod-mail.conf r,
  owner /usr/share/nginx/modules-available/mod-stream.conf r,
}
'

# enforce profile
sudo aa-enforce nginx

# restart nginx
sudo service nginx restart

# reload daemon
sudo /etc/init.d/apparmor reload

# check status
sudo apparmor_status

##
##  5.0: setup fail2ban
##

# install fail2ban
sudo apt-get install fail2ban

# copy file
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# edit jail
sudo nano /etc/fail2ban/jail.local
:'
[nginx-http-auth]

enabled = true
port    = http,https
logpath = %(nginx_error_log)s

...

[nginx-badbots]

enabled  = true
port     = http,https
filter   = nginx-badbots
logpath  = /var/log/nginx/access.log
maxretry = 2

[nginx-nohome]

enabled  = true
port     = http,https
filter   = nginx-nohome
logpath  = /var/log/nginx/access.log
maxretry = 2
'

# create configurations

# copy badbots config
sudo cp /etc/fail2ban/filter.d/apache-badbots.conf /etc/fail2ban/filter.d/nginx-badbots.conf


sudo nano /etc/fail2ban/filter.d/nginx-nohome.conf
:'
[Definition]

failregex = ^<HOST> -.*GET .*/~.*

ignoreregex =
'

# restart fail2ban
sudo service fail2ban restart

# check status
sudo fail2ban-client status

##
## 6.0: kernel hardening
##

sudo nano /etc/sysctl.conf

:'
# Turn on execshield
kernel.exec-shield=1
kernel.randomize_va_space=1
# Enable IP spoofing protection
net.ipv4.conf.all.rp_filter=1
# Disable IP source routing
net.ipv4.conf.all.accept_source_route=0
# Ignoring broadcasts request
net.ipv4.icmp_echo_ignore_broadcasts=1
net.ipv4.icmp_ignore_bogus_error_messages=1
# Make sure spoofed packets get logged
net.ipv4.conf.all.log_martians = 1
'

# reboot system
sudo shutdown -r now


##
##  7.0: setup rootkit hunter
##

# install rkhunter
sudo apt-get install rkhunter

# run rkhunter
sudo rkhunter --check


##
##  8.0 OPTIONAL: use lynis to check for vulnerabilities
##


##
##  9.0: setup nginx reverse-proxy
##

# the following config files have been copied from 30.5:
# - /etc/nginx/sites-available/cloud.bict.ch
# - /etc/nginx/sites-available/dev.bict.ch
# - /etc/nginx/sites-available/env.bict.ch
# - /etc/nginx/sites-available/gitlab.bict.ch
# - /etc/nginx/sites-available/ipa.bict.ch
# - /etc/nginx/sites-available/registry.bict.ch
# all certbot-related configs have been removed

# enable sites
sudo ln -s /etc/nginx/sites-available/{cloud,dev,env,gitlab,ipa,registry}.bict.ch /etc/nginx/sites-enabled/

##
##  10.0: setup nginx https
##

# install certbot
sudo apt-get install certbot 

# install nginx plugin certbot 
sudo apt-get install python3-certbot-nginx 

# generate first certificate 
sudo certbot --authenticator standalone --installer nginx --pre-hook "service nginx stop" --post-hook "service nginx start" 

# check renewal
sudo certbot renew --dry-run

