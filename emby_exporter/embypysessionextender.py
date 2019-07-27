from embypy import Emby
import json
import requests

class EmbySessionExtender(Emby):
  @property
  def sessions_sync(self):
    return self.connector.sync_run(self.sessions)

  @property
  async def sessions(self):
    '''returns a list of all sessions.
    |force|
    |coro|
    Returns
    -------
    list
      of type :class:`embypy.objects.sessions`
    '''
    return self.extras.get('sessions', []) or \
        await self.sessions_force

  @property
  def sessions_force_sync(self):
    return self.connector.sync_run(self.sessions_force)

  @property
  async def sessions_force(self):
    # Generate URL
    url = self.connector.get_url('/Sessions', remote=False)

    # Remove device ID (Because in sessions it causes filtering)
    url = url.replace('&deviceId=EmbyPy', '')

    # Create get request for url
    sessions_request = requests.get(url)

    # Output session Data and load as json
    json_session_data = json.loads(sessions_request.content)

    # Create new list 
    items = list()

    # Filter out only devices that have content that is open (playing or paused)
    for current_session in json_session_data:
        try:
            if current_session['PlayState']['PositionTicks']:
                items.append(current_session)
        except:
            pass
    # Process (Turn into objects) all the items
    items = await self.process(items)
    self.extras['sessions'] = items
    return items
