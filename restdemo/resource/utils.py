from flask import request, current_app
import inspect
import jwt

def min_length_str(min_length):
  def validate(s):
    if s is None:
      raise Exception('password required')
    if not isinstance(s, (int, str)):
      raise Exception('password format error')
    s = str(s)
    if len(s) >= min_length:
      return s
    raise Exception("String must be at least %i characters long" % min_length)
  return validate

def jwt_required(fn):
  def decode_token(*args, **kwargs):
    token = request.headers.get('Authorization')
    try:
      data = jwt.decode(
        token,
        current_app.config.get('SECRET'),
        algorithms='HS256'
      )
      if 'sub' in inspect.signature(fn).parameters:
        kwargs['sub'] = data['sub']
        
    except jwt.ExpiredSignatureError:
      return { "message": "Expired token. Please login to get a new token" }
    except jwt.InvalidTokenError:
      return { "message": "Invalid token. Please register or login" }

    return fn(*args, **kwargs)
  return decode_token
