import socketio
import json
import uuid

socket_io = socketio.Client()

responses = {}


@socket_io.on('response')
def on_message(data):
  response_id = data['data']['id']
  response = BorgoResponse(data['data']['body']['response'])
  responses[response_id] = response


@socket_io.on('initialized')
def on_message(data):
  responses['initialized'] = data


class BorgoClient:
  def __init__(self, key):
    socket_io.connect('https://borgo-server.herokuapp.com')
    whitespace_removed_key = ''.join(key.split())
    socket_io.emit(
        'initialize',
        json.dumps({'key': whitespace_removed_key})
    )
    while 'initialized' not in responses:
      pass

    is_initialized = responses.pop('initialized')
    if (not is_initialized):
      error_message = 'Key provided is invalid or expired' + \
          ' - log in to https://borgo.app/ to get a new one.'
      raise Exception(error_message)

  # Sends request to human and halts until human responds.
  def wait_for(self, request):
    request_id = str(uuid.uuid4())
    request_dict = {'id': request_id, 'body': request.to_dict()}
    socket_io.emit('request', json.dumps(request_dict))
    while request_id not in responses:
      pass
    response = responses.pop(request_id)
    socket_io.disconnect()
    return response


class BorgoRequest:
  def __init__(self, value, affirmative='Accept', negative='Reject'):
    self.value = value
    self.affirmative = affirmative
    self.negative = negative

  def to_dict(self):
    return {
        'value': self.value,
        'affirmative': self.affirmative,
        'negative': self.negative
    }


class BorgoResponse:
  def __init__(self, status):
    self.status = status
    self.is_accepted = status == 'accepted'
    self.is_rejected = not self.is_accepted
