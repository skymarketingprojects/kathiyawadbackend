from kathiyawadApi.models import HeroImages
class HeroTasks:
    @classmethod
    def GetHeroImageData(self,heroImage:HeroImages):
        try:
            data = {
                "id": heroImage.id,
                "link": heroImage.link,
                "image": heroImage.image.url,
                "index": heroImage.index,
            }
            return True, data
        except Exception as e:
            return False,str(e)