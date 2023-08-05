import asyncio

# Use standard logging in this module.
import logging

# Base class for cli subcommands.
from xchembku_cli.subcommands.base import Base

# Context creator.
from xchembku_lib.contexts.contexts import Contexts

logger = logging.getLogger()

# Specifications of services we can start, and their short names for parse args.
services = {
    "xchembku_dataface_specification": "dataface",
}


# --------------------------------------------------------------
class StartServices(Base):
    """
    Start one or more services and keep them running until ^C.
    """

    def __init__(self, args, mainiac):
        super().__init__(args)

        self.__mainiac = mainiac

    # ----------------------------------------------------------------------------------------
    def run(self):
        """ """

        # Run in asyncio event loop.
        asyncio.run(self.__run_coro())

    # ----------------------------------------------------------
    async def __run_coro(self):
        """"""

        # Load the configuration.
        xchembku_multiconf = self.get_multiconf()

        # Let the multiconf know about any mpqueue logging.
        # xchembku_multiconf.set_logging_mpqueue(self.__mainiac.mpqueue)

        context_configuration = await xchembku_multiconf.load()

        if "all" in self._args.service_names:
            selected_service_names = []
            for _, service_name in services.items():
                selected_service_names.append(service_name)
        else:
            selected_service_names = self._args.service_names

        # Change all start_as to None, except the one we are starting.
        for keyword, specification in context_configuration.items():
            if keyword in services:
                service_name = services[keyword]
                if service_name in selected_service_names:
                    specification["context"] = {"start_as": "process"}

        # Make a services context from the configuration.
        context = Contexts().build_object(context_configuration)

        # Open the context (servers and clients).
        async with context:
            try:
                # Stay up until all processes are dead.
                # TODO: Use asyncio wait or sentinel for all started processes to be dead.
                while True:
                    await asyncio.sleep(1.0)
                    if not await context.is_any_process_alive():
                        logger.info("all processes have shutdown")
                        break
            except KeyboardInterrupt:
                pass

    # ----------------------------------------------------------
    def add_arguments(parser):

        services_list = list(services.values())

        parser.add_argument(
            help='"all" or any combination of {%s}' % (" ".join(services_list)),
            nargs="+",
            type=str,
            metavar="service name(s)",
            dest="service_names",
        )

        return parser
