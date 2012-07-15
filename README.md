To add a new user:

 - set his/her main group to focweb
 - append the following command to the end of his/her ~/.bashrc file:

    umask 003

To push to the server simply push to this branch:

    bzr+ssh://dlucanin@lis.irb.hr//var/www/foc/

On the server side do a:

    bzr update

(or install the push-and-update plugin as explained [here][http://wiki.bazaar.canonical.com/BazaarForWebDevs])
