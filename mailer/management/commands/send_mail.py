import logging

from django.conf import settings
from django.core.management.base import NoArgsCommand

from mailer.engine import send_all

from optparse import make_option

# allow a sysadmin to pause the sending of mail temporarily.
PAUSE_SEND = getattr(settings, "MAILER_PAUSE_SEND", False)


class Command(NoArgsCommand):
    help = "Do one pass through the mail queue, attempting to send all mail."
    
    option_list = NoArgsCommand.option_list+(
        make_option('--limit', action='store', dest='limit', default=None, type='int',
                    help="Limit number of messages sent in this pass (default: send all)"),
    )
    
    def handle_noargs(self, **options):
        logging.basicConfig(level=logging.DEBUG, format="%(message)s")
        logging.info("-" * 72)
        # if PAUSE_SEND is turned on don't do anything.
        if not PAUSE_SEND:
            send_all(options.get('limit'))
        else:
            logging.info("sending is paused, quitting.")
