from kathiyawadApi.models import HeroImages, Page
from kathiyawadApi.Utils.response import localResponse
from django.db.models import Q 
from kathiyawadApi.Utils.code import ResponseCode
from kathiyawadApi.Utils.message import ResponseMessage
from kathiyawadApi.Utils.status import ResponseStatus
from django.http import HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .Tasks.HeroTasks import HeroTasks
class HeroController():
    
    @classmethod
    def GetImageByPage(cls, request):
        pageName = ''
        try:
            pageName = request.GET.get('page', '')
            page = Page.objects.get(Q(title=pageName))
            heroImages = page.HeroImages.all().order_by('index')
            imagesData = []
            for image in heroImages:
                status,data = HeroTasks.GetHeroImageData(image)
                if status:
                    imagesData.append(data)
            return localResponse(
                response=True,
                status=ResponseStatus.SUCCESS,
                code=ResponseCode.SUCCESS,
                data=imagesData,
                message=ResponseMessage.HERO_IMAGES_FETCHED
                )
        except Page.DoesNotExist:
            return localResponse(
                status=ResponseStatus.ERROR,
                code=ResponseCode.NOT_FOUND,
                data={},
                message=ResponseMessage.PAGE_NOT_FOUND.replace("{}", str(pageName))
            )
        except Exception as e:
            return localResponse(
                status=ResponseStatus.ERROR,
                code=ResponseCode.ERROR,
                data={"error": str(e)},
                message=ResponseMessage.HERO_IMAGES_FETCHED_ERROR
            )
                    
