import logging

all_loggers = dict()

def __new__(module, requester):
	name = requester.__name__
	if name not in all_loggers:
		logger = logging.getLogger(name)
		all_loggers[name] = logger
	return all_loggers[name]