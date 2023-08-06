__all__ = ['session', 'ifpe']


from .http import session
from .resources import ifpe

configure = session.configure
