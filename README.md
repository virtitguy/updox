Install ELK Stack Instructions:

This covers the use of the setup-elasticsearch-env.yml playbook.

Playbooks
=========

There are two playbooks. The first one, buildenv.yml is used to build and tear down containers in my LXC cluster. It is somewhat propreatiary. If you don't have an environment that looks like my lab, it wont work.

The second playbook, setup-elasticsearch-env.yml, will install elasticsearch, kibana, nginx. It also will install filebeat on every host in the ansible groups referrenced and beconfigured to submit /var/log/messages and /var/log/syslog. The playbook is backed by roles in for functionality and ease of maintainance.

Requirements
------------

The playbook and roles were developed against Ubuntu Bionic Beaver hosts. While they might work on variants, it is not certain nor tested. 

Playbook Variables
--------------

All variables are in the playbook group_vars/all.yml file. They are as follows:

is_new_cluster: true <-- set to new for a fresh deployment. The playbook will change it afterwards.
env_nameserver: 192.168.2.1 <-- needed for my home lab
elasticsearch_cluster_name: updox <-- the name of the elasticsearch cluster you are deploying>
elasticsearch_http_port: 9200 <-- The port you want elasticsearch http_transport on
elasticsearch_transport_port: 9300 <-- The port you want elasticsearch ssl_transport on
kibana_port: 5601 <-- The port you want Kibana to run on
nginx_http_port: 80 <-- nginx http port
nginx_https_port: 443 <-- nginx https port
Xms_memory_amount: 512m <-- Java setting for elasticsearch, look at jvm.options Xms and Xmx in the manual
Xmx_memory_amount: 512m <-- Java setting for elasticsearch, look at jvm.options Xms and Xmx in the manual
cluster_join_async_seconds: 600 <-- How long to wait for the cluster to form
cluster_join_poll_seconds: 10 <-- how often to check for cluster formation
master_node: "{{groups['elasticsearch'][0]}}" <-- This is the master Elasticsearch node name, it will set it'self
elasticsearch_certutil: /usr/share/elasticsearch/bin/elasticsearch-certutil <-- path to certutil utility
es_certs_dir: /etc/elasticsearch/certs <-- path to certs dir
install_deps: <-- Dependencies to install on all hosts
  - apt-utils
  - curl
  - wget
  - iptables
  - iptables-persistent

Dependencies
------------

To deploy a new cluster, first create the groups in the ansible hosts file:

The first group should use the same name as the Elasitcsearch cluster name and list all of the hosts to be installed in the env. This includes Elasticsearch, kibana, and nginx hosts.
The other groups are elasticsearch, kibana and nginx.

The hostnames can be anything you want but the group names (elasticsearch, kibana and nginx) must be those names.
Example ansible hosts file:

[updox] 
els1
els2
els3
kib1
kib2
ngnx1
ngnx2
[elasticsearch]
els1
els2
els3
[kibana]
kib1
kib2
[nginx]
ngnx1
ngnx2

Example Playbook Use
----------------

Under normal cercumstances, you should only have to run:

ansible-playbook setup-elasticsearch-env.yml

You may restart the elasticsearch cluster with:

ansible-playbook setup-elasticsearch-env.yml --limit elasticsearch -t restart_elasticsearch

You may restart an individual elasticsearch host with:

ansible-playbook setup-elasticsearch-env.yml --limit els1 -t restart_elasticsearch

To reconfigure the ES cluster nodes, make changes in templates/elasticsearch.yml.j2, then run:

ansible-playbook setup-elasticsearch-env.yml --limit elasticsearch -t write_elasticsearch_yml

followed by:

ansible-playbook setup-elasticsearch-env.yml --limit elasticsearch -t restart_elasticsearch

Kibana:

You may restart the Kibana service on all kibana hosts with:

ansible-playbook setup-elasticsearch-env.yml --limit kibana -t restart_kibana

or a single host with

ansible-playbook setup-elasticsearch-env.yml --limit <kibana host name> -t restart_kibana

Filebeat:

You may restart the filebeat service on all hosts with:

ansible-playbook setup-elasticsearch-env.yml --limit <elasticsearch_cluster_name> -t restart_filebeat

or a single host with

ansible-playbook setup-elasticsearch-env.yml --limit <host name> -t restart_filebeat

Nginx:

You may restart the nginx service on all hosts with:

ansible-playbook setup-elasticsearch-env.yml --limit nginx -t restart_nginx

or a single host with

ansible-playbook setup-elasticsearch-env.yml --limit <host name> -t restart_nginx

ENV WIDE:

You may reconfigure the IPtables FW by editting the iptables-rules.v4.j2 file and running:

ansible-playbook setup-elasticsearch-env.yml --limit <GROUP OR HOST> -t fw_rules


License
-------

BSD

Author Information
------------------
Created by Craig Cowen for the Updox pre-employment challenge.