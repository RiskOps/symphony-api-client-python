import argparse
import logging
import os

from sym_api_client_python.auth.auth import Auth
from sym_api_client_python.clients.sym_bot_client import SymBotClient
from sym_api_client_python.configure.configure import SymConfig
from sym_api_client_python.listeners.im_listener_test_imp import \
    IMListenerTestImp
from sym_api_client_python.listeners.room_listener_test_imp import \
    RoomListenerTestImp


def configure_logging():
        log_dir = os.path.join(os.path.dirname(__file__), "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        logging.basicConfig(
                filename=os.path.join(log_dir, 'example.log'),
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                filemode='w', level=logging.DEBUG
        )
        logging.getLogger("urllib3").setLevel(logging.WARNING)


def main():
        print('Python Client runs using Cert authentication')
        parser = argparse.ArgumentParser()
        parser.add_argument("--config", help="Config json file to be used")

        args = parser.parse_args()

        # Configure log
        configure_logging()

        # Cert Auth flow: pass path to certificate config.json file
        if args.config is None:
            config_path = os.path.join(os.path.dirname(__file__), "..", "resources", "config.json")
        else:
            config_path = args.config

        # Cert Auth flow: pass path to certificate config.json file
        configure = SymConfig(config_path, __file__)
        configure.load_config()
        auth = Auth(configure)
        auth.authenticate()

        # Initialize SymBotClient with auth and configure objects
        bot_client = SymBotClient(auth, configure)

        # Initialize datafeed service
        datafeed_event_service = bot_client.get_datafeed_event_service()

        # Initialize listener objects and append them to datafeed_event_service
        # Datafeed_event_service polls the datafeed and the event listeners
        # respond to the respective types of events
        im_listener_test = IMListenerTestImp(bot_client)
        datafeed_event_service.add_im_listener(im_listener_test)
        room_listener_test = RoomListenerTestImp(bot_client)
        datafeed_event_service.add_room_listener(room_listener_test)

        # Create and read the datafeed
        print('Starting datafeed')
        datafeed_event_service.start_datafeed()


if __name__ == "__main__":
    main()
