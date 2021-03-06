Flocker Tutorial
================

The goal of this tutorial is to teach you to use Flocker's container, network, and volume orchestration functionality.
By the time you reach the end of the tutorial you will know how to use Flocker to create an application.
You will know how to configure a persistent data volume for that application.
You will also know how to expose that application to the network and how to move it from one host to another.

This tutorial is based around the setup of a MongoDB service.
Flocker is a generic container manager.
MongoDB is used only as an example here.
Any application you can deploy into Docker you can manage with Flocker.

.. toctree::
   :maxdepth: 2

   vagrant-setup
   moving-applications
   exposing-ports
