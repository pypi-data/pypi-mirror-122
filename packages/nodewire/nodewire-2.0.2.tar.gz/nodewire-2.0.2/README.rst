Introduction
=============

This package enables you to:

1. Create software that connects to IoT devices for monitoring and control
2. Create microservices


NodeWire uses a dataflow programming model. Nodes have input and output ports through which it receives and sends messages.
A NodeWire program can connect to other nodes to monitor and send messagesto it.

Hello NodeWire
===============

   .. code-block:: python

    import asyncio
    from nodewire import Node

    class MyNode(Node):
        def on_reset(self, value, sender):
            self.count = value

        def get_status(self, sender):
            return {
                'counting': self.start==1,
                'count': self.count
            }

        async def loop(self):
            print('connected')
            while True:
                await asyncio.sleep(1)
                if self.start==1: 
                    self.count = self.count + 1

    mynode = MyNode(nodename='hello', inputs='start reset', outputs='count status',  server='localhost')
    mynode.nw.debug = True
    mynode.nw.run()

First we created our node class. In this class, we defined message handlers that will be called when the system wants to determine the value
of our output ports (get_portname) or when it wants to forward a new value to us (on_portname).
Note that you can chose to define handlers for some ports (reset and status in this example), or chose not to (start and count). You also have the choice to make thehandler syncronous or asyncronous.
If the handler is going to take a long time to run, then it is better to make it asyncronous and use asyncio.sleep every once in a while, so that other tasks will get a chance to run.

The loop function is special. It is called only once, the first time the node establishes a successful connection to the server. It must be an async function.
This function is meant to serve as the mainloop of your nodewire application but you can also terminate it without any effect on the overal running of the run. The loop function is optional


Control and Monitor
===================

    .. code-block:: python

        from nodewire import Node

        class MyNode(Node):
            def got_count(self, nodename):
                print(counter.count)
                if counter.count == 10:
                    counter.reset = 0

            async def loop(self):
                global counter
                print('connected')
                counter = await self.get_node('hello')
                counter.start = 1
                counter.on_count = self.got_count

        mynode = MyNode(nodename='control', server='localhost')
        mynode.nw.run()

