import time
import vk_mda as vk_api

access_token = "ТОКЕН ВК"
vk_session = vk_api.VkApi(token=access_token)
vk = vk_session.get_api()
while True:
    vk.messages.setActivity(user_id='ЮЗЕР АЙДИ', type='typing', peer_id='2000000033 - такого вида', v=5.124)
    time.sleep(5)
