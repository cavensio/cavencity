import logging

log = logging.getLogger('cavencity')
log.setLevel(logging.DEBUG)

fh = logging.FileHandler('cavencity.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s %(levelname).4s [%(module)s.%(funcName)s:%(lineno)d] %(message)s'
)
fh.setFormatter(formatter)
ch.setFormatter(formatter)

log.addHandler(fh)
log.addHandler(ch)
