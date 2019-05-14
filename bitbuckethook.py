import json

from buildbot.plugins import webhooks
from buildbot.util import bytes2unicode

class BitBucketHook(webhooks.base):
    def getChanges(self, request):
        payload = self._get_payload(request)
        chdict = dict(
                      revision=payload['refChanges'][0]['toHash'],
                      repository=payload['repository']['name'],
                      repo_url=payload['changesets']['values'][0]['links']['self'][0]['href'].rstrip('#README.md').rstrip('commits/{}'.format(payload['refChanges'][0]['toHash'])),
                      project=payload['repository']['project']['name'],
                      author=payload['changesets']['values'][0]['toCommit']['author']['name'],
                      branch=payload['refChanges'][0]['refId'],
                      revlink=payload['changesets']['values'][0]['links']['self'][0]['href'].rstrip('#README.md'))
        return ([chdict], None)

    def _get_payload(self, request):
        content = request.content.read()
        content = bytes2unicode(content)
        content_type = request.getHeader(b'Content-Type')
        content_type = bytes2unicode(content_type)
        if content_type.startswith('application/json'):
            payload = json.loads(content)
        else:
            raise ValueError('Unknown content type: {}'
                             .format(content_type))

        print("Payload: {}".format(payload))
        return payload