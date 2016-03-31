PROXY_MGR

Purpose:
--------------------
The purpose of the proxy_mgr is to provide a simplified interface to interact
with a remote host via a proxy (single hop for now, multi-hop in the future).

By instantiating the proxy manager and providing the proxy host information, a
user can ping or ssh/execute commands a remote system via the remote manager.

Example:

   # Given a server_model_obj representing the proxy and
   # a remote host ip, username, & password.

   proxy = NetworkProxyMgr(use_proxy=True)
   proxy.set_proxy_server(server_obj=server_model_obj)

   output = proxy.ping(target_ip)
   response = proxy.ssh_to_target(
         target_ip=target_ip, user=<username>, password=<password>,
         cmds=<list of cmds>)

   proxy.close_connections(response)


Basic Architecture
------------------------
For code organizational purposes, the proxy server information is defined in
the NetworkProxyMgr class, and the various utility classes (ping/ssh) are
maintained as dependent mixin classes. This is done to keep the code
organized, maintainable (e.g. - ping issues are in the ping mixin), and
additional utilities can be added with minimal effort.


Basic Methods and Basic Args (not complete list):
-------------------------------------------------

   ping(target_ip, count, threshold) - Pings remote target.
      Return: (Boolean) 'count' pings sent to target_ip, minimum threshold
      of replies received.

   connect_to_proxy()
      Return: open pexpect console connection to the proxy.

   can_ssh(target_ip, user, password)
      Return: (Boolean) Was SSH connection be negotiated (via proxy).

    ssh_to_target(target_ip, user, password, cmds)
      Return: Response Object (described below) of SSH transaction.


Response Object:
------------------------
Basic storage object that contains:
    stdin - all stdin in conversation
    stdout - all stdout in conversation
    stderr - all stderr in conversation
    output - all stdin|out|err interlaced into conversation
    cmd_output - ordered dictionary of key: cmd, value: output
    errors - Any unexpected exceptions, etc.
    connection - open pexpect connection (if closed, value = None)
