Requirements
============

To replicate the steps demonstrated in this tutorial, you will need:

  * Linux, FreeBSD, or OS X
  * `Vagrant`_ (1.6.2 or newer)
  * `VirtualBox`_
  * The OpenSSH client (the ``ssh``, ``ssh-agent``, and ``ssh-add`` command-line programs)
  * bash
  * The ``mongo`` MongoDB interactive shell

You will also need ``flocker-cli`` installed (providing the ``flocker-deploy`` command).

Setup
=====

Before you can deploy anything with Flocker you'll need a node onto which to deploy it.
To make this easier, this tutorial uses `Vagrant`_ to create two VirtualBox VMs.
These VMs serve as hosts on which Flocker can run Docker.
Flocker does not require Vagrant or VirtualBox.
You can run it on other virtualization technology (e.g., VMware), on clouds (e.g., EC2), or directly on physical hardware.

For your convenience, this tutorial includes ``Vagrantfile`` which will boot the necessary VMs.
Flocker and its dependencies will be installed on these VMs the first time you start them.
One important thing to note is that these VMs are statically assigned the IPs ``172.16.255.250`` (node1) and ``172.16.255.251`` (node2).
These two IP addresses will be used throughout the tutorial and configuration files.
If these addresses conflict with your local network configuration you can edit the ``Vagrantfile`` to use different values.
Note that you will need to make the same substitution in commands used throughout the tutorial.

The tutorial ``Vagrantfile`` can take advantage of `vagrant-cachier`_ to avoid certain redundant downloads.
You will probably want to install this plugin:

.. code-block:: console

   alice@mercury:~/flocker-tutorial$ vagrant plugin install vagrant-cachier
   Installing the 'vagrant-cachier' plugin. This can take a few minutes...
   Installed the plugin 'vagrant-cachier (0.7.2)'!
   ...
   alice@mercury:~/flocker-tutorial$

Next download the :download:`Vagrant configuration <Vagrantfile>` and the :download:`Flocker repository configuration <clusterhq-flocker.repo>`.
Save these in the same directory and preserve their filenames.
Then use ``vagrant up`` to start and provision the VMs:

.. code-block:: console

   alice@mercury:~/flocker-tutorial$ ls
   clusterhq-flocker.repo  Vagrantfile
   alice@mercury:~/flocker-tutorial$ vagrant up
   Bringing machine 'node1' up with 'virtualbox' provider...
   ==> node1: Importing base box 'clusterhq/flocker-dev'...
   ... lots of output ...
   ==> node2: ln -s '/usr/lib/systemd/system/docker.service' '/etc/systemd/system/multi-user.target.wants/docker.service'
   ==> node2: ln -s '/usr/lib/systemd/system/geard.service' '/etc/systemd/system/multi-user.target.wants/geard.service'
   alice@mercury:~/flocker-tutorial$

This step may take several minutes or more.
Beyond just booting a virtual machine to use as a node for the tutorial, it will download and build the necessary ZFS kernel modules.
Your network connectivity and CPU speed will affect how long this takes.
Fortunately this extra work is only necessary the first time you bring up a node (until you destroy it).

After ``vagrant up`` completes you may want to verify that the two VMs are really running and accepting SSH connections:

.. code-block:: console

   alice@mercury:~/flocker-tutorial$ vagrant status
   Current machine states:

   node1                     running (virtualbox)
   node2                     running (virtualbox)
   ...
   alice@mercury:~/flocker-tutorial$ vagrant ssh -c hostname node1
   node1
   Connection to 127.0.0.1 closed.
   alice@mercury:~/flocker-tutorial$ vagrant ssh -c hostname node2
   node2
   Connection to 127.0.0.1 closed.
   alice@mercury:~/flocker-tutorial$

If all goes well, the next step is to configure your SSH agent.
This will allow Flocker to authenticate itself to the VM.
If you're not sure whether you already have an SSH agent running, ``ssh-add`` can tell you.
If you don't, you'll see an error:

.. code-block:: console

   alice@mercury:~/flocker-tutorial$ ssh-add
   Could not open a connection to your authentication agent.
   alice@mercury:~/flocker-tutorial$

If you do, you'll see no output:

.. code-block:: console

   alice@mercury:~/flocker-tutorial$ ssh-add
   alice@mercury:~/flocker-tutorial$

If you don't have an SSH agent running, start one:

.. code-block:: console

   alice@mercury:~/flocker-tutorial$ eval $(ssh-agent)
   Agent pid 27233
   alice@mercury:~/flocker-tutorial$

Finally, add the Vagrant key to your agent:

.. code-block:: console

   alice@mercury:~/flocker-tutorial$ ssh-add ~/.vagrant.d/insecure_private_key
   alice@mercury:~/flocker-tutorial$

You now have two VMs running and easy SSH access to them.
This completes the Vagrant-related setup.

.. _`Vagrant`: https://docs.vagrantup.com/
.. _`VirtualBox`: https://www.virtualbox.org/
.. _`vagrant-cachier`: https://github.com/fgrehm/vagrant-cachier
