import json

from buildbot.plugins import webhooks
from buildbot.util import bytes2unicode

class BitBucketHookImpl(webhooks.base):
    def getChanges(self, request):
        payload = self._get_payload(request)
        revision=payload['refChanges'][0]['toHash']

        for changeset in payload['changesets']['values']:
            if changeset['toCommit']['id'] ==  revision:
                revlink=changeset['links']['self'][0]['href'].rstrip('#README.md')
                author=changeset['toCommit']['author']['name']
                message=changeset['toCommit']['message']

        chdict = dict(
                      revision=revision,
                      repository=payload['repository']['name'],
                      project=payload['repository']['project']['name'],
                      branch=payload['refChanges'][0]['refId'],
                      revlink=revlink,
                      author=author,
                      comments='Bitbucket Server Pull Request #{} .\nCommit comment: {}'.format(revision, message) 
                      )
        print('change payload data that was sent to db: {} '.format(chdict))             
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