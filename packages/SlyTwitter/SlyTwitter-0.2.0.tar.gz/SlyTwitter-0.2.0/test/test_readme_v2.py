import pytest

from SlyTwitter import TwitterV2 as Twitter, OAuth2

@pytest.mark.skip(reason="Twitter API changes")
async def test_readme_v2():

    auth = OAuth2('test/twauth2.json', 'test/user22.json')

    twitter = Twitter(auth)

    me = await twitter.user()

    assert me == await twitter.user('dunkyl_')

    print(me)

    followed = await twitter.all_followed_by(me)

    follows_TechConnectify = False

    async for user in followed:
        if user.at == 'TechConnectify':
            follows_TechConnectify = True
            break

    assert follows_TechConnectify